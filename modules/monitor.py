"""
Google Sheets monitoring - Connection and polling loop.
Modern auth, strict validation, zero ambiguity.
"""

import logging
import time
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

from modules import lifecycle, pipeline


# ---------------------------------------------------------------------
# Google Sheets Connection
# ---------------------------------------------------------------------
def connect_sheets(state: dict) -> None:
    """
    Authenticate with Google Sheets API and cache client.

    Updates:
    - state['resources']['sheets_client']
    - state['resources']['spreadsheet']
    """
    logger = logging.getLogger("monitor")

    config = state["config"]
    sheets_cfg = config["google_sheets"]

    logger.info("Connecting to Google Sheets API...")

    # --------------------------------------------------
    # Resolve credentials path (NO relative-path bugs)
    # --------------------------------------------------
    creds_path = Path(sheets_cfg["credentials_file"]).expanduser().resolve()

    if not creds_path.exists():
        raise FileNotFoundError(f"Google credentials file not found: {creds_path}")

    # --------------------------------------------------
    # Validate credentials JSON early (fail fast)
    # --------------------------------------------------
    try:
        import json
        with creds_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if "private_key" not in data:
            raise ValueError("Missing 'private_key' in credentials JSON")

        if not data["private_key"].startswith("-----BEGIN PRIVATE KEY-----"):
            raise ValueError("Invalid private_key format (not PEM)")

    except Exception as e:
        logger.error(f"Invalid credentials file: {e}")
        raise

    # --------------------------------------------------
    # Authorize using google-auth (NOT oauth2client)
    # --------------------------------------------------
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = Credentials.from_service_account_file(
            str(creds_path),
            scopes=scopes
        )

        client = gspread.authorize(creds)

        spreadsheet_id = sheets_cfg["spreadsheet_id"]
        spreadsheet = client.open_by_key(spreadsheet_id)

        state["resources"]["sheets_client"] = client
        state["resources"]["spreadsheet"] = spreadsheet

        logger.info(f"✅ Connected to spreadsheet: {spreadsheet.title}")

    except gspread.exceptions.SpreadsheetNotFound:
        logger.error(f"Spreadsheet not found: {sheets_cfg['spreadsheet_id']}")
        raise

    except Exception as e:
        logger.error(f"Failed to connect to Google Sheets: {e}")
        raise


# ---------------------------------------------------------------------
# Polling Loop
# ---------------------------------------------------------------------
def poll_loop(state: dict) -> None:
    """
    Main monitoring loop - polls Google Sheets for trigger.
    """
    logger = logging.getLogger("monitor")

    poll_interval = state["config"]["google_sheets"]["poll_interval_seconds"]
    logger.info(f"Monitoring started (poll interval: {poll_interval}s)")

    while lifecycle.is_running(state):
        try:
            if check_trigger(state):
                logger.info("🔔 Trigger detected - executing pipeline")
                pipeline.run(state)

            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break

        except Exception as e:
            logger.error(f"Monitor loop error: {e}")
            time.sleep(poll_interval)

    logger.info("Monitoring loop stopped")


# ---------------------------------------------------------------------
# Trigger Detection
# ---------------------------------------------------------------------
def check_trigger(state: dict) -> bool:
    """
    Check if user trigger is active in CUSTOM_VIEW sheet.
    """
    logger = logging.getLogger("monitor")

    cfg = state["config"]["google_sheets"]
    sheet_names = cfg["sheet_names"]
    cells = cfg["control_cells"]

    try:
        spreadsheet = state["resources"]["spreadsheet"]
        sheet = spreadsheet.worksheet(sheet_names["custom_view"])

        symbol = sheet.acell(cells["symbol"]).value
        from_date = sheet.acell(cells["from_date"]).value
        to_date = sheet.acell(cells["to_date"]).value
        trigger = sheet.acell(cells["trigger"]).value

        if trigger and trigger.strip().upper() in {"TRUE", "YES", "1", "X"}:
            if not symbol or not from_date or not to_date:
                logger.warning("Trigger active but inputs incomplete")
                return False

            state["transaction"]["symbol"] = symbol.strip().upper()
            state["transaction"]["from_date"] = from_date.strip()
            state["transaction"]["to_date"] = to_date.strip()

            logger.info(
                f"Trigger accepted: {symbol} ({from_date} → {to_date})"
            )
            return True

        return False

    except gspread.exceptions.WorksheetNotFound:
        logger.error(f"Worksheet not found: {sheet_names['custom_view']}")
        return False

    except Exception as e:
        logger.error(f"Trigger check failed: {e}")
        return False
