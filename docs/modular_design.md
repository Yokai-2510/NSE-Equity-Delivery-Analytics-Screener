# NSE Equity Delivery Analytics System
## Modular Design Document

**Version:** 1.0  
**Date:** February 8, 2026  
**Design Philosophy:** LLM Coding Guidelines v3 Compliant

---

## 1. Design Principles

This modular design strictly adheres to the LLM Python Coding Style & Execution Specification (v3).

**Core Tenets:**
1. **Separation of Concerns:** Each module owns exactly one responsibility
2. **No God Functions:** Every function does one specific task
3. **Linear Entry Point:** `main.py` orchestrates, never implements
4. **Explicit Over Implicit:** No hidden state, no side effects at import
5. **Small, Readable Functions:** Flat flow, minimal nesting

---

## 2. Project Structure

```
nse-delivery-analytics/
│
├── main.py                          # Entry point (orchestrator only)
├── requirements.txt                 # Python dependencies
├── README.md                        # User documentation
├── .gitignore                       # Git exclusions
│
├── config/                          # Configuration & credentials
│   ├── settings.yaml                # Application settings
│   ├── credentials.json             # Google service account key (gitignored)
│   └── logging_config.yaml          # Logging configuration
│
├── modules/                         # Core business logic
│   ├── __init__.py
│   ├── nse_fetcher.py               # NSE API interaction
│   ├── sheets_reader.py             # Read from Google Sheets
│   ├── sheets_writer.py             # Write to Google Sheets
│   ├── data_processor.py            # CSV parsing and validation
│   └── utils.py                     # Shared utilities
│
├── data/                            # Temporary CSV storage
│   ├── .gitkeep
│   └── *.csv                        # Downloaded CSVs (auto-deleted)
│
└── logs/                            # Application logs
    ├── app.log                      # Main application log
    ├── nse_api.log                  # NSE fetcher specific
    └── sheets.log                   # Google Sheets operations
```

---

## 3. Module Specifications

### 3.1 main.py (Entry Point)

**Purpose:** Bootstrap and orchestrate the application

**Allowed Operations:**
- Import modules
- Load configuration
- Initialize logging
- Register signal handlers
- Call module entry points
- Keep process alive

**Forbidden Operations:**
- ❌ Function definitions
- ❌ Class definitions
- ❌ Business logic
- ❌ Conditional orchestration
- ❌ Error handling beyond shutdown

**Structure:**
```python
# Imports only
from modules.utils import setup_logging, register_shutdown_handlers, load_config
from modules.sheets_reader import start_monitoring_loop

# Linear execution top to bottom
setup_logging()
config = load_config()
register_shutdown_handlers()
start_monitoring_loop(config)
```

**Rationale:** The entry point is a checklist, not a program. All complexity lives in modules.

---

### 3.2 modules/utils.py

**Responsibility:** Shared utilities used by all modules

**Exposed Functions:**

```python
def setup_logging() -> None
    """Configure file and console logging based on logging_config.yaml"""

def load_config() -> dict
    """Load settings.yaml and return configuration dictionary"""

def parse_date_string(date_str: str, format: str = "%d-%m-%Y") -> datetime
    """Convert string to datetime object"""

def format_date_for_nse(date_obj: datetime) -> str
    """Convert datetime to NSE API format (DD-MM-YYYY)"""

def validate_symbol(symbol: str) -> bool
    """Check if symbol format is valid (uppercase, alphanumeric)"""

def validate_date_range(from_date: str, to_date: str) -> tuple[bool, str]
    """Validate date range, return (is_valid, error_message)"""

def cleanup_old_csvs(data_folder: Path, max_age_hours: int = 24) -> None
    """Delete CSV files older than specified hours"""

def retry_on_failure(func: Callable, max_retries: int = 3, delay: int = 2) -> Any
    """Decorator for retrying flaky operations"""

def register_shutdown_handlers() -> None
    """Setup SIGTERM and SIGINT handlers for graceful shutdown"""
```

**Design Notes:**
- Each function is single-purpose
- No state mutation except logging
- All functions are pure or have explicit side effects in docstring
- Validation functions return tuples: (success, error_message)

---

### 3.3 modules/nse_fetcher.py

**Responsibility:** Download historical equity data from NSE API

