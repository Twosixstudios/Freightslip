import json
import pandas as pd
import streamlit as st
from parser import parse_rate_con_pdf
from database import init_db, save_load, get_all_loads

# Initialize SQLite database on app startup
init_db()

# Page Configuration
st.set_page_config(
    page_title="FreightSlip | Two Six Studios",
    page_icon="�",
    layout="wide",
)

st.title("� FreightSlip")
st.caption("Automated Freight Ingestion Engine — Built by Two Six Studios")
st.markdown("---")

# Navigation Tabs
tab_parse, tab_ledger = st.tabs(["� Parse Rate Con", "� Load Ledger"])

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
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Pay", f"${rate_con.total_pay:,.2f}")
                col2.metric("Line Haul", f"${rate_con.line_haul_rate:,.2f}")
                col3.metric("Fuel Surcharge", f"${rate_con.fuel_surcharge:,.2f}")

                st.markdown("---")

                # --- Structured Load Details ---
                st.subheader("� Load & Route Details")

                left_col, right_col = st.columns(2)

                with left_col:
                    st.write(f"**Broker Name:** {rate_con.broker_name or 'N/A'}")
                    st.write(f"**Load / Ref #:** {rate_con.load_number or 'N/A'}")
                    st.write(f"**Equipment:** {rate_con.equipment_type or 'N/A'}")
                    st.write(f"**Commodity:** {rate_con.commodity or 'N/A'}")

                with right_col:
                    st.write(f"**Origin:** {rate_con.origin or 'N/A'}")
                    st.write(f"**Destination:** {rate_con.destination or 'N/A'}")
                    st.write(f"**Total Miles:** {rate_con.total_miles or 'N/A'}")

                st.markdown("---")

                # --- Data Export & Database Save Section ---
                st.subheader("� Export & Store Options")

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
                    if st.button("�️ Save to Local Ledger", type="primary"):
                        save_load(rate_con)
                        st.toast("Load successfully saved to database!", icon="✅")

            except Exception as e:
                st.error(f"Error processing document: {e}")
    else:
        st.info("� Drop a PDF rate confirmation above to process load metrics.")

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