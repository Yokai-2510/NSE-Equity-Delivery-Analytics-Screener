"""
Hardcoded Google Sheets write test.
Writes TEST_OK to SYSTEM_STATUS!B12.
No settings.json. No state. No excuses.
"""

from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials


# --------------------------------------------------
# HARD-CODED VALUES (EDIT ONLY IF NEEDED)
# --------------------------------------------------

CREDENTIALS_FILE = Path("config/credentials.json").resolve()

SPREADSHEET_ID = "1j-dHdL-9xeLE6mSkTd-XF3OI4mtKnDoV4donfbl80gw"

TARGET_SHEET = "SYSTEM_STATUS"
TARGET_CELL = "B12"


# --------------------------------------------------
# Sanity checks
# --------------------------------------------------
if not CREDENTIALS_FILE.exists():
    raise FileNotFoundError(f"Credentials file not found: {CREDENTIALS_FILE}")


# --------------------------------------------------
# Authenticate (modern google-auth)
# --------------------------------------------------
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    str(CREDENTIALS_FILE),
    scopes=scopes
)

client = gspread.authorize(creds)


# --------------------------------------------------
# Open sheet and write test value
# --------------------------------------------------
spreadsheet = client.open_by_key(SPREADSHEET_ID)
sheet = spreadsheet.worksheet(TARGET_SHEET)

sheet.update(
    range_name=TARGET_CELL,
    values=[["TEST_OK"]],
    value_input_option="USER_ENTERED"
)

print("✅ SUCCESS: TEST_OK written to SYSTEM_STATUS!B12")