**Exposed Entry Point:**

```python
def fetch_nse_historical_data(symbol: str, from_date: str, to_date: str, data_folder: Path) -> Path
    """
    Download NSE historical data CSV
    
    Returns: Path to downloaded CSV file
    Raises: NSEFetchError on failure
    """
```

**Internal Functions:**

```python
def _create_session_with_headers() -> requests.Session
    """Create HTTP session with required headers"""

def _get_nse_cookies(session: requests.Session) -> None
    """Hit NSE homepage to obtain cookies"""

def _build_api_params(symbol: str, from_date: str, to_date: str) -> dict
    """Construct query parameters for API call"""

def _download_csv_content(session: requests.Session, params: dict) -> bytes
    """Make API call and return CSV bytes"""

def _save_csv_to_disk(content: bytes, symbol: str, from_date: str, to_date: str, data_folder: Path) -> Path
    """Write CSV bytes to file with timestamp"""

def _validate_csv_response(content: bytes) -> bool
    """Check if response is valid CSV (not HTML error page)"""
```

**Error Handling:**

```python
class NSEFetchError(Exception):
    """Raised when NSE API fetch fails"""
```

**Flow:**
1. Create session
2. Get cookies
3. Build params
4. Download content
5. Validate response
6. Save to disk
7. Return path

**Retry Strategy:**
- Uses `@retry_on_failure` decorator from utils
- Max 3 retries with 2-second exponential backoff
- Logs each attempt

---

### 3.4 modules/data_processor.py

**Responsibility:** Parse, validate, and transform NSE CSV data

**Exposed Entry Point:**

```python
def process_nse_csv(csv_path: Path) -> dict
    """
    Process NSE CSV into structured data
    
    Returns: {
        'raw_data': [[col1, col2, ...], ...],  # List of rows
        'summary': {
            'avg_delivery_pct': float,
            'max_delivery_pct': float,
            'min_delivery_pct': float,
            'total_days': int,
            'symbol': str,
            'from_date': str,
            'to_date': str
        }
    }
    """
```

**Internal Functions:**

```python
def _load_csv_to_dataframe(csv_path: Path) -> pd.DataFrame
    """Read CSV using pandas"""

def _standardize_column_names(df: pd.DataFrame) -> pd.DataFrame
    """Rename columns to consistent format"""

def _calculate_delivery_percentage(df: pd.DataFrame) -> pd.DataFrame
    """Add delivery_pct column if missing"""

def _handle_missing_values(df: pd.DataFrame) -> pd.DataFrame
    """Fill NaN values with 0 or appropriate defaults"""

def _convert_dates_to_standard_format(df: pd.DataFrame) -> pd.DataFrame
    """Ensure all dates are DD-MM-YYYY format"""

def _compute_summary_statistics(df: pd.DataFrame) -> dict
    """Calculate avg, max, min delivery percentages"""

def _dataframe_to_list_of_lists(df: pd.DataFrame) -> list
    """Convert pandas DataFrame to list format for sheets"""
```

**Validation Rules:**
- Required columns: Date, Symbol, Close, Total Traded Quantity, Deliverable Quantity
- Dates must be parseable
- Numeric columns must be non-negative
- Delivery percentage must be 0-100 range

---

### 3.5 modules/sheets_reader.py

**Responsibility:** Monitor Google Sheets for user input and trigger

**Exposed Entry Point:**

```python
def start_monitoring_loop(config: dict) -> None
    """
    Main monitoring loop - polls Google Sheets every N seconds
    Runs indefinitely until shutdown signal
    """
```

**Internal Functions:**

```python
def _authenticate_sheets_service(credentials_path: Path) -> gspread.Client
    """Create authenticated Google Sheets client"""

def _open_spreadsheet(client: gspread.Client, sheet_id: str) -> gspread.Spreadsheet
    """Open spreadsheet by ID"""

def _read_control_inputs(worksheet: gspread.Worksheet) -> dict
    """
    Read user inputs from CUSTOM_VIEW sheet
    
    Returns: {
        'symbol': str,
        'from_date': str,
        'to_date': str,
        'trigger': bool
    }
    """

def _check_trigger_status(worksheet: gspread.Worksheet) -> bool
    """Check if UPDATE_TRIGGER cell is TRUE"""

def _reset_trigger(worksheet: gspread.Worksheet) -> None
    """Set UPDATE_TRIGGER cell back to FALSE"""

def _trigger_pipeline(symbol: str, from_date: str, to_date: str, config: dict) -> None
    """Execute the full data pipeline"""

def _handle_pipeline_error(error: Exception, spreadsheet: gspread.Spreadsheet) -> None
    """Write error message to SYSTEM_STATUS sheet"""
```

