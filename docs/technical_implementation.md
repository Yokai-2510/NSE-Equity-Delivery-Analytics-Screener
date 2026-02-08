# NSE Equity Delivery Analytics System
## Technical Implementation Document

**Version:** 1.0  
**Date:** February 8, 2026  
**Audience:** Developers and System Administrators

---

## 1. Technical Overview

This document provides implementation-level details for building the NSE Equity Delivery Analytics System. It covers API integration, data processing algorithms, Google Sheets operations, and deployment strategies.

---

## 2. NSE API Integration

### 2.1 API Endpoint Details

**Base URL:** `https://www.nseindia.com`

**Historical Data Endpoint:**
```
GET /api/historical/cm/equity
```

**Query Parameters:**
```python
{
    "symbol": "RELIANCE",           # NSE equity symbol (uppercase)
    "series": "EQ",                 # Equity series
    "from": "01-01-2025",           # DD-MM-YYYY format
    "to": "31-12-2025",             # DD-MM-YYYY format
    "csv": "true"                   # Return CSV format
}
```

**Alternative Endpoint (Fallback):**
```
GET /api/historicalOR/generateSecurityWiseHistoricalData
```

---

### 2.2 Authentication & Cookie Handling

NSE requires a valid session cookie to access the API.

**Cookie Acquisition Flow:**

```python
import requests

def acquire_nse_cookies():
    session = requests.Session()
    
    # Required headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.nseindia.com/report-detail/eq_security",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    session.headers.update(headers)
    
    # CRITICAL: Must hit homepage first
    response = session.get("https://www.nseindia.com", timeout=10)
    
    # Now session has valid cookies
    return session
```

**Why This Works:**
- NSE sets cookies via homepage response
- Subsequent API calls include these cookies automatically
- Session object persists cookies across requests
- Must include `Referer` header to avoid 403 errors

---

### 2.3 CSV Response Format

**Successful Response:**
- Content-Type: `text/csv`
- File download with historical data

**Sample CSV Structure:**
```csv
Symbol,Date,Open Price,High Price,Low Price,Close Price,Last Price,Prev Close,Total Traded Quantity,Turnover,No. of Trades,Deliverable Qty,% Dly Qt to Traded Qty
INFY,01-Jan-2025,1450.50,1465.00,1448.00,1462.75,1462.80,1450.00,5234567,763456789.50,45678,3145678,60.12
```

**Column Mapping:**
| NSE Column | Internal Name | Type |
|------------|---------------|------|
| Symbol | symbol | string |
| Date | date | string (DD-MMM-YYYY) |
| Open Price | open | float |
| High Price | high | float |
| Low Price | low | float |
| Close Price | close | float |
| Total Traded Quantity | total_qty | int |
| Turnover | turnover | float |
| No. of Trades | num_trades | int |
| Deliverable Qty | deliverable_qty | int |
| % Dly Qt to Traded Qty | delivery_pct | float |

---

### 2.4 Error Response Handling

**HTTP Error Codes:**
- `403 Forbidden`: Missing cookies or invalid headers
- `404 Not Found`: Invalid symbol or date range
- `429 Too Many Requests`: Rate limited
- `500 Internal Server Error`: NSE server issue

**HTML Error Page Detection:**

```python
def is_valid_csv(content: bytes) -> bool:
    # NSE returns HTML error pages when something fails
    content_str = content.decode('utf-8', errors='ignore')
    
    # Check for HTML indicators
    html_indicators = ['<!DOCTYPE', '<html>', '<HTML>']
    
    return not any(indicator in content_str for indicator in html_indicators)
```

---

### 2.5 Rate Limiting Strategy

**NSE Limitations:**
- Approximately 10 requests per minute per IP
- Excessive requests may trigger temporary ban

**Implementation:**
```python
import time
from datetime import datetime, timedelta

class NSERateLimiter:
    def __init__(self, requests_per_minute=8):
        self.requests_per_minute = requests_per_minute
        self.request_times = []
    
    def wait_if_needed(self):
        now = datetime.now()
        cutoff = now - timedelta(minutes=1)
        
        # Remove old requests
        self.request_times = [t for t in self.request_times if t > cutoff]
        
        if len(self.request_times) >= self.requests_per_minute:
            # Wait until oldest request is > 1 minute old
            oldest = self.request_times[0]
            wait_time = 60 - (now - oldest).total_seconds()
            if wait_time > 0:
                time.sleep(wait_time)
        
        self.request_times.append(datetime.now())
```

