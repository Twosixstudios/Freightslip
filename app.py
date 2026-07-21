import json
import os
import pandas as pd
import streamlit as st
from database import get_all_loads, init_db, save_load
from parser import parse_rate_con_pdf

# Initialize SQLite database on app startup
init_db()

# Check if logo file exists on server
HAS_LOGO = os.path.exists("logo.png")

# Page Configuration
st.set_page_config(
    layout="wide",
    page_title="FreightSlip — AI Ingestion Engine",
    page_icon="⚡"
)

# Header Section (Failsafe with Streamlit Shortcodes)
if HAS_LOGO:
    col_logo, col_title = st.columns([1, 8])
    with col_logo:
        st.image("logo.png", width=70)
    with col_title:
        st.title("FreightSlip")
        st.caption("Automated Freight Ingestion Engine — Built by Two Six Studios")
else:
    st.title(":truck: FreightSlip")
    st.caption("Automated Freight Ingestion Engine — Built by Two Six Studios")

st.markdown("---")

# Navigation Tabs
tab_parse, tab_ledger = st.tabs([":page_facing_up: Parse Rate Con", ":bar_chart: Load Ledger"])

with tab_parse:
    # File Upload Section
    uploaded_file = st.file_uploader(
        "Upload a Rate Confirmation PDF", type=["pdf"]
    )

    if uploaded_file is not None:
        with st.spinner("Extracting visual layout and parsing load details with Gemini..."):
            try:
                # 1. Read raw PDF bytes directly for Gemini's multimodal vision engine
                pdf_bytes = uploaded_file.read()

                # 2. Parse PDF bytes directly into Pydantic schema
                rate_con = parse_rate_con_pdf(pdf_bytes)

                st.success("Successfully Parsed Rate Confirmation!")

                # --- Financial Highlights Metrics ---
                col1, col2 = st.columns([1, 1], gap="large")

                with col1:
                    st.header(" Document Preview")
                    import pypdfium2 as pdfium
                    try:
                        # Load PDF bytes directly with pypdfium2
                        pdf = pdfium.PdfDocument(pdf_bytes)
                        first_page = pdf[0]
                        # Render page at 2x scale for crisp visual quality
                        image = first_page.render(scale=2).to_pil()
                        st.image(image, use_container_width=True)
                    except Exception as pdf_err:
                        st.warning(f"Could not render visual preview: {pdf_err}")

                with col2:
                    st.header("⚡ Parsed Payload & Metrics")
                    
                    subcol1, subcol2, subcol3, subcol4 = st.columns(4)
                    subcol1.metric("Total Rate", f"${rate_con.total_pay:,.2f}")
                    subcol2.metric("Linehaul", f"${rate_con.line_haul_rate:,.2f}")
                    if hasattr(rate_con, 'broker_name') and rate_con.broker_name:
                        subcol3.metric("Broker/Carrier", rate_con.broker_name)
                    else:
                        subcol3.metric("Broker/Carrier", "N/A")
                    if hasattr(rate_con, 'total_miles') and rate_con.total_miles:
                        subcol4.metric("Mileage/RPM", f"{rate_con.total_miles or 'N/A'}")
                    else:
                        subcol4.metric("Mileage/RPM", "N/A")

                    st.markdown("---")

                    # --- Structured Load Details ---
                    st.subheader(" Load & Route Details")

                    left_col, right_col = st.columns(2)

                    with left_col:
                        st.write(f"**Broker Name:** {rate_con.broker_name or '—'}")
                        st.write(f"**Load / Ref #:** {rate_con.load_number or '—'}")
                        st.write(f"**Equipment:** {rate_con.equipment_type or '—'}")
                        st.write(f"**Commodity:** {rate_con.commodity or '—'}")

                    with right_col:
                        st.write(f"**Origin:** {rate_con.origin or '—'}")
                        st.write(f"**Destination:** {rate_con.destination or '—'}")
                        st.write(f"**Total Miles:** {rate_con.total_miles or '—'}")

                    st.markdown("---")

                    # --- Data Export & Database Save Section ---
                    st.subheader(" Export & Store Options")

                    data_dict = rate_con.model_dump()
                    json_str = json.dumps(data_dict, indent=2)

                    df_export = pd.DataFrame([data_dict])
                    csv_str = df_export.to_csv(index=False)

                    exp_col1, exp_col2, exp_col3 = st.columns(3)

                    with exp_col1:
                        st.download_button(
                            label="⬇️ Download JSON",
                            data=json_str,
                            file_name=f"ratecon_{rate_con.load_number or 'parsed'}.json",
                            mime="application/json",
                        )

                    with exp_col2:
                        st.download_button(
                            label="⬇️ Download CSV",
                            data=csv_str,
                            file_name=f"ratecon_{rate_con.load_number or 'parsed'}.csv",
                            mime="text/csv",
                        )

                    with exp_col3:
                        if st.button(" Save to Local Ledger", type="primary"):
                            save_load(rate_con)
                            st.toast("Load successfully saved to database!", icon="✅")

            except Exception as e:
                st.error(f"Error processing document: {e}")
    else:
        st.info(" Drop a PDF rate confirmation above to process load metrics.")

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
        st.info("No saved records in the database yet. Upload a rate confirmation and click 'Save to Local Ledger'.")