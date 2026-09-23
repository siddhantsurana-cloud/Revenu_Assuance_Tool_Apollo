# Software Bill of Materials (SBOM)
**Platform**: Apollo Healthcare Revenue Assurance Platform  
**Version**: 2.5.2 Enterprise Baseline  

| Component | Version | License | Usage / Purpose |
| :--- | :--- | :--- | :--- |
| **Python Standard Library** | 3.10+ | PSF License | Local HTTP synchronization server (`http.server`, `sqlite3`, `json`) |
| **SheetJS (xlsx.full.min.js)** | 0.18.5 | Apache 2.0 | In-browser Excel workbook ingestion |
| **PDF.js (pdf.min.js)** | 2.14.305 | Apache 2.0 | In-browser contract rendering & text reading |
| **Chart.js** | 3.9.1 | MIT License | Revenue trend visualizations and variance analytics |
| **openpyxl** | 3.1.2+ | MIT License | Server-side Excel workbook parsing & tariff compilation (`soc_module/`) |
| **pdfplumber** | 0.10.0+ | MIT License | Server-side PDF contract table extraction & fuzzy mapping |
| **Vanilla JS Engine** | Custom | Proprietary (Assigned to AHEL) | Calculation engine, audit rules, and UI controllers |

**License Compliance Warranty**: No components are licensed under GNU GPL, AGPL, or any viral copyleft framework. All libraries are MIT, Apache 2.0, or PSF permissive licenses.