**Monitoring Flow:**
1. Authenticate with Google Sheets
2. Open target spreadsheet
3. Loop:
   - Check trigger status (every 5 seconds)
   - If triggered:
     - Read inputs
     - Validate inputs
     - Execute pipeline
     - Reset trigger
     - Update system status
   - Sleep

**Threading Model:**
- Main thread runs monitoring loop
- Pipeline execution in same thread (sequential)
- No concurrent pipeline runs (prevents race conditions)

---

### 3.6 modules/sheets_writer.py

**Responsibility:** Write processed data to all Google Sheets tabs

**Exposed Entry Point:**

```python
def update_all_sheets(spreadsheet: gspread.Spreadsheet, processed_data: dict, 
                      symbol: str, from_date: str, to_date: str, 
                      execution_time: float) -> None
    """
    Atomically update all 4 sheets
    Rolls back on any failure
    """
```

**Internal Functions:**

```python
def _get_or_create_sheet(spreadsheet: gspread.Spreadsheet, sheet_name: str) -> gspread.Worksheet
    """Get existing sheet or create if missing"""

def _clear_sheet_data(worksheet: gspread.Worksheet) -> None
    """Clear all data from sheet (preserves formulas in protected ranges)"""

def _write_raw_data_sheet(worksheet: gspread.Worksheet, data: list) -> None
    """Bulk write to RAW_DATA sheet"""

def _update_system_status_sheet(worksheet: gspread.Worksheet, status_data: dict) -> None
    """Write system health metrics"""

def _format_status_data(symbol: str, from_date: str, to_date: str, 
                        summary: dict, execution_time: float) -> dict
    """Prepare status metrics for display"""

def _batch_update_cells(worksheet: gspread.Worksheet, updates: list) -> None
    """Use batch API for efficient writes"""
```

**Write Strategy:**
1. Clear RAW_DATA sheet
2. Write all rows in single batch operation
3. Update SYSTEM_STATUS sheet with metrics
4. Preserve CUSTOM_VIEW formulas (only data changes)
5. DELIVERY_CHARTS auto-updates via chart references

**Atomic Behavior:**
- If any sheet write fails, log error and update SYSTEM_STATUS with failure
- Do not attempt partial rollback (too complex)
- User can re-trigger to retry

**Google Sheets Structure Written:**

**RAW_DATA Sheet:**
```
Row 1: Headers [Symbol, Date, Open, High, Low, Close, VWAP, Total_Qty, Deliverable_Qty, Delivery_Pct, Turnover, Trades]
Row 2+: Data rows
```

**SYSTEM_STATUS Sheet:**
```
Last Update Time: <timestamp>
Symbol: <symbol>
Date Range: <from> to <to>
Status: Success / Error
Total Records: <count>
Avg Delivery %: <value>
Max Delivery %: <value>
Min Delivery %: <value>
Execution Time: <seconds>
Last Error: <error message if any>
```

---

