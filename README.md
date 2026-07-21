# FreightSlip

> Automated rate confirmation parser built by Two Six Studios.

FreightSlip takes messy, unstructured rate confirmation PDFs from freight brokers and automatically pulls out the key load details—like total pay, line haul, fuel surcharge, route details, and equipment—so you don't have to type them in manually.

👉 **Live App:** [freightslip.streamlit.app](https://freightslip.streamlit.app)

---

## Features

* **PDF Ingestion:** Upload a rate con PDF and extract structured load details in seconds using Gemini's vision engine.
* **Data Validation:** Uses Pydantic to ensure financial totals, load numbers, and route details strictly match expected data types.
* **Database Ledger:** Automatically saves parsed loads to a local SQLite database (`freightslip.db`) so you can view past records.
* **CSV & JSON Export:** Export parsed load data directly to JSON or CSV for accounting or spreadsheet tracking.

---

## How It Works

PDF Rate Con ➔ Gemini Vision API ➔ Pydantic Schema ➔ SQLite Database / CSV Export

---

## Local Setup

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/Twosixstudios/freightslip.git](https://github.com/Twosixstudios/freightslip.git)
   cd freightslip
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API key:**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY="your_api_key_here"
   ```

5. **Run the app:**
   ```bash
   streamlit run app.py
   ```

---

## Streamlit Cloud Deployment Notes

* Set `GEMINI_API_KEY` under **App Settings ➔ Secrets** using TOML format: `GEMINI_API_KEY = "your_key"`.
* The app dynamically redirects database writes to `/tmp` when running on Streamlit Cloud to handle read-only container filesystems cleanly.