---

### 2.6 Retry Logic Implementation

**Exponential Backoff:**

```python
def retry_with_backoff(func, max_retries=3, base_delay=2):
    for attempt in range(max_retries):
        try:
            return func()
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                raise
            
            delay = base_delay * (2 ** attempt)  # Exponential
            logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
            time.sleep(delay)
```

---

## 3. Data Processing

### 3.1 CSV Parsing Strategy

**Using Pandas:**

```python
import pandas as pd
from pathlib import Path

def parse_nse_csv(csv_path: Path) -> pd.DataFrame:
    # NSE CSVs may have encoding issues
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding='latin-1')
    
    return df
```

**Date Parsing:**

```python
def standardize_dates(df: pd.DataFrame) -> pd.DataFrame:
    # NSE uses DD-MMM-YYYY format (01-Jan-2025)
    df['date'] = pd.to_datetime(df['Date'], format='%d-%b-%Y')
    
    # Convert to DD-MM-YYYY for consistency
    df['date_formatted'] = df['date'].dt.strftime('%d-%m-%Y')
    
    return df
```

---

### 3.2 Data Validation Rules

**Required Column Validation:**

```python
REQUIRED_COLUMNS = [
    'Symbol', 'Date', 'Close Price', 
    'Total Traded Quantity', 'Deliverable Qty'
]

def validate_csv_structure(df: pd.DataFrame) -> tuple[bool, str]:
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    
    if missing_cols:
        return False, f"Missing columns: {', '.join(missing_cols)}"
    
    return True, ""
```

**Data Quality Checks:**

```python
def validate_data_quality(df: pd.DataFrame) -> pd.DataFrame:
    # Remove rows with null critical values
    df = df.dropna(subset=['Date', 'Close Price', 'Total Traded Quantity'])
    
    # Ensure numeric columns are non-negative
    numeric_cols = ['Open Price', 'High Price', 'Low Price', 'Close Price', 
                    'Total Traded Quantity', 'Deliverable Qty', 'Turnover']
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].clip(lower=0)  # No negative values
    
    return df
```

---

### 3.3 Delivery Percentage Calculation

**Formula:**
```
Delivery % = (Deliverable Quantity / Total Traded Quantity) × 100
```

**Implementation:**

```python
def calculate_delivery_percentage(df: pd.DataFrame) -> pd.DataFrame:
    # Handle division by zero
    df['delivery_pct'] = 0.0
    
    mask = df['Total Traded Quantity'] > 0
    df.loc[mask, 'delivery_pct'] = (
        (df.loc[mask, 'Deliverable Qty'] / df.loc[mask, 'Total Traded Quantity']) * 100
    )
    
    # Cap at 100% (shouldn't exceed, but just in case)
    df['delivery_pct'] = df['delivery_pct'].clip(upper=100)
    
    # Round to 2 decimal places
    df['delivery_pct'] = df['delivery_pct'].round(2)
    
    return df
```

---

### 3.4 Summary Statistics Computation

```python
def compute_summary_metrics(df: pd.DataFrame) -> dict:
    # Filter out rows where delivery_pct is 0 (likely data issues)
    valid_delivery = df[df['delivery_pct'] > 0]['delivery_pct']
    
    if len(valid_delivery) == 0:
        return {
            'avg_delivery_pct': 0.0,
            'max_delivery_pct': 0.0,
            'min_delivery_pct': 0.0,
            'total_days': len(df),
            'valid_days': 0
        }
    
    return {
        'avg_delivery_pct': round(valid_delivery.mean(), 2),
        'max_delivery_pct': round(valid_delivery.max(), 2),
        'min_delivery_pct': round(valid_delivery.min(), 2),
        'total_days': len(df),
        'valid_days': len(valid_delivery)
    }
```

---

### 3.5 Data Transformation for Sheets

**Convert DataFrame to List of Lists:**

