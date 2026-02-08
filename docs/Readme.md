# NSE Equity Delivery Analytics System

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

> Automated NSE equity delivery data analysis with Google Sheets integration

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

---

## 🎯 Overview

The **NSE Equity Delivery Analytics System** is a Python-based automation tool that fetches historical delivery data from the National Stock Exchange of India (NSE) and presents it in an interactive Google Sheets dashboard.

### What It Does

- **Monitors** Google Sheets for user input (symbol + date range)
- **Fetches** historical delivery data from NSE API
- **Processes** CSV data and calculates metrics
- **Updates** Google Sheets with analyzed data
- **Visualizes** trends through automated charts

### Who It's For

- 📊 Retail traders analyzing delivery trends
- 🏢 Analysts researching delivery patterns
- 💼 Portfolio managers monitoring holdings
- 📈 Anyone interested in NSE equity delivery data

---

## ✨ Features

### Core Capabilities

- ✅ **Automated Data Fetching**: Download historical NSE data on-demand
- ✅ **Google Sheets Integration**: No-code interface for non-technical users
- ✅ **Real-time Monitoring**: Polls Google Sheets every 5 seconds
- ✅ **Data Processing**: Validates, cleans, and calculates delivery metrics
- ✅ **Visual Analytics**: Auto-updating charts for trend analysis
- ✅ **System Health Monitoring**: Track operation status and errors
- ✅ **Logging**: Comprehensive logging for debugging and audit

### Data Metrics

| Category | Metrics |
|----------|---------|
| **Price** | Open, High, Low, Close, VWAP |
| **Volume** | Total Traded Quantity, Turnover, Number of Trades |
| **Delivery** | Deliverable Quantity, Delivery Percentage |
| **Derived** | Avg/Max/Min Delivery %, Trend Analysis |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Google account
- 100 MB disk space
- Stable internet connection

### Installation (5 Minutes)

```bash
# 1. Clone repository
git clone https://github.com/your-repo/nse-analytics.git
cd nse-analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure
# - Add credentials.json to config/
# - Edit config/settings.yaml with your Spreadsheet ID

# 4. Run
python main.py
```

