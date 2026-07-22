# FreightSlip

> Automated rate confirmation parser & trip profitability engine built by Two Six Studios.

FreightSlip takes messy, unstructured rate confirmation PDFs from freight brokers and automatically extracts key load metrics using multimodal AI. It features a side-by-side document previewer, a real-time dispatch decision engine, and local ledger tracking.

👉 **Live App:** [freightslip.streamlit.app](https://freightslip.streamlit.app)

---

## Features

* **Multimodal AI Ingestion:** Extracts structured load details (linehaul, FSC, total pay, broker info, equipment, commodities, route details) in seconds using Gemini's vision engine.
* **Side-by-Side Document Preview:** Interactive PDF page renderer powered by `pypdfium2` with multi-page navigation controls.
* **Trip Profitability Calculator:** Real-time RPM and net profit decision engine accounting for deadhead miles, diesel prices, truck MPG, maintenance costs, and tolls.
* **API Response Caching:** Uses Streamlit caching (`@st.cache_data`) to prevent duplicate Gemini API requests during UI interaction.
* **Data Validation & Persistence:** Enforces structure with Pydantic and saves records to a local SQLite database (`freightslip.db`).
* **CSV & JSON Export:** Instant data downloads for accounting or fleet management.

---

## Project Structure

* `app.py` - Streamlit application UI and layout
* `parser.py` - Gemini Vision prompt logic and Pydantic schemas
* `calculator.py` - Standalone trip profitability and RPM decision module
* `database.py` - SQLite helper functions and data persistence
* `generate_mock_pdf.py` - Script to generate realistic multi-page test PDFs

---

## Local Setup

1. **Clone the repository:**
    git clone [https://github.com/Twosixstudios/freightslip.git](https://github.com/Twosixstudios/freightslip.git)
    cd freightslip

2. **Create and activate a virtual environment:**
    python3 -m venv venv
    source venv/bin/activate

3. **Install dependencies:**
    pip install -r requirements.txt

4. **Add your API key:**
    Create a `.env` file in the root directory:
    GEMINI_API_KEY="your_api_key_here"

5. **Run the app:**
    streamlit run app.py

---

## Generating Test Data

To create a realistic multi-page rate confirmation PDF for local testing:

    python generate_mock_pdf.py

This creates `mock_rate_con_multipage.pdf` in the root folder, ready to upload directly into the app interface.

---

## Streamlit Cloud Deployment Notes

* Set `GEMINI_API_KEY` under **App Settings ➔ Secrets** using TOML format: `GEMINI_API_KEY = "your_key"`.
* The app dynamically redirects database writes to `/tmp` when running on Streamlit Cloud to handle read-only container filesystems cleanly.