```python
def dataframe_to_sheets_format(df: pd.DataFrame) -> list:
    # Column order for RAW_DATA sheet
    column_order = [
        'Symbol', 'date_formatted', 'Open Price', 'High Price', 'Low Price', 
        'Close Price', 'Total Traded Quantity', 'Deliverable Qty', 
        'delivery_pct', 'Turnover', 'No. of Trades'
    ]
    
    # Header row
    result = [['Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 
               'Total Qty', 'Deliverable Qty', 'Delivery %', 'Turnover', 'Trades']]
    
    # Data rows
    for _, row in df.iterrows():
        result.append([
            str(row.get(col, '')) for col in column_order
        ])
    
    return result
```

---

## 4. Google Sheets Integration

### 4.1 Authentication Setup

**Service Account Creation:**

1. Go to Google Cloud Console
2. Create new project or select existing
3. Enable Google Sheets API
4. Create Service Account
5. Download JSON key file
6. Share target spreadsheet with service account email

**Authentication Code:**

```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def authenticate_google_sheets(credentials_path: str):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_path, scope
    )
    
    client = gspread.authorize(credentials)
    return client
```

---

### 4.2 Reading User Inputs

**CUSTOM_VIEW Sheet Structure:**

```
     A                    B
1    Symbol:             [User enters here]
2    From Date:          [User enters DD-MM-YYYY]
3    To Date:            [User enters DD-MM-YYYY]
4    Update Trigger:     [Checkbox, TRUE/FALSE]
```

**Reading Implementation:**

```python
def read_control_inputs(spreadsheet: gspread.Spreadsheet) -> dict:
    worksheet = spreadsheet.worksheet("CUSTOM_VIEW")
    
    inputs = {
        'symbol': worksheet.acell('B1').value or '',
        'from_date': worksheet.acell('B2').value or '',
        'to_date': worksheet.acell('B3').value or '',
        'trigger': worksheet.acell('B4').value == 'TRUE'
    }
    
    # Clean inputs
    inputs['symbol'] = inputs['symbol'].strip().upper()
    
    return inputs
```

---

### 4.3 Writing Data to Sheets

**Bulk Write Strategy:**

```python
def write_raw_data(worksheet: gspread.Worksheet, data: list):
    # Clear existing data
    worksheet.clear()
    
    # Batch update (much faster than cell-by-cell)
    # data is list of lists: [header_row, data_row1, data_row2, ...]
    
    if len(data) > 0:
        # Update range A1 to last column/row
        num_rows = len(data)
        num_cols = len(data[0])
        
        end_col = chr(65 + num_cols - 1)  # A=65, B=66, etc.
        range_notation = f'A1:{end_col}{num_rows}'
        
        worksheet.update(range_notation, data)
```

**Batch API Usage:**

```python
def batch_update_cells(worksheet: gspread.Worksheet, updates: list):
    """
    updates = [
        {'range': 'A1', 'values': [['Header']]},
        {'range': 'A2:C100', 'values': data_rows}
    ]
    """
    worksheet.batch_update(updates)
```

---

### 4.4 System Status Sheet Format

**SYSTEM_STATUS Sheet Layout:**

```
     A                          B
1    Metric                     Value
2    Last Update Time           08-02-2026 14:32:15
3    Symbol                     INFY
4    Date Range                 01-01-2025 to 31-12-2025
5    Pipeline Status            Success
6    Total Records              250
7    Average Delivery %         45.67
8    Max Delivery %             78.23
9    Min Delivery %             12.45
10   Execution Time (sec)       3.45
11   Last Error                 (None)
```

**Writing Implementation:**

```python
def update_system_status(worksheet: gspread.Worksheet, status: dict):
    from datetime import datetime
    
    timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    
    data = [
        ['Metric', 'Value'],
        ['Last Update Time', timestamp],
        ['Symbol', status['symbol']],
        ['Date Range', f"{status['from_date']} to {status['to_date']}"],
        ['Pipeline Status', status.get('status', 'Success')],
        ['Total Records', str(status.get('total_records', 0))],
        ['Average Delivery %', str(status.get('avg_delivery_pct', 0))],
        ['Max Delivery %', str(status.get('max_delivery_pct', 0))],
        ['Min Delivery %', str(status.get('min_delivery_pct', 0))],
        ['Execution Time (sec)', str(status.get('execution_time', 0))],
        ['Last Error', status.get('last_error', '(None)')]
    ]
    
    worksheet.clear()
    worksheet.update('A1:B11', data)
```

