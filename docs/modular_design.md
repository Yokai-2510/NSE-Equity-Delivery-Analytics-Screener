# NSE Equity Delivery Analytics - Modular Design

**Version:** 2.0  
**Date:** February 8, 2026

---

## 1. Project Structure

```
nse-analytics/
├── main.py                    # Linear orchestrator (no logic)
├── requirements.txt           # requests, pandas, gspread, oauth2client
├── config/
│   ├── settings.json         # App config (NSE URLs, polling interval, paths)
│   └── credentials.json      # Google service account key
├── data/                     # Temp CSV storage (auto-cleanup)
├── logs/                     # app.log (timestamp + tags)
└── modules/
    ├── __init__.py
    ├── state.py              # Universal dict init/reset
    ├── lifecycle.py          # Signal handlers, shutdown logic
    ├── monitor.py            # Poll Google Sheets for trigger
    ├── pipeline.py           # Execute single fetch-process-write cycle
    ├── nse_client.py         # THE HOLY GRAIL (cookie + CSV fetch)
    ├── processor.py          # Parse CSV, calc delivery %
    ├── sheets_io.py          # Read inputs, write outputs
    └── utils.py              # Date formatting, logging setup
```

---

## 2. The Universal State Dict

Single dict passed to all functions. Created once in `main.py`.

```python
state = {
    "config": {
        "nse_url": "...",
        "nse_api": "...",
        "sheet_id": "...",
        "poll_interval": 5,
        "data_folder": "./data",
        "log_folder": "./logs"
    },
    "resources": {
        "sheets_client": None,      # gspread client
        "spreadsheet": None,         # active spreadsheet
        "shutdown_flag": False       # toggled by SIGINT
    },
    "transaction": {                 # RESET after each pipeline run
        "symbol": None,
        "from_date": None,
        "to_date": None,
        "csv_path": None,
        "raw_data": [],              # list of lists for sheets
        "metrics": {},               # avg/max/min delivery
        "error": None
    }
}
```

---

## 3. Module Breakdown

### `modules/state.py`
```python
def init_state() -> dict
    # Load settings.json into state['config']
    # Return empty state dict

def reset_transaction(state: dict) -> None
    # Wipe state['transaction'] clean
```

### `modules/lifecycle.py`
```python
def setup_signals(state: dict) -> None
    # Register SIGINT/SIGTERM to set shutdown_flag=True

def is_running(state: dict) -> bool
    # Return not state['resources']['shutdown_flag']
```

### `modules/monitor.py`
```python
def connect_sheets(state: dict) -> None
    # Auth with credentials.json
    # Store client in state['resources']['sheets_client']

def poll_loop(state: dict) -> None
    # while is_running(state):
    #     if check_trigger(state):
    #         pipeline.run(state)
    #     sleep(poll_interval)

def check_trigger(state: dict) -> bool
    # Read CUSTOM_VIEW sheet
    # If checkbox=TRUE: load symbol/dates into state['transaction']
    # Return True/False
```

### `modules/nse_client.py` ⚠️ **SACRED CODE - DO NOT MODIFY**

```python
def fetch_csv(state: dict) -> Path:
    # Extract symbol, from_date, to_date from state['transaction']
    
    # HOLY GRAIL SEQUENCE (DO NOT ALTER):
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/report-detail/eq_security",
        "X-Requested-With": "XMLHttpRequest"
    })
    
    # Step 1: Homepage for cookies
    session.get("https://www.nseindia.com", timeout=10)
    
    # Step 2: API call
    params = {
        "from": from_date,
        "to": to_date,
        "symbol": symbol,
        "type": "priceVolumeDeliverable",
        "series": "ALL",
        "csv": "true"
    }
    r = session.get(NSE_API_URL, params=params, timeout=20)
    r.raise_for_status()
    
    # Save to data/ folder
    csv_path = Path(data_folder) / f"{symbol}_{from_date}_{to_date}.csv"
    csv_path.write_bytes(r.content)
    
    # Update state
    state['transaction']['csv_path'] = csv_path
    return csv_path
```

