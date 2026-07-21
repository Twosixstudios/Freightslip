# 🚚 FreightSlip

> **Automated Freight Ingestion & Rate Con Processing Engine**  
> *Built by Two Six Studios*

---

## 📌 Overview

**FreightSlip** is an AI-powered document processing web application designed to eliminate manual data entry in freight dispatch operations. By leveraging Google Gemini's multimodal vision engine and Pydantic schema enforcement, FreightSlip instantly extracts financial metrics, route logistics, and broker reference numbers directly from unstructured PDF Rate Confirmations.

With built-in **SQLite & SQLAlchemy persistence**, every parsed load can be saved directly to a persistent database ledger, providing real-time revenue tracking and load history.

---

## 🧩 Modular Integration with Fleet Scout

FreightSlip is engineered both as a high-speed standalone utility and as a **pluggable microservice module for Fleet Scout**—Two Six Studios' flagship dispatch and fleet orchestration platform.

* **Step 1:** Ingest PDF Rate Confirmation directly into FreightSlip.
* **Step 2:** Gemini Vision extracts and validates load parameters into structured Pydantic schemas.
* **Step 3:** Validated payloads write to SQLite/SQLAlchemy ORM.
* **Step 4:** Data passes directly to `fleetscout-core` for active driver assignment and route dispatching.

---

## 🔥 Key Features

* **🤖 Multimodal AI Ingestion:** Processes raw PDF byte streams using Google's Gemini Vision API.
* **🛡️ Strict Schema Enforcement:** Uses **Pydantic** to guarantee typed data models (`total_pay`, `line_haul_rate`, `fuel_surcharge`, `origin`, `destination`, `total_miles`, `commodity`).
* **🗄️ Persistent Load Ledger:** Saves parsed rate confirmation records directly to a local **SQLite** database via **SQLAlchemy ORM**.
* **📊 Historical Load Ledger Tab:** Displays a clean, filterable data grid of all past ingested freight loads.
* **💾 Multi-Format Exports:** Download structured load payloads in one click as formatted **JSON** or **CSV** files.

---

## 🛠️ Tech Stack

* **Frontend / UI:** Streamlit
* **AI & Document Processing:** Google GenAI SDK
* **Data Modeling:** Pydantic V2
* **Database & ORM:** SQLite & SQLAlchemy
* **Data Processing:** Pandas

---

## 🏢 About Two Six Studios

Building database-driven Python applications, Streamlit tools, and practical local AI pipelines grounded in real-world logistics and operational logic.