## 4. Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 1. setup_logging()                                   │   │
│  │ 2. config = load_config()                            │   │
│  │ 3. register_shutdown_handlers()                      │   │
│  │ 4. start_monitoring_loop(config)  ◄── Blocks here   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  sheets_reader.py                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Loop every 5 seconds:                                │   │
│  │   ├─ _check_trigger_status()                         │   │
│  │   ├─ if triggered:                                   │   │
│  │   │    ├─ _read_control_inputs()                     │   │
│  │   │    ├─ validate (utils.validate_*)                │   │
│  │   │    ├─ _trigger_pipeline() ──────────┐            │   │
│  │   │    └─ _reset_trigger()              │            │   │
│  └──────────────────────────────────────────┼────────────┘   │
└─────────────────────────────────────────────┼────────────────┘
                                              │
                                              ▼
                        ┌─────────────────────────────────┐
                        │     Pipeline Execution          │
                        └─────────────────────────────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                ▼                   ▼                   ▼
    ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
    │ nse_fetcher.py   │ │data_processor.py │ │sheets_writer.py  │
    │                  │ │                  │ │                  │
    │ fetch_nse_       │ │ process_nse_csv()│ │ update_all_      │
    │ historical_data()│ │                  │ │ sheets()         │
    │                  │ │ Returns:         │ │                  │
    │ Returns:         │ │ - raw_data       │ │ Writes to:       │
    │ - CSV file path  │ │ - summary stats  │ │ - RAW_DATA       │
    │                  │ │                  │ │ - SYSTEM_STATUS  │
    └──────────────────┘ └──────────────────┘ └──────────────────┘
            │                     │                     │
            │                     │                     │
            └─────────┬───────────┴─────────────────────┘
                      │
                      ▼
              ┌──────────────────┐
              │    utils.py      │
              │                  │
              │ - cleanup_old_   │
              │   csvs()         │
              │ - logging        │
              └──────────────────┘
```

---

## 5. Function Granularity Examples

### ❌ BAD - God Function (Violates Guidelines)

```python
def handle_update_request(spreadsheet, config):
    # 100+ lines of mixed responsibilities
    inputs = read_cells(...)
    if not validate(inputs):
        write_error(...)
        return
    
    session = create_session()
    session.get("https://nseindia.com")
    response = session.get(API_URL, params=...)
    
    df = pd.read_csv(io.BytesIO(response.content))
    df = df.rename(columns=...)
    df['delivery_pct'] = df['deliverable'] / df['total'] * 100
    
    worksheet = spreadsheet.worksheet("RAW_DATA")
    worksheet.clear()
    worksheet.update(...)
    
    # ... more mixed logic
```

**Problems:**
- Multiple responsibilities in one function
- Impossible to test individual steps
- Hidden dependencies
- Difficult to debug

---

### ✅ GOOD - Modular Functions (Compliant)

```python
# sheets_reader.py
def _trigger_pipeline(symbol, from_date, to_date, config):
    csv_path = fetch_nse_historical_data(symbol, from_date, to_date, config['data_folder'])
    processed = process_nse_csv(csv_path)
    update_all_sheets(config['spreadsheet'], processed, symbol, from_date, to_date, 0.0)
    cleanup_old_csvs(config['data_folder'])
```

**Benefits:**
- Each line is a single, testable operation
- Clear separation of concerns
- Easy to add logging between steps
- Readable top-to-bottom

---

## 6. Error Handling Strategy

### Module-Level Error Handling

Each module handles its own errors explicitly.

**nse_fetcher.py:**
```python
def fetch_nse_historical_data(symbol, from_date, to_date, data_folder):
    try:
        session = _create_session_with_headers()
        _get_nse_cookies(session)
        params = _build_api_params(symbol, from_date, to_date)
        content = _download_csv_content(session, params)
        
        if not _validate_csv_response(content):
            raise NSEFetchError("Invalid CSV response from NSE")
        
        return _save_csv_to_disk(content, symbol, from_date, to_date, data_folder)
    
    except requests.RequestException as e:
        raise NSEFetchError(f"Network error: {e}")
    except Exception as e:
        raise NSEFetchError(f"Unexpected error: {e}")
```

**sheets_reader.py:**
```python
def _trigger_pipeline(symbol, from_date, to_date, config):
    try:
        csv_path = fetch_nse_historical_data(symbol, from_date, to_date, config['data_folder'])
        processed = process_nse_csv(csv_path)
        update_all_sheets(config['spreadsheet'], processed, symbol, from_date, to_date, 0.0)
        
    except NSEFetchError as e:
        _handle_pipeline_error(f"Data fetch failed: {e}", config['spreadsheet'])
    except Exception as e:
        _handle_pipeline_error(f"Pipeline error: {e}", config['spreadsheet'])