---

### 4.5 Chart Configuration

**DELIVERY_CHARTS Sheet:**

Charts are created manually in Google Sheets UI, but reference RAW_DATA programmatically.

**Chart 1: Delivery % Over Time (Line Chart)**
- Data Range: `RAW_DATA!B2:B` (Dates) and `RAW_DATA!I2:I` (Delivery %)
- X-Axis: Date
- Y-Axis: Delivery %
- Title: "Delivery Percentage Trend"

**Chart 2: Volume vs Delivery (Combo Chart)**
- Data Range: `RAW_DATA!B2:B` (Dates), `RAW_DATA!G2:G` (Volume), `RAW_DATA!I2:I` (Delivery %)
- Left Y-Axis: Volume (bars)
- Right Y-Axis: Delivery % (line)
- Title: "Volume vs Delivery Analysis"

**Note:** Charts auto-update when RAW_DATA changes.

---

### 4.6 CUSTOM_VIEW Sheet Formulas

**Filtered Data Display:**

```
Cell A10: "Filtered Data (Based on Inputs)"
Cell A11: Headers

Cell A12 (Formula):
=QUERY(RAW_DATA!A:K, "SELECT * WHERE A = '" & B1 & "' AND B >= date '" & TEXT(B2, "yyyy-MM-dd") & "' AND B <= date '" & TEXT(B3, "yyyy-MM-dd") & "'", 1)
```

**Summary Metrics:**

```
Cell D2 (Average Delivery %):
=AVERAGE(FILTER(RAW_DATA!I:I, RAW_DATA!A:A=B1, RAW_DATA!B:B>=B2, RAW_DATA!B:B<=B3))

Cell D3 (Max Delivery %):
=MAX(FILTER(RAW_DATA!I:I, RAW_DATA!A:A=B1, RAW_DATA!B:B>=B2, RAW_DATA!B:B<=B3))

Cell D4 (Min Delivery %):
=MIN(FILTER(RAW_DATA!I:I, RAW_DATA!A:A=B1, RAW_DATA!B:B>=B2, RAW_DATA!B:B<=B3))
```

---

### 4.7 API Rate Limiting

**Google Sheets API Limits:**
- 300 requests per minute per project
- 100 requests per 100 seconds per user

**Mitigation Strategy:**

```python
import time

class SheetsRateLimiter:
    def __init__(self, requests_per_minute=60):
        self.rpm = requests_per_minute
        self.min_interval = 60.0 / requests_per_minute
        self.last_request_time = 0
    
    def wait_if_needed(self):
        now = time.time()
        elapsed = now - self.last_request_time
        
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        
        self.last_request_time = time.time()

# Usage
rate_limiter = SheetsRateLimiter(requests_per_minute=60)

def safe_sheet_update(worksheet, data):
    rate_limiter.wait_if_needed()
    worksheet.update('A1', data)
```

---

## 5. Monitoring and Polling

### 5.1 Polling Loop Implementation

**Basic Polling:**

```python
import time

def start_monitoring_loop(config: dict):
    client = authenticate_google_sheets(config['credentials_path'])
    spreadsheet = client.open_by_key(config['spreadsheet_id'])
    
    poll_interval = config.get('poll_interval_seconds', 5)
    
    logging.info(f"Monitoring started. Polling every {poll_interval} seconds.")
    
    while not is_shutdown_requested():
        try:
            inputs = read_control_inputs(spreadsheet)
            
            if inputs['trigger']:
                logging.info(f"Trigger detected: {inputs['symbol']}")
                
                # Execute pipeline
                execute_pipeline(inputs, config, spreadsheet)
                
                # Reset trigger
                reset_trigger(spreadsheet)
            
        except Exception as e:
            logging.error(f"Monitoring error: {e}")
        
        time.sleep(poll_interval)
    
    logging.info("Monitoring stopped")
```

---

### 5.2 Trigger Detection Optimization

**Smart Polling (Check Trigger Cell Only):**

