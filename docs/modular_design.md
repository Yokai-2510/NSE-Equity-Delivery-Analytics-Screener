nse-delivery-analytics/
│
├── main.py                    # Entry point (linear orchestrator only)
├── requirements.txt
├── README.md
│
├── config/                    # Configuration & credentials
│   ├── settings.yaml          # NSE URLs, sheet IDs, date formats
│   ├── credentials.json       # Google Sheets service account key
│   └── symbols.json           # Optional: symbol validation list
│
├── modules/                   # Core business logic
│   ├── nse_fetcher.py         # NSE API interaction
│   ├── sheets_reader.py       # Read user inputs from Google Sheets
│   ├── sheets_writer.py       # Write data to all 4 sheets
│   ├── data_processor.py      # CSV parsing, validation, metrics calculation
│   └── utils.py               # Common functions (logging, date parsing, retries)
│
└── data/                      # Downloaded CSV storage
    └── .gitkeep               # (CSVs deleted after processing)