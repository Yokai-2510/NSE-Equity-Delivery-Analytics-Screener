import requests
from pathlib import Path

URL = "https://www.nseindia.com/api/historicalOR/generateSecurityWiseHistoricalData"

PARAMS = {
    "from": "08-02-2025",
    "to": "08-02-2026",
    "symbol": "RELIANCE",
    "type": "priceVolumeDeliverable",
    "series": "ALL",
    "csv": "true",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/report-detail/eq_security",
    "X-Requested-With": "XMLHttpRequest",
}

def download_csv():
    session = requests.Session()
    session.headers.update(HEADERS)

    # 🔑 Step 1: hit homepage to get cookies (mandatory)
    session.get("https://www.nseindia.com", timeout=10)

    # 🔑 Step 2: actual API call
    r = session.get(URL, params=PARAMS, timeout=20)
    r.raise_for_status()

    out = Path("INFY_historical.csv")
    out.write_bytes(r.content)
    print(f"Saved → {out.resolve()}")

if __name__ == "__main__":
    download_csv()