### `modules/processor.py`
```python
def process_csv(state: dict) -> None
    # Load CSV from state['transaction']['csv_path']
    # Parse dates, clean columns
    # Calculate Delivery % = (Deliverable Qty / Total Traded Qty) * 100
    # Compute metrics: avg, max, min delivery %
    # Store as list-of-lists in state['transaction']['raw_data']
    # Store metrics in state['transaction']['metrics']
```

### `modules/sheets_io.py`
```python
def write_results(state: dict) -> None
    # Bulk update RAW_DATA sheet with state['transaction']['raw_data']
    # Update SYSTEM_STATUS with last_update, symbol, metrics
    # Reset trigger checkbox to FALSE

def write_error(state: dict, error: str) -> None
    # Log error to SYSTEM_STATUS sheet
```

### `modules/pipeline.py`
```python
def run(state: dict) -> None
    # Linear execution:
    try:
        nse_client.fetch_csv(state)
        processor.process_csv(state)
        sheets_io.write_results(state)
    except Exception as e:
        state['transaction']['error'] = str(e)
        sheets_io.write_error(state, str(e))
    finally:
        state_module.reset_transaction(state)
        cleanup_old_csvs(state)
```

---

## 4. main.py (The Checklist)

```python
from modules import state, lifecycle, monitor

# 1. Initialize state
app_state = state.init_state()

# 2. Setup logging & signals
utils.setup_logging(app_state)
lifecycle.setup_signals(app_state)

# 3. Connect to Google Sheets
monitor.connect_sheets(app_state)

# 4. Run monitoring loop
monitor.poll_loop(app_state)
```

**Total lines:** ~10  
**Logic:** 0  
**Conditionals:** 0

---

## 5. settings.json Structure

```json
{
  "nse": {
    "base_url": "https://www.nseindia.com",
    "api_endpoint": "/api/historicalOR/generateSecurityWiseHistoricalData",
    "homepage": "https://www.nseindia.com",
    "timeout": 20
  },
  "sheets": {
    "spreadsheet_id": "1ABC...",
    "input_sheet": "CUSTOM_VIEW",
    "output_sheet": "RAW_DATA",
    "status_sheet": "SYSTEM_STATUS"
  },
  "polling": {
    "interval_seconds": 5
  },
  "paths": {
    "data_folder": "./data",
    "log_folder": "./logs"
  }
}
```

---

## 6. Key Design Principles

### ✅ Sacred Code Protection
- `nse_client.py` fetch logic is **LOCKED** - exact headers, exact sequence
- Any NSE failures → check if this code was modified

### ✅ State Isolation
- `reset_transaction()` called after EVERY pipeline run
- Ensures clean slate for next symbol

### ✅ No God Functions
- Each module has 2-4 focused functions
- `pipeline.run()` is the only orchestrator (besides `main.py`)

### ✅ Error Handling
- Errors logged to file + written to SYSTEM_STATUS sheet
- Pipeline continues after errors (doesn't crash monitor loop)

### ✅ Minimal Dependencies
- No YAML parser needed (pure JSON)
- No complex abstractions
- Standard library + 4 packages

---

## 7. Execution Flow

```
User checks box in Google Sheets
         ↓
monitor.check_trigger() detects it
         ↓
Loads symbol/dates into state['transaction']
         ↓
pipeline.run(state) executes:
    1. nse_client.fetch_csv(state)      → downloads CSV
    2. processor.process_csv(state)     → parses & calculates
    3. sheets_io.write_results(state)   → updates all sheets
    4. state.reset_transaction(state)   → wipes transaction data
         ↓
Loop continues polling every 5 seconds
```

---

## 8. What Changed from v1

| Old Design | New Design | Reason |
|------------|------------|--------|
| YAML config | JSON config | Simpler, no extra parser |
| Multiple state objects | Universal dict | Single source of truth |
| Separate logger module | utils.py | Too granular |
| Complex orchestrator | 3-step pipeline | Matches LLM guidelines |
| Untested NSE code | Holy grail script | **Working code locked in** |

---

## 9. Critical Success Factors

1. **DO NOT modify nse_client.py headers/sequence** - this is the only code that works
2. **DO reset transaction state** - prevents data leakage between runs
3. **DO use the universal dict** - no prop drilling, no hidden coupling
4. **DO keep main.py linear** - zero logic, just 4 function calls

---

**End of Modular Design Document**