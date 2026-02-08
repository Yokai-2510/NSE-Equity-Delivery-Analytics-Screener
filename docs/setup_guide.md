# NSE Analytics - Complete Setup Guide

**Time Required:** 20 minutes  
**Difficulty:** Beginner-friendly  
**Cost:** Free (Google Cloud free tier)

---

## 📋 Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Google Cloud Setup](#2-google-cloud-setup)
3. [Google Sheets Setup](#3-google-sheets-setup)
4. [Python Installation](#4-python-installation)
5. [Configuration](#5-configuration)
6. [First Run](#6-first-run)
7. [Verification](#7-verification)

---

## 1. Prerequisites

### What You Need

- ✅ Google Account (free - gmail.com)
- ✅ Computer with Python 3.9+
- ✅ Internet connection
- ✅ 20 minutes

### Check Python Version

**Windows:**
```cmd
python --version
```

**macOS/Linux:**
```bash
python3 --version
```

**Expected:** `Python 3.9.0` or higher

**If not installed:** Download from [python.org/downloads](https://www.python.org/downloads/)

---

## 2. Google Cloud Setup

### 2.1 Create Google Cloud Project

**Step 1:** Go to [console.cloud.google.com](https://console.cloud.google.com)

**Step 2:** Create New Project
1. Click **Select a project** dropdown (top-left)
2. Click **NEW PROJECT**
3. Enter name: `NSE Analytics`
4. Click **CREATE**
5. Wait 10 seconds
6. Select the new project from dropdown

---

### 2.2 Enable APIs

**Step 1: Enable Google Sheets API**

1. In Google Cloud Console, open ☰ menu (top-left)
2. Go to: **APIs & Services** → **Library**
3. Search: `Google Sheets API`
4. Click result
5. Click **ENABLE**
6. Wait for confirmation

**Step 2: Enable Google Drive API**

1. Click **<- Back to Library** (or search again)
2. Search: `Google Drive API`
3. Click result  
4. Click **ENABLE**
5. Wait for confirmation

---

### 2.3 Create Service Account

**Step 1:** Navigate to Service Accounts

1. Open ☰ menu
2. Go to: **APIs & Services** → **Credentials**
3. Click **+ CREATE CREDENTIALS** (top)
4. Select **Service Account**

**Step 2:** Fill Service Account Details

1. **Service account name:** `nse-analytics-service`
2. **Service account ID:** (auto-filled)
3. Click **CREATE AND CONTINUE**

**Step 3:** Grant Permissions (Skip)

1. Click **CONTINUE** (no role needed)

**Step 4:** Grant Access (Skip)

1. Click **DONE**

---

### 2.4 Create Service Account Key

**Step 1:** Find Your Service Account

1. You'll see your service account in the list
2. Email format: `nse-analytics-service@your-project.iam.gserviceaccount.com`
3. **COPY THIS EMAIL** (you'll need it later)

**Step 2:** Create JSON Key

1. Click on the service account email
2. Go to **KEYS** tab
3. Click **ADD KEY** → **Create new key**
4. Select **JSON**
5. Click **CREATE**

**Step 3:** Save the File

1. File downloads as `your-project-xxxxx.json`
2. **Rename it to:** `credentials.json`
3. **Move it to your project:** `nse-analytics/config/credentials.json`

⚠️ **IMPORTANT:** Never share or commit this file to Git!

---

## 3. Google Sheets Setup

### Option A: Use Template Spreadsheet (Recommended)

**Step 1:** Copy Template

There's a template Excel file in `config/NSE_Equity_Delivery_Analytics_System.xlsx`

1. Go to [Google Sheets](https://sheets.google.com)
2. Click **File** → **Import**
3. Upload the Excel file from `config/` folder
4. Click **Import data**

**Step 2:** Share with Service Account

1. Click **Share** button (top-right)
2. Paste the service account email (from step 2.4)
3. Change permissions to **Editor**
4. **Uncheck** "Notify people"
5. Click **Share**

**Step 3:** Copy Spreadsheet ID

From URL:
```
https://docs.google.com/spreadsheets/d/1ABC123xyz/edit
                                        ^^^^^^^^^
                                   This is the ID
```

Copy `1ABC123xyz` part

---

### Option B: Create From Scratch

**Step 1:** Create New Sheet

1. Go to [sheets.google.com](https://sheets.google.com)
2. Click **+ Blank**

**Step 2:** Create Tabs

Create 5 sheets (tabs at bottom):
1. `CUSTOM_VIEW`
2. `RAW_DATA`
3. `CUSTOM_DATA`
4. `DELIVERY_CHARTS`
5. `SYSTEM_STATUS`

**Step 3:** Setup CUSTOM_VIEW

In the `CUSTOM_VIEW` sheet:

| Cell | Content |
|------|---------|
| A1 | `NSE EQUITY DELIVERY ANALYTICS` |
| A3 | `INPUT PARAMETERS` |
| A4 | `Symbol` |
| C4 | (leave empty - user input) |
| A5 | `From Date (DD-MM-YYYY)` |
| C5 | (leave empty - user input) |
| A6 | `To Date (DD-MM-YYYY)` |
| C6 | (leave empty - user input) |
| A7 | `Update Trigger (TRUE/FALSE)` |
| C7 | `FALSE` |
| A9 | `INSTRUCTIONS:` |
| A10 | `1. Enter NSE symbol (e.g., RELIANCE, INFY, TCS)` |
| A11 | `2. Enter date range in DD-MM-YYYY format` |
| A12 | `3. Set trigger to TRUE to fetch data` |
| A13 | `4. Data will appear in RAW_DATA sheet` |
| A14 | `5. Charts will auto-update in DELIVERY_CHARTS` |
| A16 | `SUMMARY METRICS` |
| A17 | `Average Delivery %` |
| C17 | `=IFERROR(AVERAGE(CUSTOM_DATA!E2:E), "-")` |
| A18 | `Maximum Delivery %` |
| C18 | `=IFERROR(MAX(CUSTOM_DATA!E2:E), "-")` |
| A19 | `Minimum Delivery %` |
| C19 | `=IFERROR(MIN(CUSTOM_DATA!E2:E), "-")` |
| A20 | `Total Records` |
| C20 | `=COUNTA(CUSTOM_DATA!A2:A)` |

**Format:**
- Make row 1 bold, large font
- Make row 3, 9, 16 bold with background color
- Make cells C4-C7 have light yellow background (input cells)

**Step 4:** Setup CUSTOM_DATA

Add headers in row 1:
| A1 | B1 | C1 | D1 | E1 |
|----|----|----|----|----|
| `SYMBOL` | `Date` | `Traded Volume` | `Delivery Volume` | `Delivery %` |

In cell A2, add formula:
```
=QUERY(RAW_DATA!A:O, "SELECT A, C, K, N, O WHERE C IS NOT NULL OFFSET 1", 0)
```

Make row 1 bold.

**Step 5:** Setup RAW_DATA

Leave empty - Python will populate this.

Just add a header in A1: `Raw NSE Data` (bold)

**Step 6:** Setup SYSTEM_STATUS

Add in column A:
| A1 | B1 |
|----|-----|
| `Last Update Time` | (empty) |
| `Symbol` | (empty) |
| `Date Range` | (empty) |
| `Status` | (empty) |
| `Total Rows` | (empty) |
| `Avg Delivery %` | (empty) |
| `Max Delivery %` | (empty) |
| `Min Delivery %` | (empty) |
| `Error` | (empty) |

Make column A bold.

**Step 7:** Setup DELIVERY_CHARTS

1. Leave empty initially
2. After first data fetch, insert chart:
   - Select data range: `CUSTOM_DATA!B:E`
   - Insert → Chart
   - Chart type: Line chart
   - X-axis: Date (Column B)
   - Series: Delivery % (Column E)

**Step 8:** Share with Service Account

Same as Option A Step 2.

**Step 9:** Copy Spreadsheet ID

Same as Option A Step 3.

---

## 4. Python Installation

### Step 1: Clone/Download Project

```bash
cd /path/to/your/projects
git clone <your-repo-url>
cd nse-analytics
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed requests-2.31.0 pandas-2.1.4 gspread-5.12.0 ...
```

---

## 5. Configuration

### Step 1: Place Credentials

Move `credentials.json` to config folder:

```bash
# Your file should be at:
nse-analytics/config/credentials.json
```

### Step 2: Edit Settings

Open `config/settings.json` and update:

```json
{
  "project": {
    "name": "NSE Equity Delivery Analytics",
    "version": "1.0"
  },
  "google_sheets": {
    "spreadsheet_id": "PASTE_YOUR_SPREADSHEET_ID_HERE",
    "credentials_file": "config/credentials.json",
    "poll_interval_seconds": 5
  }
}
```

**Replace `PASTE_YOUR_SPREADSHEET_ID_HERE`** with your actual ID from step 3.

### Step 3: Verify File Structure

```
nse-analytics/
├── config/
│   ├── settings.json (edited with your spreadsheet ID)
│   └── credentials.json (downloaded from Google Cloud)
├── data/
│   └── nse_equity_list.CSV (already there)
├── logs/ (will be created)
├── modules/ (already there)
├── main.py
└── requirements.txt
```

---

## 6. First Run

### Step 1: Start the Service

```bash
# Make sure virtual environment is activated
python main.py
```

### Step 2: Expected Output

```
2026-02-08 14:30:15.123 [INFO] [main] ============================================================
2026-02-08 14:30:15.124 [INFO] [main] NSE Equity Delivery Analytics System - STARTING
2026-02-08 14:30:15.125 [INFO] [main] ============================================================
2026-02-08 14:30:15.456 [INFO] [state] Configuration loaded successfully
2026-02-08 14:30:15.457 [INFO] [state] Universal state initialized
2026-02-08 14:30:16.123 [INFO] [monitor] Connecting to Google Sheets API...
2026-02-08 14:30:17.456 [INFO] [monitor] ✅ Connected to spreadsheet: NSE Equity Delivery Analytics System
2026-02-08 14:30:17.457 [INFO] [monitor] Monitoring started (poll interval: 5s)
2026-02-08 14:30:17.458 [INFO] [main] Entering monitoring loop...
```

**If you see this:** ✅ Setup successful!

**If you see errors:** Check [Troubleshooting](#common-errors) below

---

## 7. Verification

### Step 1: Test Data Fetch

1. Open your Google Sheet
2. Go to `CUSTOM_VIEW` tab
3. Enter:
   - **C4 (Symbol):** `RELIANCE`
   - **C5 (From Date):** `01-01-2025`
   - **C6 (To Date):** `31-01-2025`
   - **C7 (Trigger):** `TRUE`

4. Watch the terminal - you should see:
```
2026-02-08 14:32:00.123 [INFO] [monitor] 🔔 Trigger detected - executing pipeline
2026-02-08 14:32:00.124 [INFO] [monitor] Trigger accepted: RELIANCE (01-01-2025 → 31-01-2025)
2026-02-08 14:32:00.456 [INFO] [nse_client] Fetching NSE data: RELIANCE (01-01-2025 → 31-01-2025)
2026-02-08 14:32:03.789 [INFO] [nse_client] CSV saved: RELIANCE_01012025_31012025.csv (3981 bytes)
2026-02-08 14:32:03.890 [INFO] [processor] Processing CSV: RELIANCE_01012025_31012025.csv
2026-02-08 14:32:03.991 [INFO] [processor] CSV processed: 20 rows | Avg Delivery: 54.23%
2026-02-08 14:32:04.092 [INFO] [processor] 🗑️  Cleaned up 0 old CSV file(s)
2026-02-08 14:32:05.456 [INFO] [sheets_io] RAW_DATA overwritten: 20 rows
2026-02-08 14:32:05.567 [INFO] [sheets_io] All sheets updated successfully
```

5. Check Google Sheet - all tabs should have data!

---

## Common Errors

### Error: "Config file not found"

**Problem:** `settings.json` not in `config/` folder

**Solution:**
```bash
# Create from template
cp config/settings.json.template config/settings.json
# Edit with your spreadsheet ID
```

### Error: "Google credentials file not found"

**Problem:** `credentials.json` not in `config/` folder or wrong path

**Solution:**
```bash
# Verify file exists
ls -la config/credentials.json

# If missing, re-download from Google Cloud Console
```

### Error: "Spreadsheet not found"

**Problem:** Service account doesn't have access or wrong ID

**Solution:**
1. Check spreadsheet ID in `config/settings.json`
2. Open your sheet → Share button
3. Add service account email as **Editor**
4. Email is in `credentials.json`: `client_email` field

### Error: "Invalid private_key format"

**Problem:** Corrupted credentials file

**Solution:**
1. Delete current `credentials.json`
2. Re-download from Google Cloud Console:
   - APIs & Services → Credentials
   - Find service account
   - Keys tab → Add Key → Create new key → JSON

### Error: "403 Forbidden" from NSE

**Problem:** NSE blocking requests

**Solution:**
- Wait 2 minutes
- Try different symbol
- Check symbol is valid on [nseindia.com](https://www.nseindia.com)

---

## Security Checklist

✅ `credentials.json` is in `config/` folder  
✅ `credentials.json` is listed in `.gitignore`  
✅ Never commit `credentials.json` to Git  
✅ Service account has minimum permissions (Sheets + Drive only)  
✅ Spreadsheet shared only with service account

---

## Next Steps

✅ Setup complete!

**Now read:** [USER_GUIDE.md](USER_GUIDE.md) for daily usage instructions

---

**Need Help?**

- Check `logs/app.log` for detailed error messages
- Review troubleshooting section in [README.md](README.md)

---

**Setup Complete! 🎉**