```python
def check_trigger_only(spreadsheet: gspread.Spreadsheet) -> bool:
    worksheet = spreadsheet.worksheet("CUSTOM_VIEW")
    trigger_value = worksheet.acell('B4').value
    return trigger_value == 'TRUE'

# In polling loop:
if not check_trigger_only(spreadsheet):
    continue  # Skip full read if no trigger
```

---

### 5.3 Pipeline Execution Flow

```python
def execute_pipeline(inputs: dict, config: dict, spreadsheet: gspread.Spreadsheet):
    start_time = time.time()
    
    try:
        # Step 1: Validate inputs
        is_valid, error_msg = validate_inputs(inputs)
        if not is_valid:
            raise ValueError(error_msg)
        
        # Step 2: Fetch NSE data
        csv_path = fetch_nse_historical_data(
            inputs['symbol'], 
            inputs['from_date'], 
            inputs['to_date'],
            config['data_folder']
        )
        
        # Step 3: Process CSV
        processed = process_nse_csv(csv_path)
        
        # Step 4: Update sheets
        update_all_sheets(
            spreadsheet, 
            processed, 
            inputs['symbol'],
            inputs['from_date'],
            inputs['to_date'],
            time.time() - start_time
        )
        
        # Step 5: Cleanup
        cleanup_old_csvs(config['data_folder'])
        
        logging.info(f"Pipeline completed in {time.time() - start_time:.2f} seconds")
        
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        update_system_status_with_error(spreadsheet, str(e))
```

---

## 6. Error Handling & Recovery

### 6.1 Error Classification

**Recoverable Errors:**
- Network timeouts → Retry
- Rate limiting → Backoff and retry
- Temporary NSE downtime → Retry later

**Non-Recoverable Errors:**
- Invalid symbol → User input error
- Invalid date format → User input error
- Missing credentials → Configuration error

---

### 6.2 Error Reporting to User

**Write Error to SYSTEM_STATUS:**

```python
def update_system_status_with_error(spreadsheet: gspread.Spreadsheet, error_msg: str):
    worksheet = spreadsheet.worksheet("SYSTEM_STATUS")
    
    from datetime import datetime
    timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    
    data = [
        ['Metric', 'Value'],
        ['Last Update Time', timestamp],
        ['Pipeline Status', 'ERROR'],
        ['Last Error', error_msg]
    ]
    
    worksheet.update('A1:B4', data)
```

---

### 6.3 Logging Errors

**Structured Error Logging:**

```python
import logging
import traceback

def log_error_with_context(error: Exception, context: dict):
    logging.error(f"Error: {str(error)}")
    logging.error(f"Context: {context}")
    logging.error(f"Traceback: {traceback.format_exc()}")
```

---

## 7. Deployment Strategies

### 7.1 Local Machine Deployment

**systemd Service (Linux):**

Create `/etc/systemd/system/nse-analytics.service`:

```ini
[Unit]
Description=NSE Equity Delivery Analytics Service
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/nse-delivery-analytics
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10

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

### 7.2 Cloud VM Deployment (AWS EC2)

**Instance Requirements:**
- Instance Type: t3.micro (sufficient)
- OS: Ubuntu 22.04 LTS
- Storage: 10 GB
- Security Group: Outbound HTTPS (443) only

**Setup Steps:**

```bash
# Install Python
sudo apt update
sudo apt install python3 python3-pip

# Clone repository
git clone <your-repo-url>
cd nse-delivery-analytics

# Install dependencies
pip3 install -r requirements.txt

# Configure
cp config/settings.yaml.example config/settings.yaml
# Edit settings.yaml with your spreadsheet ID

# Upload credentials.json
scp credentials.json ec2-user@<instance-ip>:/path/to/config/

# Run as service
sudo systemctl enable nse-analytics
sudo systemctl start nse-analytics
```

---

### 7.3 Google Cloud Run Deployment (Serverless)

**Not recommended** for this use case because:
- Cloud Run is for HTTP request-response
- This system needs continuous polling
- Alternative: Google Cloud Compute Engine with persistent VM

---

### 7.4 Docker Deployment

**Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  nse-analytics:
    build: .
    volumes:
      - ./config:/app/config
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    environment:
      - TZ=Asia/Kolkata
```

