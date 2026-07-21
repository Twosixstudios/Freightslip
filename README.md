# 🚚 Rate Confirmation AI Parser
> **Automated Freight Ingestion Engine — Built by Two Six Studios**

An intelligent, multimodal document processing engine that automatically extracts financial metrics, load references, and route details from logistics Rate Confirmation PDFs using **Google Gemini AI** and **Streamlit**.

---

## ✨ Key Features

* 👁️ **Multimodal PDF Processing:** Ingests raw PDF document bytes directly via Gemini's vision engine without relying on brittle text-scraping libraries.
* 🎯 **Structured Schema Validation:** Enforces strict data types and JSON output using **Pydantic** schema definitions (`RateConfirmation`).
* 📊 **Financial Highlights Dashboard:** Displays critical revenue figures (**Total Pay**, **Line Haul**, **Fuel Surcharge**) in clean high-level metrics.
* 📦 **Load & Route Extraction:** Automatically captures Broker Name, Load Reference Number, Origin, Destination, Equipment Type, and Mileage.
* 💾 **Multi-Format Exporting:** Download structured load payloads with a single click in **JSON** or **CSV** formats.

---

## 🛠️ Tech Stack

* **Language:** Python 3.14+
* **Frontend:** [Streamlit](https://streamlit.io/)
* **AI Engine:** Google Gemini SDK (`google-genai`)
* **Data Validation:** [Pydantic](https://docs.pydantic.dev/)
* **Data Analysis:** Pandas

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your system.

### 2. Installation
Clone the repository and set up a virtual environment:

```bash
git clone [https://github.com/Twosixstudios/ratecon-ai-parser.git](https://github.com/Twosixstudios/ratecon-ai-parser.git)
cd ratecon-ai-parser

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