**Detailed setup instructions**: See [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[SETUP_GUIDE.md](SETUP_GUIDE.md)** | Complete installation and Google Cloud setup |
| **[USER_GUIDE.md](USER_GUIDE.md)** | End-user guide for daily usage |
| **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** | High-level project description |
| **[MODULAR_DESIGN.md](MODULAR_DESIGN.md)** | Architecture and module specifications |
| **[TECHNICAL_IMPLEMENTATION.md](TECHNICAL_IMPLEMENTATION.md)** | Developer-focused technical details |

---

## 💻 System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 10+, macOS 10.14+, Ubuntu 20.04+ |
| **Python** | 3.9 or higher |
| **RAM** | 512 MB available |
| **Storage** | 100 MB free space |
| **Network** | Stable internet (for NSE API and Google Sheets) |

### Dependencies

```txt
requests==2.31.0        # HTTP client for NSE API
pandas==2.1.4           # Data processing
gspread==5.12.0         # Google Sheets API
oauth2client==4.1.3     # Google authentication
PyYAML==6.0.1           # Configuration management
python-dateutil==2.8.2  # Date parsing
```

---

## 🔧 Installation

### Step 1: Google Cloud Setup

**Enable APIs:**
1. Google Sheets API
2. Google Drive API

**Create Service Account:**
1. Go to Google Cloud Console
2. Create service account
3. Download `credentials.json`
4. Place in `config/` folder

**Detailed instructions**: [SETUP_GUIDE.md](SETUP_GUIDE.md#2-google-cloud-setup)

---

### Step 2: Google Sheets Preparation

**Create Spreadsheet with 4 sheets:**
1. `RAW_DATA` - Complete data dump
2. `CUSTOM_VIEW` - User interface and filtered view
3. `DELIVERY_CHARTS` - Visual analytics
4. `SYSTEM_STATUS` - Health monitoring

**Share with service account email**

**Detailed instructions**: [SETUP_GUIDE.md](SETUP_GUIDE.md#3-google-sheets-preparation)

---

### Step 3: Python Installation

```bash
# Clone repository
git clone https://github.com/your-repo/nse-analytics.git
cd nse-analytics

# Install dependencies
pip install -r requirements.txt

# Verify installation
python --version  # Should show Python 3.9+
```

---

### Step 4: Configuration

**Edit `config/settings.yaml`:**

```yaml
google_sheets:
  spreadsheet_id: "YOUR_SPREADSHEET_ID_HERE"  # ← Update this
  credentials_file: "config/credentials.json"
  poll_interval_seconds: 5
```

**Place credentials:**
```bash
# Copy downloaded credentials.json to config folder
cp ~/Downloads/credentials.json config/
```

---

## ⚙️ Configuration

### settings.yaml

```yaml
# NSE API Configuration
nse:
  base_url: "https://www.nseindia.com"
  timeout_seconds: 20
  max_retries: 3

# Google Sheets Configuration
google_sheets:
  spreadsheet_id: "YOUR_SPREADSHEET_ID"
  poll_interval_seconds: 5
  
  sheet_names:
    raw_data: "RAW_DATA"
    custom_view: "CUSTOM_VIEW"
    charts: "DELIVERY_CHARTS"
    system_status: "SYSTEM_STATUS"

# Data Storage
data:
  folder: "data"
  cleanup_enabled: true
  max_age_hours: 24
```

### Environment Variables (Optional)

```bash
export SPREADSHEET_ID="your-spreadsheet-id"
export CREDENTIALS_PATH="config/credentials.json"
```

---

## 📖 Usage

### Basic Usage

**1. Start the service:**
```bash
python main.py
```

**2. In Google Sheets (CUSTOM_VIEW tab):**
- Enter Symbol: `INFY`
- From Date: `01-01-2026`
- To Date: `31-01-2026`
- Check the trigger box

**3. Wait 10-30 seconds**

**4. View results in all sheets**

### Advanced Usage

**Run as background service (Linux/Mac):**
```bash
nohup python main.py > logs/app.log 2>&1 &
```

**Run as systemd service:**
```bash
sudo systemctl start nse-analytics
sudo systemctl status nse-analytics
```

**Docker deployment:**
```bash
docker-compose up -d
```

**Detailed usage**: [USER_GUIDE.md](USER_GUIDE.md)

---

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────┐
│                    Google Sheets                        │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │ CUSTOM_VIEW │  │ DELIVERY_    │  │ SYSTEM_STATUS  │ │
│  │ (Input)     │  │ CHARTS       │  │ (Health)       │ │
│  └─────────────┘  └──────────────┘  └────────────────┘ │
└────────────┬────────────────────────────────────────────┘
             │ (Trigger Detection)
             ▼
┌─────────────────────────────────────────────────────────┐
│              Python Monitoring Service                   │
│  ┌──────────────────────────────────────────────────┐   │
│  │ main.py  → Orchestrator                          │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Modules:                                         │   │
│  │  • sheets_reader   → Read inputs, monitor trigger│   │
│  │  • nse_fetcher     → Download NSE data          │   │
│  │  • data_processor  → Parse & validate CSV       │   │
│  │  • sheets_writer   → Update all sheets          │   │
│  │  • utils           → Common functions           │   │
│  └──────────────────────────────────────────────────┘   │
└────────────┬────────────────────────────────────────────┘
             │ (Data Fetch)
             ▼
┌─────────────────────────────────────────────────────────┐
│                      NSE API                             │
│  https://www.nseindia.com/api/historical/cm/equity      │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Input** → Google Sheets (CUSTOM_VIEW)
2. **Trigger Detection** → Python polls every 5 seconds
3. **Input Validation** → Symbol, date format check
4. **NSE API Call** → Download historical CSV
5. **Data Processing** → Parse, validate, calculate metrics
6. **Sheets Update** → Write to all 4 sheets atomically
7. **Status Update** → Log success/failure in SYSTEM_STATUS

---

## 📂 Project Structure

```
nse-delivery-analytics/
│
├── main.py                          # Entry point (orchestrator)
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── LICENSE                          # MIT License
├── .gitignore                       # Git exclusions
│
├── config/                          # Configuration files
│   ├── settings.yaml                # Application settings
│   ├── credentials.json             # Google service account (gitignored)
│   └── logging_config.yaml          # Logging configuration
│
├── modules/                         # Core business logic
│   ├── __init__.py
│   ├── nse_fetcher.py               # NSE API interaction
│   ├── sheets_reader.py             # Google Sheets reading
│   ├── sheets_writer.py             # Google Sheets writing
│   ├── data_processor.py            # CSV processing
│   └── utils.py                     # Shared utilities
│
├── data/                            # Temporary CSV storage
│   └── .gitkeep                     # (CSV files auto-deleted)
│
├── logs/                            # Application logs
│   ├── app.log                      # Main log
│   ├── nse_api.log                  # NSE operations
│   └── sheets.log                   # Sheets operations
│
└── docs/                            # Documentation
    ├── SETUP_GUIDE.md
    ├── USER_GUIDE.md
    ├── PROJECT_OVERVIEW.md
    ├── MODULAR_DESIGN.md
    └── TECHNICAL_IMPLEMENTATION.md
```

---

## 🔍 Troubleshooting

### Common Issues

#### 1. "Unable to authenticate with Google Sheets"

**Cause:** Missing or invalid credentials

**Solution:**
- Verify `config/credentials.json` exists
- Check Google Sheets API is enabled
- Ensure Google Drive API is enabled (required since 2024)

---

#### 2. "403 Forbidden from NSE"

**Cause:** Missing cookies or rate limiting

**Solution:**
- NSE requires hitting homepage first (handled automatically)
- Wait 5-10 minutes if rate limited
- Check NSE website accessibility

---

#### 3. "No data in Google Sheets"

**Cause:** Sheet not shared with service account

**Solution:**
- Share spreadsheet with service account email
- Grant "Editor" permissions
- Verify spreadsheet ID in settings.yaml

---

#### 4. "Invalid symbol" error

**Cause:** Wrong symbol format

**Solution:**
- Use exact NSE symbol (e.g., `INFY`, not `INFOSYS`)
- Verify symbol at https://www.nseindia.com
- Use UPPERCASE letters

---

### Debugging

**Check logs:**
```bash
# View main application log
tail -f logs/app.log

# View NSE API operations
tail -f logs/nse_api.log

# View Google Sheets operations
tail -f logs/sheets.log
```

**Test connection:**
```bash
# Test NSE connectivity
curl -I https://www.nseindia.com

# Test Google Sheets auth
python -c "from modules.utils import load_config; print(load_config())"
```

**More troubleshooting**: [SETUP_GUIDE.md#7-troubleshooting](SETUP_GUIDE.md#7-troubleshooting)

---

## 🧪 Testing

### Manual Testing

```bash
# Run the application
python main.py

# In Google Sheets, enter test data:
# Symbol: INFY
# From: 01-01-2026
# To: 31-01-2026
# Trigger: TRUE

# Verify results appear in ~10-30 seconds
```

### Unit Tests (Optional)

```bash
# Install test dependencies
pip install pytest

# Run tests
pytest tests/
```

---

## 🚀 Deployment

### Option 1: Local Machine

```bash
# Run in terminal
python main.py

# Or as background process
nohup python main.py > logs/app.log 2>&1 &
```

---

### Option 2: Linux Server (systemd)

**Create service file:**
```bash
sudo nano /etc/systemd/system/nse-analytics.service
```

**Add:**
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

**Enable and start:**
```bash
sudo systemctl enable nse-analytics
sudo systemctl start nse-analytics
sudo systemctl status nse-analytics
```

---

### Option 3: Docker

**Build:**
```bash
docker build -t nse-analytics .
```

**Run:**
```bash
docker run -d \
  --name nse-analytics \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/logs:/app/logs \
  nse-analytics
```

**Or use docker-compose:**
```bash
docker-compose up -d
```

---

### Option 4: Cloud VM (AWS EC2, Google Compute)

1. Launch VM (t3.micro sufficient)
2. Install Python 3.9+
3. Clone repository
4. Configure credentials
5. Set up as systemd service
6. Enable auto-start on boot

**Detailed deployment**: [TECHNICAL_IMPLEMENTATION.md#7-deployment-strategies](TECHNICAL_IMPLEMENTATION.md#7-deployment-strategies)

---

## 🛡️ Security

### Best Practices

- ✅ **Never commit** `credentials.json` to version control
- ✅ **Set read-only permissions** on credentials file
- ✅ **Use .gitignore** to exclude sensitive files
- ✅ **Rotate credentials** if compromised
- ✅ **Limit service account permissions** to minimum required

### Protecting Credentials

```bash
# Set read-only permissions
chmod 400 config/credentials.json

# Verify .gitignore includes:
config/credentials.json
config/settings.yaml
*.log
data/*.csv
```

---

## 📊 Performance

### Expected Metrics

| Metric | Value |
|--------|-------|
| Poll Interval | 5 seconds |
| Data Fetch Time | 2-5 seconds |
| CSV Processing | <1 second |
| Sheets Update | 2-3 seconds |
| **Total Pipeline** | **5-10 seconds** |
| Memory Usage | <100 MB |
| CPU Usage (idle) | <5% |

### Optimization Tips

- Use batch Google Sheets API calls
- Implement rate limiting for NSE API
- Clean up old CSV files automatically
- Enable log rotation

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### How to Contribute

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Code Standards

- Follow PEP 8 style guide
- Add docstrings to functions
- Write unit tests for new features
- Update documentation as needed
- Follow the LLM coding guidelines (see [MODULAR_DESIGN.md](MODULAR_DESIGN.md))

### Reporting Bugs

**Use GitHub Issues with:**
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Log files (if applicable)
- System information (OS, Python version)

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### What You Can Do

- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Use privately

### What You Must Do

- Include copyright notice
- Include license text

### What You Cannot Do

- ❌ Hold liable
- ❌ Claim warranty

---

## 🙏 Acknowledgments

- **NSE India** for providing public historical data API
- **Google** for Sheets API and Drive API
- **Python Community** for excellent libraries (pandas, gspread, requests)
- **Contributors** who helped improve this project

---

## 📞 Support

### Getting Help

**Documentation:**
- [Setup Guide](SETUP_GUIDE.md)
- [User Guide](USER_GUIDE.md)
- [Technical Docs](TECHNICAL_IMPLEMENTATION.md)

**Community:**
- GitHub Issues: Report bugs or request features
- Discussions: Ask questions, share ideas

**Contact:**
- Email: support@yourcompany.com
- Twitter: @yourhandle
- Website: https://yourwebsite.com

---

## 🗺️ Roadmap

### Current Version (1.0)
- ✅ Basic NSE data fetching
- ✅ Google Sheets integration
- ✅ Delivery metrics calculation
- ✅ Automated charts
- ✅ System monitoring

### Future Enhancements

**Version 1.1:**
- [ ] Multi-symbol comparison
- [ ] Email/Slack alerts on delivery spikes
- [ ] Historical comparison (YoY)
- [ ] Custom date range presets

**Version 2.0:**
- [ ] Web UI (alternative to Google Sheets)
- [ ] Database backend (PostgreSQL)
- [ ] RESTful API
- [ ] User authentication
- [ ] Real-time data streaming (when available)

**Version 3.0:**
- [ ] Machine learning predictions
- [ ] Portfolio tracking integration
- [ ] Mobile app
- [ ] Multi-exchange support (BSE, etc.)

---

## 📈 Project Stats

![GitHub Stars](https://img.shields.io/github/stars/your-repo/nse-analytics?style=social)
![GitHub Forks](https://img.shields.io/github/forks/your-repo/nse-analytics?style=social)
![GitHub Issues](https://img.shields.io/github/issues/your-repo/nse-analytics)
![GitHub Pull Requests](https://img.shields.io/github/issues-pr/your-repo/nse-analytics)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

## 📝 Changelog

### v1.0.0 (2026-02-08)
- Initial release
- NSE data fetching
- Google Sheets integration
- Delivery analytics
- Automated charts
- System monitoring

---

## 🔗 Related Projects

- [NSE Python](https://github.com/vsjha18/nse-python) - NSE data library
- [Google Sheets API Python](https://github.com/burnash/gspread) - gspread library
- [pandas](https://github.com/pandas-dev/pandas) - Data analysis library

---

## 📚 Additional Resources

**NSE Resources:**
- [NSE Official Website](https://www.nseindia.com)
- [NSE API Documentation](https://www.nseindia.com/api)
- [Market Data](https://www.nseindia.com/market-data)

**Google Sheets API:**
- [Google Sheets API Docs](https://developers.google.com/sheets/api)
- [gspread Documentation](https://docs.gspread.org)
- [Service Account Setup](https://cloud.google.com/iam/docs/service-accounts)

**Python Resources:**
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [requests Documentation](https://requests.readthedocs.io/)
- [Python 3.9+ Features](https://docs.python.org/3/whatsnew/3.9.html)

---

## 💡 Tips for New Users

1. **Start Small**: Test with 1-month date range first
2. **Verify Symbol**: Always check symbol on NSE website
3. **Monitor Logs**: Keep an eye on `logs/app.log` for errors
4. **Backup Data**: Download Google Sheet as Excel for offline analysis
5. **Read Docs**: Refer to User Guide for detailed usage instructions

---

## 🎓 Learning Resources

**Understanding Delivery %:**
- High delivery % (>60%) indicates genuine buying/selling
- Low delivery % (<30%) indicates speculative trading
- Rising delivery % suggests accumulation
- Falling delivery % suggests distribution

**NSE Market Basics:**
- Trading hours: 9:15 AM - 3:30 PM IST
- Equity segment includes EQ, BE, BZ series
- Delivery data available next day after trading

---

**Made with ❤️ for the trading community**

---

**Quick Links:**
- [📖 Setup Guide](SETUP_GUIDE.md)
- [👤 User Guide](USER_GUIDE.md)
- [🏗️ Architecture](MODULAR_DESIGN.md)
- [⚙️ Technical Docs](TECHNICAL_IMPLEMENTATION.md)
- [🐛 Report Bug](https://github.com/your-repo/nse-analytics/issues)
- [💡 Request Feature](https://github.com/your-repo/nse-analytics/issues)

---

**© 2026 NSE Analytics Project. All rights reserved.**