**Run:**
```bash
docker-compose up -d
docker-compose logs -f
```

---

## 8. Performance Optimization

### 8.1 CSV Processing

**Use Chunking for Large Files:**

```python
def process_large_csv(csv_path: Path) -> pd.DataFrame:
    chunks = []
    
    for chunk in pd.read_csv(csv_path, chunksize=1000):
        # Process chunk
        chunk = standardize_dates(chunk)
        chunk = calculate_delivery_percentage(chunk)
        chunks.append(chunk)
    
    return pd.concat(chunks, ignore_index=True)
```

---

### 8.2 Google Sheets Batch Operations

**Instead of:**
```python
for row in data:
    worksheet.append_row(row)  # Slow!
```

**Do this:**
```python
worksheet.update('A1', data)  # Fast batch update
```

---

### 8.3 Caching Strategy

**Cache Recent Symbols:**

```python
from functools import lru_cache

@lru_cache(maxsize=10)
def fetch_cached_data(symbol: str, from_date: str, to_date: str):
    # Only fetch if not in cache
    return fetch_nse_historical_data(symbol, from_date, to_date)
```

---

## 9. Security Considerations

### 9.1 Credentials Management

**Never commit credentials:**

```gitignore
# .gitignore
config/credentials.json
config/settings.yaml
*.log
data/*.csv
```

**Use environment variables (optional):**

```python
import os

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID', 'fallback-id')
```

---

### 9.2 Input Sanitization

**Prevent SQL-like injection in symbols:**

```python
import re

def sanitize_symbol(symbol: str) -> str:
    # Only allow alphanumeric and underscore
    sanitized = re.sub(r'[^A-Z0-9_]', '', symbol.upper())
    
    if len(sanitized) == 0 or len(sanitized) > 20:
        raise ValueError("Invalid symbol format")
    
    return sanitized
```

---

## 10. Testing Strategy

### 10.1 Unit Tests

**Test Date Parsing:**

```python
def test_parse_nse_date():
    assert parse_date_string("01-01-2025") == datetime(2025, 1, 1)
    assert parse_date_string("31-12-2025") == datetime(2025, 12, 31)
```

**Test Delivery Calculation:**

```python
def test_delivery_percentage():
    df = pd.DataFrame({
        'Total Traded Quantity': [1000, 2000, 0],
        'Deliverable Qty': [600, 1200, 0]
    })
    
    result = calculate_delivery_percentage(df)
    
    assert result['delivery_pct'].iloc[0] == 60.0
    assert result['delivery_pct'].iloc[1] == 60.0
    assert result['delivery_pct'].iloc[2] == 0.0
```

---

### 10.2 Integration Tests

**Mock NSE API:**

```python
from unittest.mock import patch
import requests_mock

def test_nse_fetch_with_mock():
    with requests_mock.Mocker() as m:
        m.get('https://www.nseindia.com', text='')
        m.get('https://www.nseindia.com/api/historical/cm/equity',
              text='Symbol,Date,Close\nINFY,01-Jan-2025,1450')
        
        result = fetch_nse_historical_data('INFY', '01-01-2025', '31-01-2025', Path('data'))
        assert result.exists()
```

---

### 10.3 End-to-End Test

**Manual Test Checklist:**

1. ✅ Start service
2. ✅ Enter symbol in Google Sheet
3. ✅ Enter date range
4. ✅ Click trigger
5. ✅ Wait 10-30 seconds
6. ✅ Verify RAW_DATA populated
7. ✅ Verify CUSTOM_VIEW shows filtered data
8. ✅ Verify DELIVERY_CHARTS updated
9. ✅ Verify SYSTEM_STATUS shows success

---

## 11. Troubleshooting Guide

### 11.1 Common Issues

**Issue: 403 Forbidden from NSE**
- Cause: Missing cookies or invalid headers
- Solution: Ensure homepage is hit first, check headers

**Issue: No data in Google Sheets**
- Cause: Service account not shared with sheet
- Solution: Share sheet with service account email

**Issue: Charts not updating**
- Cause: Chart data range doesn't reference RAW_DATA
- Solution: Edit chart, set data range to RAW_DATA!A:K

