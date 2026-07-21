import json
import pandas as pd
import streamlit as st
from parser import parse_rate_con_pdf

# Page Configuration
st.set_page_config(
    page_title="Rate Con AI Parser | Two Six Studios",
    page_icon=":page_facing_up:",
    layout="wide",
)

st.title(":page_facing_up: Rate Confirmation AI Parser")
st.caption("Automated Freight Ingestion Engine — Built by Two Six Studios")
st.markdown("---")

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
            st.subheader(":package: Load & Route Details")

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

            # --- Data Export Section ---
            st.subheader(":floppy_disk: Export Options")

            data_dict = rate_con.model_dump()
            json_str = json.dumps(data_dict, indent=2)

            df = pd.DataFrame([data_dict])
            csv_str = df.to_csv(index=False)

            exp_col1, exp_col2 = st.columns(2)

            with exp_col1:
                st.download_button(
                    label=":arrow_down: Download JSON",
                    data=json_str,
                    file_name=f"ratecon_{rate_con.load_number or 'parsed'}.json",
                    mime="application/json",
                )

            with exp_col2:
                st.download_button(
                    label=":arrow_down: Download CSV",
                    data=csv_str,
                    file_name=f"ratecon_{rate_con.load_number or 'parsed'}.csv",
                    mime="text/csv",
                )

        except Exception as e:
            st.error(f"Error processing document: {e}")
else:
    st.info(":bulb: Drop a PDF rate confirmation above to process load metrics.")