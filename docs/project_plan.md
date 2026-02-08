This project plan is structured strictly according to the **LLM Python Coding Style & Execution Specification (v3)**.

The architecture separates concerns into explicit modules, ensuring `main.py` remains a linear orchestrator. We will build this incrementally.

---

# 📅 Project Plan: NSE Equity Delivery Analytics

## Phase 0: Environment & Repository Structure
**Goal:** Initialize the project skeleton, dependencies, and version control.

1.  **Directory Setup:** Create the following structure (enforcing separation of concerns):
    ```text
    nse-analytics/
    ├── config/                 # YAML settings & JSON credentials
    ├── data/                   # Temporary CSV storage
    ├── logs/                   # Persistent logs
    ├── modules/                # Business logic (No god functions)
    │   ├── __init__.py
    │   ├── utils.py            # Config loader & Logger setup
    │   ├── sheets_api.py       # Reader/Writer for Google Sheets
    │   ├── nse_client.py       # API Cookie handling & Fetching
    │   └── processor.py        # Pandas logic & calculations
    ├── main.py                 # Linear Orchestrator
    ├── requirements.txt        # Dependencies
    └── .gitignore              # Security (ignore credentials)
    ```
2.  **Virtual Environment:** Setup Python `venv`.
3.  **Dependencies:** Define `requirements.txt` (requests, pandas, gspread, pyyaml).
4.  **Git Initialization:** Initialize repo and configure `.gitignore` to strictly exclude `config/credentials.json` and `logs/*.log`.

**Verification:** Project structure exists, `pip install` works, and imports don't crash.

---

## Phase 1: Configuration & Logging Infrastructure
**Goal:** Establish the system's nervous system. Logic must not be hardcoded.

1.  **Settings Module (`modules/utils.py`):**
    *   Create `load_config()` to read `config/settings.yaml`.
    *   Create `setup_logger()` to handle file + console logging with sub-second timestamps.
2.  **Configuration File (`config/settings.yaml`):**
    *   Define NSE URLs, Sheet ID, polling intervals, and file paths.
3.  **Logging Config:**
    *   Ensure logs are structured (e.g., `[INFO] [NSE_CLIENT] Message`).

**Verification:** Run a test script that loads config and writes a "System Start" log entry to `logs/app.log`.

---

## Phase 2: Google Sheets Connection & Symbol List
**Goal:** Connect to the UI and populate the "Search/Menu Box" requested.

1.  **Authentication (`modules/sheets_api.py`):**
    *   Implement `get_client()` using `gspread` and `oauth2client`.
2.  **Symbol List Fetcher (The "Menu Box" feature):**
    *   Implement a function to fetch the master equity list (`EQUITY_L.csv`) from NSE.
    *   Implement logic to upload this list to a hidden sheet (e.g., `VALIDATION_DATA`).
    *   *Note:* In Google Sheets, we will set Data Validation on the Input Cell to reference this hidden range, creating a searchable dropdown.
3.  **Input Reader:**
    *   Implement `read_user_input()` to fetch Symbol, Date Range, and Trigger status.

**Verification:** The Python script successfully updates a cell in the sheet and populates the "Symbol" dropdown menu.

---

## Phase 3: NSE Data Acquisition (The Fetcher)
**Goal:** robust data downloading with cookie handling.

1.  **Session Management (`modules/nse_client.py`):**
    *   Implement `create_session()`: Hits homepage first to establish cookies/headers.
2.  **Historical Data Fetch:**
    *   Implement `fetch_historical_csv(symbol, from_date, to_date)`:
    *   Uses the specific API endpoint: `/api/historicalOR/generateSecurityWiseHistoricalData`.
    *   Saves raw CSV to `data/` folder.
3.  **Rate Limiting:**
    *   Implement simple sleep logic to prevent 403/429 errors.

**Verification:** Provide "RELIANCE" and a date range; script downloads a valid CSV to `data/RELIANCE_historical.csv`.

---

## Phase 4: Data Processing
**Goal:** Transform raw CSV into analytical data.

1.  **CSV Parsing (`modules/processor.py`):**
    *   Implement `clean_dataframe(csv_path)`:
        *   Parse dates to standard format.
        *   Ensure numeric columns are actually numeric.
2.  **Metrics Calculation:**
    *   Implement `calculate_delivery_metrics(df)`:
        *   Check for `Deliverable Qty` vs `Traded Qty`.
        *   Calculate percentages.
3.  **Formatting:**
    *   Prepare data as a list of lists (JSON-serializable) for Google Sheets upload.

**Verification:** Script reads the raw CSV from Phase 3 and prints a clean Pandas DataFrame summary to the console.

---

## Phase 5: Orchestration (The Main Loop)
**Goal:** Tie everything together in `main.py` according to LLM Guidelines (Linear Flow).

1.  **Linear Orchestrator (`main.py`):**
    *   Import all modules.
    *   Initialize Config & Logging.
    *   Enter `while True:` loop (if polling) or single run.
    *   Step 1: `sheets_api.check_trigger()`
    *   Step 2: If trigger == True -> `nse_client.fetch(...)`
    *   Step 3: `processor.process(...)`
    *   Step 4: `sheets_api.write_results(...)`
    *   Step 5: `sheets_api.reset_trigger()`
2.  **Error Handling:**
    *   Wrap steps in `try/except` to log errors to `logs/app.log` without crashing the process.

**Verification:** Full end-to-end run. User clicks checkbox in Sheets -> Python detects -> Data downloads -> Sheets updates.

---

## Phase 6: Deployment & Cleanup
**Goal:** Make it production-ready.

1.  **Cleanup:** Auto-delete old CSVs from `data/`.
2.  **Startup Scripts:** Create `run.bat` (Windows) or `run.sh` (Linux/Mac).
3.  **Documentation:** Finalize `README.md` with setup instructions.

---

### Immediate Next Step
I will begin **Phase 0** immediately to establish the folder structure and environment.

**Shall I proceed with creating the directory structure and the `requirements.txt`?**