"""
Google Sheets I/O - SAFE full overwrite of RAW_DATA.
Never deletes rows (avoids Sheets API errors).
CLEAN FORMATTING - No unnecessary colors.
"""

import logging
from datetime import datetime
import gspread


class SheetsIOError(Exception):
    pass


def write_results(state: dict) -> None:
    logger = logging.getLogger("sheets_io")

    try:
        spreadsheet = state["resources"]["spreadsheet"]
        cfg = state["config"]["google_sheets"]
        sheets = cfg["sheet_names"]

        raw_data = state["transaction"].get("raw_data", [])
        if not raw_data:
            logger.warning("No raw data to write")
            return

        raw_sheet = spreadsheet.worksheet(sheets["raw_data"])

        # --------------------------------------------------
        # SAFE ERASE (values only, structure preserved)
        # --------------------------------------------------
        raw_sheet.clear()

        # --------------------------------------------------
        # Ensure sheet is large enough (expand only)
        # --------------------------------------------------
        rows_needed = len(raw_data)
        cols_needed = len(raw_data[0])

        current_rows = raw_sheet.row_count
        current_cols = raw_sheet.col_count

        if rows_needed > current_rows or cols_needed > current_cols:
            raw_sheet.resize(
                rows=max(rows_needed, current_rows),
                cols=max(cols_needed, current_cols),
            )

        # --------------------------------------------------
        # Write CSV dump
        # --------------------------------------------------
        raw_sheet.update(
            range_name="A1",
            values=raw_data,
            value_input_option="USER_ENTERED"
        )

        # --------------------------------------------------
        # CLEAN MINIMAL FORMATTING
        # --------------------------------------------------
        # Bold header row only (no colors)
        raw_sheet.format(
            "1:1",
            {"textFormat": {"bold": True}}
        )
        raw_sheet.freeze(rows=1)

        logger.info(f"RAW_DATA overwritten: {len(raw_data) - 1} rows")

        # --------------------------------------------------
        # Status + trigger reset
        # --------------------------------------------------
        _update_system_status(state, success=True)
        _reset_trigger(state)

        logger.info("All sheets updated successfully")

    except Exception as e:
        raise SheetsIOError(f"Sheets write failed: {e}")


def write_error(state: dict) -> None:
    logger = logging.getLogger("sheets_io")
    try:
        _update_system_status(state, success=False)
        _reset_trigger(state)
    except Exception as e:
        logger.error(f"Failed to write error state: {e}")


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def _update_system_status(state: dict, success: bool) -> None:
    spreadsheet = state["resources"]["spreadsheet"]
    cfg = state["config"]["google_sheets"]
    sheet = spreadsheet.worksheet(cfg["sheet_names"]["system_status"])

    t = state["transaction"]
    metrics = t.get("metrics", {})

    status_data = [
        ["Last Update Time", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        ["Symbol", t.get("symbol", "N/A")],
        ["Date Range", f"{t.get('from_date')} → {t.get('to_date')}"],
        ["Status", "SUCCESS" if success else "ERROR"],
        ["Total Rows", metrics.get("total_rows", 0)],
        ["Avg Delivery %", metrics.get("avg_delivery_pct", 0)],
        ["Max Delivery %", metrics.get("max_delivery_pct", 0)],
        ["Min Delivery %", metrics.get("min_delivery_pct", 0)],
        ["Error", t.get("error") or "None"],
    ]

    sheet.clear()
    sheet.update("A1", status_data, value_input_option="USER_ENTERED")


def _reset_trigger(state: dict) -> None:
    spreadsheet = state["resources"]["spreadsheet"]
    cfg = state["config"]["google_sheets"]

    sheet = spreadsheet.worksheet(cfg["sheet_names"]["custom_view"])
    cell = cfg["control_cells"]["trigger"]

    sheet.update(cell, [["FALSE"]], value_input_option="USER_ENTERED")