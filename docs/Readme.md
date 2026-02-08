# NSE Equity Delivery Analytics System

> Automated NSE equity delivery data analysis with Google Sheets integration

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

Automatically fetch and analyze NSE equity delivery data in Google Sheets with zero manual work.

**What it does:**
1. Monitors your Google Sheet for symbol + date range input
2. Downloads historical delivery data from NSE
3. Calculates analytics (avg/min/max delivery %)
4. Updates all sheets + charts automatically

**Who it's for:**
- 📊 Traders analyzing delivery trends
- 🏢 Analysts researching patterns
- 💼 Portfolio managers monitoring holdings

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| ✅ **Auto-Fetch** | Downloads NSE data in 10-15 seconds |
| ✅ **No-Code UI** | Google Sheets interface (no programming needed) |
| ✅ **Real-Time** | Polls every 5 seconds for triggers |
| ✅ **Analytics** | Calculates avg/min/max delivery % |
| ✅ **Charts** | Auto-updating delivery trend graphs |
| ✅ **Cleanup** | Auto-deletes old CSV files |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+ ([Download](https://www.python.org/downloads/))
- Google Account (free)
- 20 minutes for setup

### Installation (3 Steps)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure (see SETUP_GUIDE.md for details)
# - Add credentials.json to config/
# - Edit config/settings.json with your spreadsheet ID

# 3. Run
python main.py
```

**First time?** Follow the complete [Setup Guide](SETUP_GUIDE.md) for Google Cloud configuration.

---

## 🔧 Installation

### Step 1: Clone Repository

```bash
git clone <your-repo-url>
cd nse-analytics
```

### Step 2: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 3: Google Cloud Setup

**Complete guide:** [SETUP_GUIDE.md](SETUP_GUIDE.md)

**Quick summary:**
1. Create Google Cloud Project
2. Enable Google Sheets API + Drive API
3. Create Service Account
4. Download `credentials.json` → place in `config/`
5. Copy template spreadsheet or create your own
6. Share sheet with service account email

### Step 4: Configure

**Edit `config/settings.json`:**

```json
{
  "google_sheets": {
    "spreadsheet_id": "PASTE_YOUR_SPREADSHEET_ID_HERE"
  }
}
```

**Find Spreadsheet ID:**
```
https://docs.google.com/spreadsheets/d/1ABC123xyz/edit
                                        ^^^^^^^^^
                                    Spreadsheet ID
```

---

## 📖 Usage

### Start the Service

```bash
python main.py
```

**Expected output:**
```
2026-02-08 14:30:17 [INFO] [monitor] ✅ Connected to spreadsheet
2026-02-08 14:30:17 [INFO] [monitor] Monitoring started (poll interval: 5s)
```

### Using Google Sheets

**1. Open your Google Sheet**

**2. Navigate to `CUSTOM_VIEW` tab**

**3. Enter:**
- **Cell C4 (Symbol):** `RELIANCE`
- **Cell C5 (From Date):** `01-01-2025`
- **Cell C6 (To Date):** `31-01-2025`
- **Cell C7 (Trigger):** `TRUE` (or check checkbox)

**4. Wait 10-15 seconds**

**5. View results:**
- `RAW_DATA` - Complete NSE data
- `CUSTOM_DATA` - Filtered columns (Date, Volumes, Delivery %)
- `DELIVERY_CHARTS` - Visual trend graph
- `SYSTEM_STATUS` - Update status

### Common Symbols

| Symbol | Company |
|--------|---------|
| `RELIANCE` | Reliance Industries |
| `TCS` | Tata Consultancy Services |
| `INFY` | Infosys |
| `HDFCBANK` | HDFC Bank |
| `ICICIBANK` | ICICI Bank |
| `BAJFINANCE` | Bajaj Finance |

**Full list:** See `data/nse_equity_list.CSV`

### Stop the Service

Press `Ctrl+C` in terminal

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[SETUP_GUIDE.md](SETUP_GUIDE.md)** | Complete installation with Google Cloud setup |
| **[USER_GUIDE.md](USER_GUIDE.md)** | Daily usage guide for end-users |

---

## 🏗️ Architecture

```
┌─────────────────────┐
│  Google Sheets (UI) │
│  User enters data   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Python Service     │
│  Monitors trigger   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  NSE API            │
│  Downloads CSV      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Google Sheets      │
│  Auto-updates       │
└─────────────────────┘
```

**Project Structure:**
```
nse-analytics/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── config/
│   ├── settings.json         # Configuration
│   └── credentials.json      # Google credentials (DO NOT COMMIT)
├── data/
│   └── nse_equity_list.CSV   # Symbol list
├── logs/
│   └── app.log               # Runtime logs
└── modules/
    ├── lifecycle.py          # Shutdown handling
    ├── monitor.py            # Sheets polling
    ├── pipeline.py           # Data pipeline
    ├── nse_client.py         # NSE API
    ├── processor.py          # Data processing
    ├── sheets_io.py          # Sheets writer
    ├── state.py              # State management
    └── utils.py              # Utilities
```

---

## 🔍 Troubleshooting

### "credentials.json not found"

**Solution:**
- Download from Google Cloud Console
- Place in `config/` folder
- Verify path: `config/credentials.json`

### "Spreadsheet not found"

**Solution:**
1. Verify spreadsheet ID in `config/settings.json`
2. Share sheet with service account email (found in credentials.json: `client_email`)
3. Give **Editor** access

### "403 Forbidden" from NSE

**Solution:**
- NSE API blocks rapid requests
- Wait 1-2 minutes and retry
- Verify symbol exists on [NSE website](https://www.nseindia.com)

### Charts not updating

**Solution:**
1. Verify `CUSTOM_DATA` sheet has data
2. Check chart range: `CUSTOM_DATA!B:E`
3. Refresh sheet (Ctrl+R / Cmd+R)

### Debug Mode

Edit `config/settings.json`:
```json
{
  "logging": {
    "level": "DEBUG"
  }
}
```

Check logs: `tail -f logs/app.log`

---

## 🚀 Deployment

### Local Machine

```bash
python main.py
```

### Background Service (Linux/Mac)

```bash
nohup python main.py > logs/app.log 2>&1 &

# Stop
pkill -f main.py
```

### Systemd Service (Linux)

Create `/etc/systemd/system/nse-analytics.service`:

```ini
[Unit]
Description=NSE Analytics Service
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/nse-analytics
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl daemon-reload
sudo systemctl enable nse-analytics
sudo systemctl start nse-analytics
```

---

## 🛡️ Security

✅ **Never commit `credentials.json`**  
✅ **Set permissions:** `chmod 400 config/credentials.json`  
✅ **Use service accounts** (not personal accounts)  
✅ **Limit permissions** to Sheets + Drive only

**`.gitignore` includes:**
```
config/credentials.json
config/settings.json
*.log
data/*.csv
__pycache__/
.venv/
```

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Poll Interval | 5 seconds |
| Data Fetch | 2-5 seconds |
| Processing | <1 second |
| Sheets Update | 2-3 seconds |
| **Total** | **10-15 seconds** |
| Memory | <100 MB |
| CPU (idle) | <5% |

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 💡 Tips

1. **Start with 1-month range** - Test with smaller datasets
2. **Verify symbols** - Check NSE website for correct names
3. **Monitor logs** - Keep `logs/app.log` open during first runs
4. **Use formulas** - Let Google Sheets calculate metrics (not Python)

---

**Made with ❤️ for traders and analysts**

**Quick Links:**  
📖 [Setup Guide](SETUP_GUIDE.md) | 
👤 [User Guide](USER_GUIDE.md)

---

**© 2026 NSE Analytics Project**
