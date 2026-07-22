import base64
import io
import json
import os
import pandas as pd
import pypdfium2 as pdfium
import streamlit as st

from calculator import calculate_profitability
from database import get_all_loads, init_db, save_load
from parser import parse_rate_con_pdf

# Initialize SQLite database on app startup
init_db()

# Check if logo file exists on server
HAS_LOGO = os.path.exists("logo.png")


@st.cache_data(show_spinner=False)
def parse_pdf_cached(pdf_bytes: bytes):
    return parse_rate_con_pdf(pdf_bytes)


# Page Configuration
st.set_page_config(
    layout="wide",
    page_title="FreightSlip — AI Ingestion Engine",
    page_icon="⚡",
)

# Header Section
if HAS_LOGO:
    try:
        with open("logo.png", "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")

        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 15px;">
                <img src="data:image/png;base64,{logo_b64}" style="height: 85px; width: auto; object-fit: contain; border-radius: 6px;">
                <div>
                    <h1 style="margin: 0; padding: 0; font-size: 2.3rem; font-weight: 700; line-height: 1.1;">FreightSlip</h1>
                    <p style="margin: 4px 0 0 0; padding: 0; color: #a3a8b8; font-size: 0.95rem;">Automated Freight Ingestion Engine — Built by Two Six Studios</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    except Exception:
        st.title("⚡ FreightSlip")
        st.caption(
            "Automated Freight Ingestion Engine — Built by Two Six Studios"
        )
else:
    st.title("⚡ FreightSlip")
    st.caption("Automated Freight Ingestion Engine — Built by Two Six Studios")

st.markdown("---")

# Navigation Tabs
tab_parse, tab_ledger = st.tabs(
    [":page_facing_up: Parse Rate Con", ":bar_chart: Load Ledger"]
)