```

**Principle:** Fail fast, log explicitly, bubble up custom exceptions

---

## 7. Logging Specification

### Log Files

**logs/app.log** (Main application flow)
```
2026-02-08 14:32:10.123 [INFO] [main] Application started
2026-02-08 14:32:10.234 [INFO] [sheets_reader] Monitoring started for sheet ID: 1abc...
2026-02-08 14:32:15.456 [INFO] [sheets_reader] Trigger detected: INFY, 01-01-2025 to 31-12-2025
2026-02-08 14:32:15.567 [INFO] [nse_fetcher] Fetching data for INFY
2026-02-08 14:32:18.890 [INFO] [data_processor] Processing 250 rows
2026-02-08 14:32:20.123 [INFO] [sheets_writer] Updated all sheets successfully
```

**logs/nse_api.log** (NSE-specific operations)
```
2026-02-08 14:32:15.567 [DEBUG] [nse_fetcher] Creating HTTP session
2026-02-08 14:32:15.678 [DEBUG] [nse_fetcher] Fetching homepage for cookies
2026-02-08 14:32:16.234 [DEBUG] [nse_fetcher] Cookies acquired
2026-02-08 14:32:16.345 [DEBUG] [nse_fetcher] API call: symbol=INFY, from=01-01-2025, to=31-12-2025
2026-02-08 14:32:18.456 [DEBUG] [nse_fetcher] Response size: 125KB
2026-02-08 14:32:18.567 [INFO] [nse_fetcher] CSV saved: data/INFY_20250101_20251231.csv
```

**logs/sheets.log** (Google Sheets operations)
```
2026-02-08 14:32:20.123 [DEBUG] [sheets_writer] Clearing RAW_DATA sheet
2026-02-08 14:32:20.234 [DEBUG] [sheets_writer] Writing 251 rows (including header)
2026-02-08 14:32:20.890 [DEBUG] [sheets_writer] Batch update successful
2026-02-08 14:32:21.000 [INFO] [sheets_writer] SYSTEM_STATUS updated
```

### Logging Configuration

**config/logging_config.yaml:**
```yaml
version: 1
formatters:
  standard:
    format: '%(asctime)s.%(msecs)03d [%(levelname)s] [%(name)s] %(message)s'
    datefmt: '%Y-%m-%d %H:%M:%S'

handlers:
  console:
    class: logging.StreamHandler
    formatter: standard
    level: INFO
    
  app_file:
    class: logging.handlers.RotatingFileHandler
    filename: logs/app.log
    maxBytes: 10485760  # 10MB
    backupCount: 5
    formatter: standard
    level: INFO
    
  nse_file:
    class: logging.handlers.RotatingFileHandler
    filename: logs/nse_api.log
    maxBytes: 10485760
    backupCount: 3
    formatter: standard
    level: DEBUG
    
  sheets_file:
    class: logging.handlers.RotatingFileHandler
    filename: logs/sheets.log
    maxBytes: 10485760
    backupCount: 3
    formatter: standard
    level: DEBUG

loggers:
  nse_fetcher:
    handlers: [nse_file, console]
    level: DEBUG
    propagate: no
    
  sheets_writer:
    handlers: [sheets_file, console]
    level: DEBUG
    propagate: no
    
  sheets_reader:
    handlers: [sheets_file, console]
    level: DEBUG
    propagate: no

root:
  handlers: [app_file, console]
  level: INFO
```

---

## 8. Configuration Management

### config/settings.yaml

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
  spreadsheet_id: "YOUR_SPREADSHEET_ID_HERE"
  poll_interval_seconds: 5
  
  # Sheet names (must match Google Sheet tab names)
  sheet_names:
    raw_data: "RAW_DATA"
    custom_view: "CUSTOM_VIEW"
    charts: "DELIVERY_CHARTS"
    system_status: "SYSTEM_STATUS"
  
  # Cell locations in CUSTOM_VIEW sheet
  control_cells:
    symbol: "B2"
    from_date: "B3"
    to_date: "B4"
    trigger: "B5"

# Data Storage
data:
  folder: "data"
  cleanup_enabled: true
  max_age_hours: 24
  filename_pattern: "{symbol}_{from_date}_{to_date}.csv"

# Logging
logging:
  config_file: "config/logging_config.yaml"
  
# System
system:
  shutdown_timeout_seconds: 10
```

---

## 9. Dependency Management

### requirements.txt

```
# Core dependencies
requests==2.31.0
pandas==2.1.4
gspread==5.12.0
oauth2client==4.1.3
PyYAML==6.0.1

# Utilities
python-dateutil==2.8.2

# Development (optional)
pytest==7.4.3
black==23.12.1
flake8==6.1.0
```