**Issue: Old data still showing**
- Cause: Browser cache
- Solution: Hard refresh (Ctrl+Shift+R)

---

### 11.2 Debug Commands

**Check logs:**
```bash
tail -f logs/app.log
tail -f logs/nse_api.log
```

**Test NSE connectivity:**
```bash
curl -I https://www.nseindia.com
```

**Verify Google Sheets auth:**
```python
python3 -c "from modules.sheets_reader import authenticate_google_sheets; print(authenticate_google_sheets('config/credentials.json'))"
```

---

## 12. Maintenance

### 12.1 Log Rotation

**Automatic with RotatingFileHandler:**
- Logs auto-rotate at 10MB
- Keeps 5 backup files
- Oldest deleted automatically

---

### 12.2 CSV Cleanup

**Auto-cleanup:**
- Runs after each pipeline execution
- Deletes CSVs older than 24 hours

**Manual cleanup:**
```bash
rm data/*.csv
```

---

### 12.3 Monitoring Health

**Check service status:**
```bash
systemctl status nse-analytics
```

**Check last update time in SYSTEM_STATUS sheet**

---

## 13. API Reference (Internal)

### 13.1 Module: nse_fetcher

```python
fetch_nse_historical_data(
    symbol: str,           # NSE equity symbol (e.g., "INFY")
    from_date: str,        # DD-MM-YYYY format
    to_date: str,          # DD-MM-YYYY format
    data_folder: Path      # Where to save CSV
) -> Path                  # Returns path to downloaded CSV

# Raises: NSEFetchError on any failure
```

---

### 13.2 Module: data_processor

```python
process_nse_csv(
    csv_path: Path
) -> dict

# Returns:
{
    'raw_data': [[row1], [row2], ...],  # List of lists for sheets
    'summary': {
        'avg_delivery_pct': float,
        'max_delivery_pct': float,
        'min_delivery_pct': float,
        'total_days': int,
        'valid_days': int
    }
}
```

---

### 13.3 Module: sheets_writer

```python
update_all_sheets(
    spreadsheet: gspread.Spreadsheet,
    processed_data: dict,
    symbol: str,
    from_date: str,
    to_date: str,
    execution_time: float
) -> None

# Side effects: Writes to RAW_DATA and SYSTEM_STATUS sheets
```

---

## 14. Future Technical Enhancements

### 14.1 Database Backend

**Replace CSV with SQLite:**

```python
import sqlite3

def store_in_database(processed_data: dict):
    conn = sqlite3.connect('data/nse_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historical_data (
            symbol TEXT,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            deliverable INTEGER,
            delivery_pct REAL
        )
    ''')
    
    # Insert data
    # ...
    
    conn.commit()
    conn.close()
```

---

### 14.2 Webhook Trigger (Alternative to Polling)

**Google Apps Script:**

```javascript
function onEdit(e) {
  var range = e.range;
  if (range.getA1Notation() == 'B4' && range.getValue() == true) {
    // Trigger detected, send webhook
    var url = 'https://your-webhook-endpoint.com/trigger';
    var options = {
      'method': 'post',
      'contentType': 'application/json',
      'payload': JSON.stringify({
        'symbol': SpreadsheetApp.getActiveSheet().getRange('B1').getValue(),
        'from_date': SpreadsheetApp.getActiveSheet().getRange('B2').getValue(),
        'to_date': SpreadsheetApp.getActiveSheet().getRange('B3').getValue()
      })
    };
    UrlFetchApp.fetch(url, options);
  }
}
```

**Python webhook receiver:**

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/trigger', methods=['POST'])
def handle_trigger():
    data = request.json
    execute_pipeline(data)
    return {'status': 'success'}

app.run(host='0.0.0.0', port=5000)
```

---

## 15. Performance Benchmarks

**Expected Performance:**

| Metric | Value |
|--------|-------|
| NSE API Response Time | 2-5 seconds |
| CSV Processing (250 rows) | < 1 second |
| Google Sheets Write (250 rows) | 2-3 seconds |
| Total Pipeline Execution | 5-10 seconds |
| Polling Interval | 5 seconds |
| Memory Usage | < 100 MB |
| CPU Usage | < 5% (idle), 20% (during pipeline) |

---

**End of Technical Implementation Document**