with tab_parse:
    uploaded_file = st.file_uploader(
        "Upload a Rate Confirmation PDF", type=["pdf"]
    )

    if uploaded_file is not None:
        with st.spinner(
            "Extracting visual layout and parsing load details with Gemini..."
        ):
            try:
                pdf_bytes = uploaded_file.read()
                rate_con = parse_pdf_cached(pdf_bytes)

                st.success("Successfully Parsed Rate Confirmation!")

                # --- Side-by-Side View ---
                col1, col2 = st.columns([1, 1], gap="large")

                # LEFT COLUMN: Live PDF Document Preview
                with col1:
                    st.header(":page_facing_up: Document Preview")
                    try:
                        pdf = pdfium.PdfDocument(pdf_bytes)
                        total_pages = len(pdf)

                        if total_pages > 1:
                            page_num = st.slider(
                                f"Page Selection (Total Pages: {total_pages})",
                                min_value=1,
                                max_value=total_pages,
                                value=1,
                            )
                        else:
                            page_num = 1

                        selected_page = pdf[page_num - 1]
                        image = selected_page.render(scale=2).to_pil()

                        img_buf = io.BytesIO()
                        image.save(img_buf, format="PNG")
                        img_b64 = base64.b64encode(img_buf.getvalue()).decode(
                            "utf-8"
                        )

                        st.markdown(
                            f"""
                            <div style="max-height: 800px; overflow-y: auto; border: 1px solid #2e3440; border-radius: 8px; padding: 6px; background-color: #1a1c23; text-align: center;">
                                <img src="data:image/png;base64,{img_b64}" style="max-width: 100%; height: auto; border-radius: 4px;">
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    except Exception as pdf_err:
                        st.warning(f"Could not render visual preview: {pdf_err}")

                # RIGHT COLUMN: Parsed Metrics, Calculator & Actions
                with col2:
                    st.header(":zap: Parsed Payload & Metrics")

                    subcol1, subcol2, subcol3, subcol4 = st.columns(4)
                    subcol1.metric("Total Rate", f"${rate_con.total_pay:,.2f}")
                    subcol2.metric(
                        "Linehaul", f"${rate_con.line_haul_rate:,.2f}"
                    )

                    if (
                        hasattr(rate_con, "broker_name")
                        and rate_con.broker_name
                    ):
                        subcol3.metric("Broker/Carrier", rate_con.broker_name)
                    else:
                        subcol3.metric("Broker/Carrier", "N/A")

                    if (
                        hasattr(rate_con, "total_miles")
                        and rate_con.total_miles
                    ):
                        subcol4.metric(
                            "Mileage/RPM", f"{rate_con.total_miles or 'N/A'}"
                        )
                    else:
                        subcol4.metric("Mileage/RPM", "N/A")

                    st.markdown("---")

                    # --- Interactive Trip Profitability Calculator ---
                    st.subheader("� Trip Profitability & Decision Engine")

                    with st.expander(
                        "� Adjust Operating Expenses & Deadhead",
                        expanded=True,
                    ):
                        calc_col1, calc_col2, calc_col3 = st.columns(3)

                        with calc_col1:
                            deadhead_input = st.number_input(
                                "Deadhead Miles",
                                min_value=0,
                                value=45,
                                step=5,
                            )
                            diesel_input = st.number_input(
                                "Diesel Price ($/gal)",
                                min_value=1.00,
                                value=3.85,
                                step=0.05,
                            )

                        with calc_col2:
                            mpg_input = st.number_input(
                                "Truck MPG",
                                min_value=3.0,
                                value=6.5,
                                step=0.1,
                            )
                            maint_input = st.number_input(
                                "Maintenance ($/mi)",
                                min_value=0.00,
                                value=0.15,
                                step=0.01,
                            )

                        with calc_col3:
                            tolls_input = st.number_input(
                                "Tolls & Misc ($)",
                                min_value=0,
                                value=25,
                                step=5,
                            )

                        # Run Profitability Calculation
                        profit_data = calculate_profitability(
                            gross_pay=rate_con.total_pay,
                            loaded_miles=rate_con.total_miles,
                            deadhead_miles=deadhead_input,
                            diesel_price=diesel_input,
                            truck_mpg=mpg_input,
                            maintenance_cost_per_mile=maint_input,
                            tolls_misc=tolls_input,
                        )

                        # Decision Card Display
                        st.markdown(
                            f"""
                            <div style="background-color: #1e2330; border-left: 5px solid {'#10b981' if profit_data.net_rpm >= 1.20 else '#f59e0b' if profit_data.net_rpm >= 0.75 else '#ef4444'}; padding: 12px; border-radius: 6px; margin-top: 10px;">
                                <h4 style="margin:0; font-size: 1.1rem; color: #f8fafc;">{profit_data.status_emoji} {profit_data.status}</h4>
                                <p style="margin: 4px 0 0 0; color: #94a3b8; font-size: 0.9rem;">
                                    True RPM: <b>${profit_data.true_rpm:.2f}/mi</b> | Net Profit / Mile: <b>${profit_data.net_rpm:.2f}/mi</b>
                                </p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        # Profitability Metric Badges
                        m_col1, m_col2, m_col3 = st.columns(3)
                        m_col1.metric(
                            "Net Profit", f"${profit_data.net_profit:,.2f}"
                        )
                        m_col2.metric(
                            "Est. Fuel Cost",
                            f"${profit_data.fuel_cost:,.2f}",
                        )
                        m_col3.metric(
                            "Total Expenses",
                            f"${profit_data.total_expenses:,.2f}",
                        )

                    st.markdown("---")

                    # --- Structured Load Details ---
                    st.subheader(":clipboard: Load & Route Details")

                    left_col, right_col = st.columns(2)

                    with left_col:
                        st.write(
                            f"**Broker Name:** {rate_con.broker_name or '—'}"
                        )
                        st.write(
                            f"**Load / Ref #:** {rate_con.load_number or '—'}"
                        )
                        st.write(
                            f"**Equipment:** {rate_con.equipment_type or '—'}"
                        )
                        st.write(
                            f"**Commodity:** {rate_con.commodity or '—'}"
                        )

                    with right_col:
                        st.write(f"**Origin:** {rate_con.origin or '—'}")
                        st.write(
                            f"**Destination:** {rate_con.destination or '—'}"
                        )
                        st.write(
                            f"**Total Miles:** {rate_con.total_miles or '—'}"
                        )

                    st.markdown("---")

                    # --- Data Export & Database Save Section ---
                    st.subheader(":floppy_disk: Export & Store Options")

                    data_dict = rate_con.model_dump()
                    json_str = json.dumps(data_dict, indent=2)

                    df_export = pd.DataFrame([data_dict])
                    csv_str = df_export.to_csv(index=False)

                    exp_col1, exp_col2, exp_col3 = st.columns(3)

                    with exp_col1:
                        st.download_button(
                            label="Download JSON",
                            data=json_str,
                            file_name=f"ratecon_{rate_con.load_number or 'parsed'}.json",
                            mime="application/json",
                        )

                    with exp_col2:
                        st.download_button(
                            label="Download CSV",
                            data=csv_str,
                            file_name=f"ratecon_{rate_con.load_number or 'parsed'}.csv",
                            mime="text/csv",
                        )

                    with exp_col3:
                        if st.button("Save to Local Ledger", type="primary"):
                            save_load(rate_con)
                            st.toast(
                                "Load successfully saved to database!",
                                icon="✅",
                            )

            except Exception as e:
                err_msg = str(e)
                if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                    st.error(
                        "⏳ **Gemini Free Tier Rate Limit Reached.** Please wait ~60 seconds before trying again!"
                    )
                else:
                    st.error(f"Error processing document: {e}")
    else:
        st.info("Drop a PDF rate confirmation above to process load metrics.")

with tab_ledger:
    st.subheader("Database History (`freightslip.db`)")
    records = get_all_loads()

    if records:
        data = [
            {
                "ID": r.id,
                "Broker": r.broker_name,
                "Load #": r.load_number,
                "Total Pay": f"${r.total_pay:,.2f}",
                "Line Haul": f"${r.line_haul_rate:,.2f}",
                "Fuel Surcharge": f"${r.fuel_surcharge:,.2f}",
                "Origin": r.origin,
                "Destination": r.destination,
                "Equipment": r.equipment_type,
                "Commodity": r.commodity,
                "Miles": r.total_miles,
                "Saved At": r.created_at.strftime("%Y-%m-%d %H:%M"),
            }
            for r in records
        ]
        df_ledger = pd.DataFrame(data)
        st.dataframe(df_ledger, use_container_width=True)
    else:
        st.info(
            "No saved records in the database yet. Upload a rate confirmation and click 'Save to Local Ledger'."
        )