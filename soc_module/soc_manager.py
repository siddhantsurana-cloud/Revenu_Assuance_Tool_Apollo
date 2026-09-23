"""
Central SOC Processing Manager & Pipeline Orchestrator
Apollo Revenue Audit - SOC Data Processing Module
"""

import os
from typing import Dict, List, Any, Optional

from .models import SOCRecord
from .config import MappingConfigManager
from .excel_parser import ExcelSOCParser
from .pdf_parser import PDFSOCParser
from .validator import SOCValidator
from .tariff_integrator import TariffIntegrator

class SOCProcessingManager:
    """End-to-end processing pipeline for Statement of Charges (SOC) documents."""

    def __init__(self, db_path: str = "revenue_audit.db"):
        self.mapping_manager = MappingConfigManager()
        self.excel_parser = ExcelSOCParser(self.mapping_manager)
        self.pdf_parser = PDFSOCParser(self.mapping_manager)
        self.validator = SOCValidator()
        self.integrator = TariffIntegrator(db_path=db_path)

    def process_file(
        self, 
        file_path: str, 
        sheet_name: Optional[str] = None, 
        template_name: Optional[str] = None,
        custom_mapping: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Executes the extraction and validation pipeline on an Excel or PDF file.
        Returns extracted data, column mappings, validation report, and standard JSON representation.
        """
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"File does not exist: {file_path}",
                "records": [],
                "validation": {"is_valid": False, "errors": ["File not found"]}
            }

        filename = os.path.basename(file_path)
        ext = os.path.splitext(filename)[1].lower()

        # Route to Excel or PDF parser
        if ext in [".xlsx", ".xls", ".xlsm"]:
            parse_result = self.excel_parser.parse_file(file_path, sheet_name=sheet_name, template_name=template_name)
        elif ext == ".pdf":
            parse_result = self.pdf_parser.parse_file(file_path, template_name=template_name)
        else:
            return {
                "status": "error",
                "message": f"Unsupported file extension '{ext}'. Only Excel (.xlsx, .xls) and PDF (.pdf) are supported.",
                "records": [],
                "validation": {"is_valid": False, "errors": [f"Invalid file extension: {ext}"]}
            }

        if parse_result.get("status") == "error":
            return parse_result

        raw_records = parse_result.get("records", [])

        # If custom mapping provided by user in UI, re-map records
        if custom_mapping and raw_records:
            remapped_records: List[Dict[str, Any]] = []
            for rec in raw_records:
                raw_data = rec.get("raw_data", {})
                new_rec_dict = dict(rec)
                for src_col, canon_f in custom_mapping.items():
                    if src_col in raw_data and raw_data[src_col] is not None:
                        new_rec_dict[canon_f] = raw_data[src_col]
                remapped_records.append(new_rec_dict)
            raw_records = remapped_records

        # Step 4: Validate Data
        validation_report = self.validator.validate_batch(raw_records)

        valid_records = validation_report.get("valid_records", [])
        invalid_records = validation_report.get("invalid_records", [])
        warnings_list = validation_report.get("warnings", [])

        total_count = len(raw_records)

        # Build lookup for invalid rows and warnings
        invalid_map = {inv.get("record_index"): inv.get("reasons", []) for inv in invalid_records}
        warn_map = {w.get("record_index"): w.get("warnings", []) for w in warnings_list}

        enriched_records: List[Dict[str, Any]] = []
        for idx, rec in enumerate(raw_records, start=1):
            r_dict = dict(rec)
            code = str(r_dict.get("service_code") or r_dict.get("id") or f"SRV_{idx}").strip()
            desc = str(r_dict.get("description") or r_dict.get("name") or "Unnamed Service").strip()
            rate = float(r_dict.get("rate") or r_dict.get("standard_rate") or 0.0)

            # Assign unified canonical keys for frontend compatibility
            r_dict["id"] = code
            r_dict["service_code"] = code
            r_dict["name"] = desc
            r_dict["description"] = desc
            r_dict["standard_rate"] = rate
            r_dict["rate"] = rate
            r_dict["opd_rate"] = float(r_dict.get("opd_rate") or rate)
            r_dict["ipd_rate"] = float(r_dict.get("ipd_rate") or rate)

            errs = invalid_map.get(idx, [])
            warns = warn_map.get(idx, [])

            if errs:
                r_dict["validation_status"] = "INVALID"
                r_dict["validation_errors"] = errs
                r_dict["validation_warnings"] = warns
            elif warns:
                r_dict["validation_status"] = "WARNING"
                r_dict["validation_errors"] = []
                r_dict["validation_warnings"] = warns
            else:
                r_dict["validation_status"] = "VALID"
                r_dict["validation_errors"] = []
                r_dict["validation_warnings"] = []

            enriched_records.append(r_dict)

        enriched_valid = [r for r in enriched_records if r.get("validation_status") in ("VALID", "WARNING")]
        enriched_invalid = [r for r in enriched_records if r.get("validation_status") == "INVALID"]
        enriched_warnings = [r for r in enriched_records if r.get("validation_status") == "WARNING"]

        summary = {
            "total_extracted": total_count,
            "valid_records": len(enriched_valid),
            "invalid_records": len(enriched_invalid),
            "warning_records": len(enriched_warnings)
        }

        # Step 5: Format Canonical JSON Response
        standard_json = {
            "metadata": {
                "source_file": filename,
                "document_type": "Excel" if ext in [".xlsx", ".xls", ".xlsm"] else "PDF",
                "template_name": template_name or "Auto-Detect",
                "total_extracted": total_count,
                "valid_count": len(enriched_valid),
                "invalid_count": len(enriched_invalid)
            },
            "summary": summary,
            "soc_records": enriched_valid
        }

        status = "success" if (len(enriched_valid) > 0 or total_count > 0) else "error"

        return {
            "status": status,
            "message": f"Extracted {total_count} records ({len(enriched_valid)} valid, {len(enriched_invalid)} invalid).",
            "metadata": parse_result.get("metadata", {}),
            "headers": parse_result.get("headers", []),
            "raw_headers": parse_result.get("headers", []),
            "mapping": custom_mapping or parse_result.get("column_mapping", {}),
            "column_mapping": custom_mapping or parse_result.get("column_mapping", {}),
            "available_sheets": parse_result.get("metadata", {}).get("available_sheets", []),
            "active_sheet": parse_result.get("metadata", {}).get("sheet_name", ""),
            "validation": validation_report,
            "summary": summary,
            "standard_json": standard_json,
            "records": enriched_records,
            "valid_records": enriched_valid,
            "invalid_records": enriched_invalid,
            "warning_records": enriched_warnings,
            "preview_records": enriched_records[:100] # First 100 for UI table preview
        }

    def commit_to_tariff_module(
        self, 
        valid_records: List[Dict[str, Any]], 
        file_name: str, 
        user: str = "Administrator",
        soc_name: str = "IMPORTED_SOC"
    ) -> Dict[str, Any]:
        """
        Commits validated records to Tariff Module and returns confirmation summary.
        """
        return self.integrator.commit_soc_records(valid_records, file_name, user=user, soc_name=soc_name)
