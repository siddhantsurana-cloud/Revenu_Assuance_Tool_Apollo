# Apollo Healthcare Revenue Assurance & Central Tariff Governance Platform
**Enterprise Baseline Release v2.5.2**  
*Originating Deployment Unit: Apollo Guwahati (Verified Production Build)*  
*Lead Author & Architect: Siddhant Surana <Siddhant@bihanico.in>*  
*Attribution: Powered by BRC • Engineered by BRC_SID.AI*

---

## 🌐 Public Live Web Access

The platform is published for instant public web browser access without requiring local installation or server setup:

- **Live Application URL**:  
  👉 **[https://siddhantsurana-cloud.github.io/Revenu_Assuance_Tool_Apollo/](https://siddhantsurana-cloud.github.io/Revenu_Assuance_Tool_Apollo/)**

- **Public Repository**:  
  👉 **[https://github.com/siddhantsurana-cloud/Revenu_Assuance_Tool_Apollo](https://github.com/siddhantsurana-cloud/Revenu_Assuance_Tool_Apollo)**

---

## 1. System Overview
The Apollo Healthcare Revenue Assurance Platform is an enterprise corporate financial intelligence and billing compliance suite designed to detect billing leakage, room rent multiplier violations, and procedure timed-slab tariff mismatches across corporate insurance providers (GIPSA, HDFC ERGO, IOCL, CGHS, and Apollo Kolkata/Guwahati rate cards).

This release incorporates the consolidated runtime application, local SQLite caching layer, deterministic calculation engines, verified master tariff schedules, and automated contract parsing engines.

---

## 2. Quick Start & Execution

### Option A: Direct Web Browser Access (Zero Installation)
Simply visit:  
**[https://siddhantsurana-cloud.github.io/Revenu_Assuance_Tool_Apollo/](https://siddhantsurana-cloud.github.io/Revenu_Assuance_Tool_Apollo/)**  
The full calculation engine, master tariff schedules, and billing audit analyzers run client-side via modern browser IndexedDB and Web Workers.

### Option B: Local Server Execution (Offline / High-Performance Database Sync)

#### Prerequisites
- Python 3.10+ (Standard Library only; no third-party runtime package dependencies required)
- Modern Web Browser (Google Chrome, Microsoft Edge, or Mozilla Firefox)

#### Running the Server
Execute the local startup batch script or launch via Python:
```bash
# Method 1: Windows Batch Launcher
Start_Webpage.bat

# Method 2: Direct Python Execution
python run_server.py
```
Open your browser and navigate to:  
**`http://localhost:8500`**

---

## 3. Core Architecture
- **Presentation Tier**: Responsive single-page web console (`index.html`, `css/styles.css`, `js/app.js`).
- **Calculation Tier**: Deterministic browser-based calculation engine (`revenue_assurance_engine.js`) executing 4-decimal precision variance analysis.
- **Data Tier**: Decoupled dual-storage model using browser IndexedDB for instant sub-millisecond lookups, synchronized with a local SQLite database (`revenue_audit.db`).
- **Master Registries**: Active contract schemas mapped in `tariff_data.js`.
- **Data Ingestion & Parsing Tier**: High-throughput Statement of Charges (SOC) and contract parsing engines (`soc_module/`) providing dual extraction:
  1. *Excel Engine* (`soc_module/excel_parser.py`): Tabular normalization, code alignment, and rate extraction via `openpyxl`.
  2. *PDF Engine* (`soc_module/pdf_parser.py`): Tabular PDF extraction and rate schedule reconstruction via `pdfplumber`.
  3. *Unit Compilers*: Contract-specific builders (`compile_kolkata_tariffs.py`, `compile_hdfc_agreed_2026.py`, `compile_iocl_2021.py`, `compile_excelcare_gipsa.py`).

---

## 4. Software Bill of Materials (SBOM) & Permissive Licensing
All third-party client-side libraries embedded within this distribution are bound strictly under permissive open-source licenses:
- **SheetJS** (Apache 2.0 / MIT)
- **PDF.js** (Apache 2.0)
- **Chart.js** (MIT)
- **FontAwesome Free** (MIT / SIL OFL)

There are **zero copyleft dependencies** (no GPL, AGPL, or LGPL components).
