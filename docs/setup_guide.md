# NSE Equity Delivery Analytics System
## Complete Setup Guide

**Version:** 1.0  
**Date:** February 8, 2026  
**Estimated Setup Time:** 30-45 minutes

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Google Cloud Setup](#2-google-cloud-setup)
3. [Google Sheets Preparation](#3-google-sheets-preparation)
4. [System Installation](#4-system-installation)
5. [Configuration](#5-configuration)
6. [First Run](#6-first-run)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Prerequisites

### 1.1 Required Accounts

- **Google Account:** Free Gmail account
- **System Requirements:**
  - Python 3.9 or higher
  - 100 MB free disk space
  - Stable internet connection

### 1.2 Check Python Installation

**Windows:**
```cmd
python --version
```

**macOS/Linux:**
```bash
python3 --version
```

Expected output: `Python 3.9.x` or higher

**If Python is not installed:**

- **Windows:** Download from [python.org](https://www.python.org/downloads/)
- **macOS:** `brew install python3`
- **Linux:** `sudo apt install python3 python3-pip`

---

## 2. Google Cloud Setup

This section will guide you through creating a Google Cloud project and obtaining credentials.

### 2.1 Create Google Cloud Project

**Step 1:** Go to Google Cloud Console
- Visit: https://console.cloud.google.com/
- Sign in with your Google account

**Step 2:** Create New Project
1. Click the project dropdown at the top of the page
2. Click **"NEW PROJECT"**
3. Enter project name: `NSE-Analytics` (or any name you prefer)
4. Click **"CREATE"**
5. Wait for project creation (10-20 seconds)
6. Select your new project from the dropdown

![Project Creation](https://i.imgur.com/example.png)

---

### 2.2 Enable Required APIs

You need to enable **two APIs**: Google Sheets API and Google Drive API.

**Step 1:** Enable Google Sheets API

1. In the Google Cloud Console, click the hamburger menu (☰) → **"APIs & Services"** → **"Library"**
2. Search for: `Google Sheets API`
3. Click on **"Google Sheets API"** in the results
4. Click **"ENABLE"** button
5. Wait for confirmation (appears immediately)

**Step 2:** Enable Google Drive API

1. Click **"API Library"** again (or press back button)
2. Search for: `Google Drive API`
3. Click on **"Google Drive API"** in the results
4. Click **"ENABLE"** button
5. Wait for confirmation

**Verification:**
- Go to **"APIs & Services"** → **"Dashboard"**
- You should see both APIs listed under "Enabled APIs & services"

---

### 2.3 Create Service Account

A service account allows the Python script to access Google Sheets without requiring you to log in manually.

**Step 1:** Navigate to Service Accounts

1. Click hamburger menu (☰) → **"APIs & Services"** → **"Credentials"**
2. Click **"+ CREATE CREDENTIALS"** at the top
3. Select **"Service Account"**

**Step 2:** Service Account Details

1. **Service account name:** `nse-analytics-service`
2. **Service account ID:** (auto-filled, leave as is)
3. **Description:** `Service account for NSE delivery analytics system`
4. Click **"CREATE AND CONTINUE"**

**Step 3:** Grant Permissions (Optional - Skip This)

1. On "Grant this service account access to project" screen
2. Click **"CONTINUE"** (no need to add roles)

**Step 4:** Grant User Access (Optional - Skip This)

1. On "Grant users access to this service account" screen
2. Click **"DONE"**

**Result:** You should now see your service account listed under "Service Accounts"

---

### 2.4 Create and Download Credentials JSON

**Step 1:** Create Key

1. In the Service Accounts list, find `nse-analytics-service@...`
2. Click on the **email address** (the service account itself)
3. Go to the **"KEYS"** tab
4. Click **"ADD KEY"** → **"Create new key"**

**Step 2:** Choose Key Type

1. Select **"JSON"** (should be selected by default)
2. Click **"CREATE"**

**Step 3:** Download

- A JSON file will automatically download to your computer
- File name format: `nse-analytics-xxxxxx-xxxxxxxxxxxxx.json`
- **IMPORTANT:** Keep this file safe and never share it publicly!

**Step 4:** Rename the File

- Rename the downloaded file to: `credentials.json`
- Move it to a safe location (you'll use it later)

---

### 2.5 Copy Service Account Email

**CRITICAL STEP:** You need the service account email to share the Google Sheet.

1. In the Service Accounts page, find your service account
2. Copy the email address (looks like: `nse-analytics-service@nse-analytics-xxxxxx.iam.gserviceaccount.com`)
3. **Save this email somewhere** - you'll need it in the next section

**Example Email Format:**
```
nse-analytics-service@nse-analytics-123456.iam.gserviceaccount.com
```

---

## 3. Google Sheets Preparation

### 3.1 Create Google Sheet from Template

**Option A: Create New Spreadsheet**

1. Go to https://sheets.google.com
2. Click **"+ Blank"** to create new spreadsheet
3. Rename it to: `NSE Delivery Analytics`

**Step-by-Step Sheet Setup:**

**Create Sheet 1: RAW_DATA**

1. Click on "Sheet1" tab at bottom
2. Right-click → Rename to: `RAW_DATA`
3. Add headers in Row 1:
   - A1: `Symbol`
   - B1: `Date`
   - C1: `Open`
   - D1: `High`
   - E1: `Low`
   - F1: `Close`
   - G1: `Total Qty`
   - H1: `Deliverable Qty`
   - I1: `Delivery %`
   - J1: `Turnover`
   - K1: `Trades`

**Create Sheet 2: CUSTOM_VIEW**

1. Click **"+"** button at bottom to add new sheet
2. Rename to: `CUSTOM_VIEW`
3. Set up input controls:

```
     A                    B                 C              D
1    Symbol:             [blank cell]      Avg Delivery:  =AVERAGE(FILTER(RAW_DATA!I:I,RAW_DATA!I:I>0))
2    From Date:          [blank cell]      Max Delivery:  =MAX(FILTER(RAW_DATA!I:I,RAW_DATA!I:I>0))
3    To Date:            [blank cell]      Min Delivery:  =MIN(FILTER(RAW_DATA!I:I,RAW_DATA!I:I>0))
4    Update Trigger:     FALSE
5
6    --- Filtered Data Below ---
7    (Headers will appear here after first data load)
```

**Format the trigger cell (B4):**
1. Click cell B4
2. Go to **Insert** → **Checkbox**
3. This creates a checkbox that toggles between TRUE/FALSE

**Create Sheet 3: DELIVERY_CHARTS**

1. Add new sheet, rename to: `DELIVERY_CHARTS`
2. Add title in A1: `Delivery Analytics Charts`
3. **We'll add charts after first data load**

**Create Sheet 4: SYSTEM_STATUS**

1. Add new sheet, rename to: `SYSTEM_STATUS`
2. Add headers:

```
     A                          B
1    Metric                     Value
2    Last Update Time           (Will be auto-filled)
3    Symbol                     (Will be auto-filled)
4    Date Range                 (Will be auto-filled)
5    Pipeline Status            (Will be auto-filled)
6    Total Records              (Will be auto-filled)
7    Average Delivery %         (Will be auto-filled)
8    Max Delivery %             (Will be auto-filled)
9    Min Delivery %             (Will be auto-filled)
10   Execution Time (sec)       (Will be auto-filled)
11   Last Error                 (Will be auto-filled)
```

---

### 3.2 Share Sheet with Service Account

**CRITICAL:** Without this step, the Python script cannot access your sheet!

**Step 1:** Click "Share" Button

1. Click the blue **"Share"** button in top-right corner of Google Sheets

**Step 2:** Add Service Account Email

1. In the "Add people and groups" field
2. Paste the service account email you copied earlier
   - Example: `nse-analytics-service@nse-analytics-123456.iam.gserviceaccount.com`
3. Press Enter or click the email suggestion

**Step 3:** Set Permissions

1. In the dropdown next to the email, select **"Editor"**
2. **UNCHECK** "Notify people" (no need to send email to service account)
3. Click **"Share"** or **"Done"**

**Verification:**
- The service account email should appear in the "Share" dialog
- Permission should show "Editor"

---

### 3.3 Copy Spreadsheet ID

You need the Spreadsheet ID for configuration.

**Where to Find It:**

Look at the URL of your Google Sheet:
```
https://docs.google.com/spreadsheets/d/1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t/edit
                                        ↑________________________________↑
                                        This is your Spreadsheet ID
```

**Example:**
- URL: `https://docs.google.com/spreadsheets/d/1ABC-XYZ123_example-ID/edit#gid=0`
- Spreadsheet ID: `1ABC-XYZ123_example-ID`

**Copy this ID** - you'll need it for configuration!

---

## 4. System Installation

### 4.1 Download the Project

**Option A: Download ZIP**

1. Download the project ZIP file
2. Extract to a location like:
   - Windows: `C:\Users\YourName\nse-analytics`
   - macOS/Linux: `/home/username/nse-analytics`

**Option B: Git Clone (if you have Git)**

```bash
git clone https://github.com/your-repo/nse-analytics.git
cd nse-analytics
```

---

### 4.2 Project Structure Verification

After extraction, your folder should look like:

```
nse-analytics/
├── main.py
├── requirements.txt
├── README.md
├── config/
│   ├── settings.yaml
│   └── logging_config.yaml
├── modules/
│   ├── __init__.py
│   ├── nse_fetcher.py
│   ├── sheets_reader.py
│   ├── sheets_writer.py
│   ├── data_processor.py
│   └── utils.py
├── data/
│   └── .gitkeep
└── logs/
    └── .gitkeep
```

---

### 4.3 Install Python Dependencies

**Windows:**

```cmd
cd C:\Users\YourName\nse-analytics
python -m pip install -r requirements.txt
```

**macOS/Linux:**

```bash
cd /home/username/nse-analytics
pip3 install -r requirements.txt
```

**Expected Output:**
```
Collecting requests==2.31.0
Collecting pandas==2.1.4
Collecting gspread==5.12.0
...
Successfully installed requests-2.31.0 pandas-2.1.4 ...
```

**If you get permission errors:**

```bash
pip3 install --user -r requirements.txt
```

---

### 4.4 Place Credentials File

**Step 1:** Locate your `credentials.json` file (downloaded from Google Cloud)

**Step 2:** Copy it to the config folder:

**Windows:**
```cmd
copy C:\Users\YourName\Downloads\credentials.json C:\Users\YourName\nse-analytics\config\
```

**macOS/Linux:**
```bash
cp ~/Downloads/credentials.json ~/nse-analytics/config/
```

**Step 3:** Verify the file is in place:

**Windows:**
```cmd
dir config\credentials.json
```

**macOS/Linux:**
```bash
ls -la config/credentials.json
```

You should see the file listed.

---

## 5. Configuration

### 5.1 Edit settings.yaml

**Open the file:**
- Windows: Use Notepad or Notepad++
- macOS: Use TextEdit or VS Code
- Linux: Use nano, vim, or any text editor

**File location:** `config/settings.yaml`

**Step 1:** Update Spreadsheet ID

Find this line:
```yaml
spreadsheet_id: "YOUR_SPREADSHEET_ID_HERE"
```

Replace with your actual Spreadsheet ID:
```yaml
spreadsheet_id: "1ABC-XYZ123_example-ID"
```

**Step 2:** Verify Other Settings (Usually No Changes Needed)

```yaml
# NSE API Configuration
nse:
  base_url: "https://www.nseindia.com"
  api_endpoint: "/api/historical/cm/equity"
  homepage_url: "https://www.nseindia.com"
  timeout_seconds: 20
  max_retries: 3
  retry_delay_seconds: 2

# Google Sheets Configuration
google_sheets:
  credentials_file: "config/credentials.json"
  spreadsheet_id: "1ABC-XYZ123_example-ID"  # ← YOUR ID HERE
  poll_interval_seconds: 5
  
  sheet_names:
    raw_data: "RAW_DATA"
    custom_view: "CUSTOM_VIEW"
    charts: "DELIVERY_CHARTS"
    system_status: "SYSTEM_STATUS"
  
  control_cells:
    symbol: "B1"
    from_date: "B2"
    to_date: "B3"
    trigger: "B4"

# Data Storage
data:
  folder: "data"
  cleanup_enabled: true
  max_age_hours: 24

# Logging
logging:
  config_file: "config/logging_config.yaml"
```

**Step 3:** Save the file

---

### 5.2 Verify Logging Configuration

The file `config/logging_config.yaml` should already be configured correctly. 

**Quick Check:** Open `config/logging_config.yaml` and verify these folders exist:

```yaml
handlers:
  app_file:
    filename: logs/app.log  # ← 'logs' folder must exist
```

**Create logs folder if missing:**

**Windows:**
```cmd
mkdir logs
```

**macOS/Linux:**
```bash
mkdir -p logs
```

---

## 6. First Run

### 6.1 Test the Installation

**Run the application:**

**Windows:**
```cmd
python main.py
```

**macOS/Linux:**
```bash
python3 main.py
```

**Expected Output:**

```
2026-02-08 10:30:15.123 [INFO] [main] Application started
2026-02-08 10:30:15.234 [INFO] [utils] Logging initialized
2026-02-08 10:30:15.345 [INFO] [utils] Configuration loaded
2026-02-08 10:30:16.456 [INFO] [sheets_reader] Authenticated with Google Sheets
2026-02-08 10:30:16.567 [INFO] [sheets_reader] Monitoring started for sheet: NSE Delivery Analytics
2026-02-08 10:30:16.678 [INFO] [sheets_reader] Polling every 5 seconds. Press Ctrl+C to stop.
```

**If you see these logs, congratulations! Setup is successful! 🎉**

---

### 6.2 First Data Fetch Test

**Step 1:** Go to your Google Sheet (CUSTOM_VIEW tab)

**Step 2:** Enter test data:

- B1 (Symbol): `INFY`
- B2 (From Date): `01-01-2025`
- B3 (To Date): `31-01-2025`
- B4 (Trigger): **Check the box** (or type `TRUE`)

**Step 3:** Wait and Watch

Within 5-10 seconds, you should see in the terminal:

```
2026-02-08 10:31:15.123 [INFO] [sheets_reader] Trigger detected: INFY, 01-01-2025 to 31-01-2025
2026-02-08 10:31:15.234 [INFO] [nse_fetcher] Fetching data for INFY
2026-02-08 10:31:18.345 [INFO] [data_processor] Processing 21 rows
2026-02-08 10:31:20.456 [INFO] [sheets_writer] Updated all sheets successfully
2026-02-08 10:31:20.567 [INFO] [utils] Cleaned up 0 old CSV files
```

**Step 4:** Check Google Sheets

1. **RAW_DATA sheet:** Should now contain 21 rows of data
2. **CUSTOM_VIEW sheet:** Checkbox should be unchecked (reset to FALSE)
3. **SYSTEM_STATUS sheet:** Should show "Success" and metrics
4. **DELIVERY_CHARTS sheet:** Will add charts manually (next section)

---

### 6.3 Add Charts (One-Time Setup)

**Chart 1: Delivery % Over Time**

1. Go to **DELIVERY_CHARTS** sheet
2. Click **Insert** → **Chart**
3. In Chart Editor:
   - **Chart type:** Line chart
   - **Data range:** `RAW_DATA!B2:B` (Dates) and `RAW_DATA!I2:I` (Delivery %)
   - **X-axis:** Date
   - **Y-axis:** Delivery %
   - **Title:** "Delivery Percentage Trend"
4. Click **Insert**

**Chart 2: Volume vs Delivery (Combo Chart)**

1. Click **Insert** → **Chart**
2. In Chart Editor:
   - **Chart type:** Combo chart
   - **Data range:** 
     - `RAW_DATA!B2:B` (Dates)
     - `RAW_DATA!G2:G` (Volume - as bars)
     - `RAW_DATA!I2:I` (Delivery % - as line)
   - **Left Y-axis:** Volume
   - **Right Y-axis:** Delivery %
   - **Title:** "Volume vs Delivery Analysis"
3. Click **Insert**

**Done!** Charts will auto-update whenever new data is loaded.

---

## 7. Troubleshooting

### 7.1 Common Installation Issues

#### Issue: "Python not found"

**Solution:**
- Install Python 3.9+ from python.org
- Add Python to PATH during installation
- Restart terminal after installation

#### Issue: "pip install fails with permission error"

**Solution:**
```bash
pip3 install --user -r requirements.txt
```

#### Issue: "Module not found" errors when running

**Solution:**
- Ensure you're in the project directory
- Re-run: `pip3 install -r requirements.txt`
- Check Python version: `python3 --version`

---

### 7.2 Google Sheets Connection Issues

#### Issue: "Unable to authenticate with Google Sheets"

**Possible Causes & Solutions:**

1. **credentials.json not found**
   - Verify file exists: `ls config/credentials.json`
   - Check file permissions (should be readable)

2. **Invalid credentials.json format**
   - Re-download from Google Cloud Console
   - Ensure it's the JSON key (not OAuth client ID)

3. **API not enabled**
   - Go to Google Cloud Console → APIs & Services
   - Verify both Google Sheets API and Google Drive API are enabled

#### Issue: "Permission denied" when accessing sheet

**Solution:**
- Verify sheet is shared with service account email
- Service account must have "Editor" permissions
- Check spelling of service account email

---

### 7.3 NSE API Issues

#### Issue: "403 Forbidden" error from NSE

**Solution:**
- NSE blocks frequent requests from same IP
- Wait 5-10 minutes and try again
- Check if NSE website is accessible: https://www.nseindia.com

#### Issue: "Invalid symbol" error

**Solution:**
- Use exact NSE symbol (all caps): `RELIANCE`, `INFY`, `TCS`
- Check symbol exists: https://www.nseindia.com/market-data/live-equity-market
- Do not add exchange prefix (e.g., use `INFY` not `NSE:INFY`)

#### Issue: "No data found for date range"

**Solution:**
- NSE only has data for trading days (not weekends/holidays)
- Ensure date range is within last 1 year
- Use DD-MM-YYYY format: `01-01-2025`, not `1/1/2025`

---

### 7.4 Data Not Appearing in Sheets

#### Issue: Trigger checkbox doesn't work

**Solution:**

1. Verify checkbox is in cell B4 of CUSTOM_VIEW sheet
2. Check settings.yaml has correct cell reference:
   ```yaml
   control_cells:
     trigger: "B4"
   ```
3. Try manually typing `TRUE` in B4 instead of using checkbox

#### Issue: Data appears in RAW_DATA but not CUSTOM_VIEW

**Solution:**
- CUSTOM_VIEW uses formulas to filter RAW_DATA
- Verify formulas are present (see section 3.1)
- Manually refresh: Ctrl+R (Windows) or Cmd+R (Mac)

---

### 7.5 Log Analysis

**Check application logs:**

**Windows:**
```cmd
type logs\app.log
```

**macOS/Linux:**
```bash
tail -f logs/app.log
```

**Common log messages and meanings:**

| Log Message | Meaning | Action |
|-------------|---------|--------|
| "Trigger detected" | User clicked update button | Normal operation |
| "NSEFetchError: 403" | NSE blocked request | Wait 5 minutes, retry |
| "Invalid symbol format" | Symbol validation failed | Check symbol spelling |
| "Permission denied" | Sheet not shared with service account | Share sheet with service account |
| "Spreadsheet not found" | Wrong spreadsheet ID | Check settings.yaml |

---

### 7.6 Getting Help

**Before asking for help, collect:**

1. **System info:**
   - Operating system
   - Python version: `python3 --version`
   
2. **Error logs:**
   - Last 50 lines of app.log
   - Screenshot of error message

3. **Configuration:**
   - Spreadsheet ID (from settings.yaml)
   - Service account email
   - Verify credentials.json exists

4. **Steps to reproduce:**
   - What you entered in Google Sheet
   - What you expected vs what happened

**Support Channels:**
- GitHub Issues (if using repository)
- Email: support@yourcompany.com
- Documentation: Link to full docs

---

## 8. Running as a Service

### 8.1 Keep Application Running (Windows)

**Option A: Background Process**

Create a batch file `start_nse_analytics.bat`:

```batch
@echo off
cd C:\Users\YourName\nse-analytics
start /B python main.py > logs\app.log 2>&1
```

Run this batch file to start in background.

**Option B: Task Scheduler**

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: At startup
4. Action: Start a program
   - Program: `python`
   - Arguments: `main.py`
   - Start in: `C:\Users\YourName\nse-analytics`

---

### 8.2 Keep Application Running (macOS/Linux)

**Option A: systemd (Linux)**

Create `/etc/systemd/system/nse-analytics.service`:

```ini
[Unit]
Description=NSE Analytics Service
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/home/yourusername/nse-analytics
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable nse-analytics
sudo systemctl start nse-analytics
sudo systemctl status nse-analytics
```

**Option B: nohup (macOS/Linux)**

```bash
cd /home/username/nse-analytics
nohup python3 main.py > logs/app.log 2>&1 &
```

To stop:
```bash
ps aux | grep main.py
kill <PID>
```

---

## 9. Daily Usage

### 9.1 Normal Workflow

1. **Open Google Sheet** → Go to CUSTOM_VIEW tab
2. **Enter symbol** (e.g., `RELIANCE`)
3. **Enter dates** (e.g., `01-02-2026` to `07-02-2026`)
4. **Check trigger box** (or type `TRUE`)
5. **Wait 10-30 seconds**
6. **View results:**
   - RAW_DATA: Complete dataset
   - CUSTOM_VIEW: Filtered view
   - DELIVERY_CHARTS: Visual trends
   - SYSTEM_STATUS: Success confirmation

---

### 9.2 Multiple Queries Per Day

**Yes, you can!** The system supports unlimited queries.

**Tips:**
- Wait for previous query to complete before triggering next
- NSE may rate-limit if you make 10+ requests per minute
- Each query refreshes all data (doesn't append)

---

### 9.3 Switching Symbols

**To analyze a different symbol:**

1. Go to CUSTOM_VIEW sheet
2. Change B1 to new symbol (e.g., `TCS`)
3. Update dates if needed
4. Check trigger box
5. Previous data in RAW_DATA will be replaced with new symbol's data

---

## 10. Maintenance

### 10.1 Log Cleanup

Logs auto-rotate at 10MB. To manually clean:

**Windows:**
```cmd
del logs\*.log
```

**macOS/Linux:**
```bash
rm logs/*.log
```

---

### 10.2 CSV Cleanup

CSVs auto-delete after 24 hours. To manually clean:

**Windows:**
```cmd
del data\*.csv
```

**macOS/Linux:**
```bash
rm data/*.csv
```

---

### 10.3 Updating the Application

**When new version is released:**

1. **Stop the application:** Press Ctrl+C
2. **Backup your config:**
   ```bash
   cp config/settings.yaml config/settings.yaml.backup
   cp config/credentials.json config/credentials.json.backup
   ```
3. **Download new version** and extract
4. **Restore your config:**
   ```bash
   cp config/settings.yaml.backup config/settings.yaml
   cp config/credentials.json.backup config/credentials.json
   ```
5. **Reinstall dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```
6. **Restart application:**
   ```bash
   python3 main.py
   ```

---

## 11. Advanced Configuration

### 11.1 Changing Poll Interval

Default: Check for trigger every 5 seconds

**To change to 10 seconds:**

Edit `config/settings.yaml`:
```yaml
google_sheets:
  poll_interval_seconds: 10  # Changed from 5
```

**Note:** Longer intervals = less responsive, but lower API usage

---

### 11.2 Changing Data Retention

Default: Delete CSVs after 24 hours

**To keep for 48 hours:**

Edit `config/settings.yaml`:
```yaml
data:
  max_age_hours: 48  # Changed from 24
```

**To disable auto-cleanup:**
```yaml
data:
  cleanup_enabled: false
```

---

### 11.3 Custom Sheet Names

If you renamed your sheets, update `config/settings.yaml`:

```yaml
google_sheets:
  sheet_names:
    raw_data: "YOUR_RAW_DATA_SHEET_NAME"
    custom_view: "YOUR_CUSTOM_VIEW_SHEET_NAME"
    charts: "YOUR_CHARTS_SHEET_NAME"
    system_status: "YOUR_STATUS_SHEET_NAME"
```

---

## 12. Security Best Practices

### 12.1 Protect credentials.json

**Never:**
- Share credentials.json with anyone
- Upload to GitHub or public repositories
- Email or message credentials.json

**Always:**
- Keep in the `config/` folder
- Set file permissions to read-only
- Backup securely if needed

**Set read-only permissions:**

**Windows:**
```cmd
attrib +R config\credentials.json
```

**macOS/Linux:**
```bash
chmod 400 config/credentials.json
```

---

### 12.2 Regenerate Credentials (If Compromised)

**If credentials.json is exposed:**

1. Go to Google Cloud Console
2. Navigate to service account
3. Go to "KEYS" tab
4. Delete old key
5. Create new key
6. Download new credentials.json
7. Replace old file in `config/` folder
8. Restart application

---

## 13. Uninstallation

**To completely remove the application:**

### 13.1 Stop the Service

**Windows:**
- Close the command prompt window
- Or: Kill process in Task Manager

**macOS/Linux:**
```bash
# If running with systemd
sudo systemctl stop nse-analytics
sudo systemctl disable nse-analytics
sudo rm /etc/systemd/system/nse-analytics.service

# If running with nohup
kill <PID>
```

### 13.2 Delete Files

**Windows:**
```cmd
rmdir /S C:\Users\YourName\nse-analytics
```

**macOS/Linux:**
```bash
rm -rf /home/username/nse-analytics
```

### 13.3 Revoke Google Sheets Access

1. Go to Google Sheet
2. Click "Share"
3. Find service account email
4. Click "Remove"

### 13.4 Delete Google Cloud Project (Optional)

1. Go to Google Cloud Console
2. Select the project
3. Go to "Settings"
4. Click "Shut down"
5. Confirm project deletion

---

## 14. Frequently Asked Questions (FAQ)

**Q: Do I need to keep my computer on 24/7?**

A: No, but the application only works when running. If your computer is off, the monitoring stops. Consider cloud deployment for 24/7 operation.

---

**Q: Can multiple people use the same Google Sheet?**

A: Yes! Share the Google Sheet with colleagues. Only one instance of the Python service should be running.

---

**Q: Can I analyze multiple symbols at once?**

A: Currently, one symbol at a time. The system replaces data on each query. Future versions may support multiple symbols.

---

**Q: What happens if NSE API is down?**

A: The system will retry 3 times with exponential backoff. If still failing, an error will be logged and shown in SYSTEM_STATUS sheet.

---

**Q: Can I use this for F&O data?**

A: No, current version supports equity (cash) segment only. F&O support may be added in future.

---

**Q: How much does this cost?**

A: Free! Google Cloud services (Sheets + Drive APIs) have generous free tiers. NSE data is public and free.

---

**Q: Can I export data to Excel?**

A: Yes! In Google Sheets, go to File → Download → Microsoft Excel (.xlsx)

---

**Q: Is my data private?**

A: Yes. Data stays in your Google Sheet. The Python service runs on your machine. No data is sent to external servers (except NSE API for fetching).

---

## 15. Next Steps

### Congratulations! 🎉

You've successfully set up the NSE Equity Delivery Analytics System.

**Recommended Next Steps:**

1. ✅ Test with different symbols (RELIANCE, TCS, HDFC, etc.)
2. ✅ Experiment with different date ranges
3. ✅ Customize charts in DELIVERY_CHARTS sheet
4. ✅ Set up as a service for continuous operation
5. ✅ Share Google Sheet with team members

**Advanced Users:**
- Explore the code in `modules/` folder
- Add custom analytics formulas in CUSTOM_VIEW
- Contribute improvements on GitHub

---

**Need Help?**
- Check [Troubleshooting](#7-troubleshooting) section
- Review logs in `logs/app.log`
- Open GitHub issue (if using repository)

**Happy Analyzing! 📊**

---

**End of Setup Guide**