**Installation:**
```bash
pip install -r requirements.txt
```

---

## 10. Testing Strategy

### Unit Tests (Suggested, Not Auto-Generated)

**tests/test_data_processor.py:**
```python
def test_calculate_delivery_percentage():
    # Test delivery percentage calculation
    pass

def test_handle_missing_values():
    # Test NaN handling
    pass
```

**tests/test_nse_fetcher.py:**
```python
def test_build_api_params():
    # Test parameter construction
    pass

def test_validate_csv_response():
    # Test CSV vs HTML detection
    pass
```

**Critical Test Areas:**
- Date parsing and validation
- Delivery percentage calculation
- CSV format detection
- Error handling paths

**Non-Critical (Skip):**
- Integration tests requiring live NSE API
- Google Sheets API mocking (too complex)
- End-to-end tests (manual verification better)

---

## 11. Concurrency Model

### Threading Strategy

**Main Thread:**
- Runs monitoring loop
- Checks trigger every 5 seconds
- Executes pipeline sequentially

**No Worker Threads:**
- Pipeline runs in main thread
- Simpler than thread pool
- Prevents concurrent runs

**Future Enhancement (If Needed):**
```python
# If multiple concurrent pipelines needed
import threading
import queue

pipeline_queue = queue.Queue()
worker_thread = threading.Thread(target=process_queue, args=(pipeline_queue,))
worker_thread.start()
```

**Rationale:** Current design favors simplicity. One pipeline at a time is sufficient.

---

## 12. Shutdown Handling

### Graceful Shutdown

**utils.py:**
```python
import signal
import sys

shutdown_flag = False

def register_shutdown_handlers():
    signal.signal(signal.SIGTERM, _shutdown_handler)
    signal.signal(signal.SIGINT, _shutdown_handler)

def _shutdown_handler(signum, frame):
    global shutdown_flag
    shutdown_flag = True
    logging.info("Shutdown signal received, stopping gracefully...")

def is_shutdown_requested():
    return shutdown_flag
```

**sheets_reader.py:**
```python
def start_monitoring_loop(config):
    while not is_shutdown_requested():
        # ... monitoring logic
        time.sleep(config['poll_interval_seconds'])
    
    logging.info("Monitoring loop stopped")
```

---

## 13. Design Compliance Checklist

✅ **Entry Point (main.py):**
- [ ] No function definitions
- [ ] No class definitions
- [ ] No business logic
- [ ] Linear top-to-bottom execution
- [ ] Only calls module entry points

✅ **Modules:**
- [ ] Each module has one responsibility
- [ ] Expose clear entry-point functions
- [ ] No side effects at import
- [ ] Self-contained error handling

✅ **Functions:**
- [ ] One function = one task
- [ ] No god functions
- [ ] Flat control flow
- [ ] Minimal nesting
- [ ] Readable top-down

✅ **Logging:**
- [ ] Persistent log files
- [ ] Sub-second timestamps
- [ ] Multiple log files for separation
- [ ] No debug spam
- [ ] Production-quality comments

✅ **Error Handling:**
- [ ] Fail fast, explicitly
- [ ] Custom exceptions for realistic failures
- [ ] No swallowed exceptions

---

## 14. Code Review Guidelines

When reviewing code against this design:

**Red Flags:**
- Function > 30 lines (likely doing too much)
- Nested if/else > 2 levels deep
- Business logic in main.py
- Import-time side effects
- Generic exception catching without re-raise
- Comments referring to "the LLM" or "we discussed"

**Green Flags:**
- Short, single-purpose functions
- Clear function names describing action
- Consistent error handling patterns
- Minimal dependencies between modules
- Easy to trace execution flow

---

## 15. Future Modular Extensions

If new features are added, create new modules:

**modules/alert_sender.py** (Email/Slack alerts)
```python
def send_delivery_spike_alert(symbol, delivery_pct, threshold)
```

**modules/multi_symbol_processor.py** (Batch processing)
```python
def process_multiple_symbols(symbols, from_date, to_date)
```

**modules/database_writer.py** (Persist to DB)
```python
def store_historical_data(processed_data, db_connection)
```

**Principle:** Each new responsibility gets its own module

---

**End of Modular Design Document**