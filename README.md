# Apollo Healthcare Revenue Assurance & Central Tariff Governance Platform
**Enterprise Baseline Release v2.5.2**  
*Originating Deployment Unit: Apollo Guwahati (Verified Production Build)*

---

## 1. System Overview
The Apollo Healthcare Revenue Assurance Platform is an enterprise corporate financial intelligence and billing compliance suite designed to detect billing leakage, room rent multiplier violations, and procedure timed-slab tariff mismatches.

This release incorporates the consolidated runtime application, local SQLite caching layer, deterministic calculation engines, and verified master tariff schedules.

---

## 2. Quick Start & Execution

### Prerequisites
- Python 3.10+ (Standard Library only; no third-party package dependencies required for runtime execution)
- Modern Web Browser (Google Chrome, Microsoft Edge, or Mozilla Firefox)

### Running the Server
Execute the local startup batch script or launch via Python:
```bash
# Option A: Windows Batch Launcher
Start_Webpage.bat

# Option B: Direct Python Execution
python run_server.py
```
Open your browser and navigate to:  
`http://localhost:8000`

---

## 3. Core Architecture
- **Presentation Tier**: Responsive single-page web console (`index.html`, `css/styles.css`, `js/app.js`).
- **Calculation Tier**: Deterministic browser-based calculation engine (`revenue_assurance_engine.js`) executing 4-decimal precision variance analysis.
- **Data Tier**: Decoupled dual-storage model using browser IndexedDB for instant sub-millisecond lookups, synchronized with a local SQLite database (`revenue_audit.db`).
- **Master Registries**: Active contract schemas mapped in `tariff_data.js`.
- **Data Ingestion & Parsing Tier**: High-throughput Statement of Charges (SOC) and contract parsing engines (`soc_module/`) providing dual extraction:
  1. *Excel Engine* (`soc_module/excel_parser.py`): Tabular normalization, code alignment, and rate extraction via `openpyxl`.
  2. *PDF Engine* (`soc_module/pdf_parser.py`): Tabular PDF extraction and rate schedule reconstruction via `pdfplumber`.
  3. *Unit Compilers*: Contract-specific builders (`compile_kolkata_tariffs.py`, `compile_hdfc_agreed_2026.py`, `compile_iocl_2021.py`).

---

## 4. Software Bill of Materials (SBOM) & Permissive Licensing
All third-party client-side libraries embedded within this distribution are bound strictly under permissive open-source licenses:
- SheetJS (Apache 2.0 / MIT)
- PDF.js (Apache 2.0)
- Chart.js (MIT)
- FontAwesome Free (MIT / SIL OFL)

There are **zero copyleft dependencies** (no GPL, AGPL, or LGPL components).
