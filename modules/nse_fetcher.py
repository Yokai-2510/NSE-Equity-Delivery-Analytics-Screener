import requests
import logging
from pathlib import Path

# ---------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------
try:
    from modules.utils import load_config, setup_logging
except ImportError:
    import sys
    sys.path.append(str(Path(__file__).parent.parent))
    from modules.utils import load_config, setup_logging


# ---------------------------------------------------------------------
# Load Config
# ---------------------------------------------------------------------
CONFIG = load_config()

PROJECT_CONFIG = CONFIG["project"]
NSE_CONFIG = CONFIG["nse"]
DATA_CONFIG = CONFIG["data"]

# Project defaults
PROJECT_SYMBOL = PROJECT_CONFIG["instrument"]["symbol"]
PROJECT_SERIES = PROJECT_CONFIG["instrument"].get("series", "ALL")
FROM_DATE = PROJECT_CONFIG["date_range"]["from_date"]
TO_DATE = PROJECT_CONFIG["date_range"]["to_date"]

# NSE endpoints
NSE_BASE_URL = NSE_CONFIG["base_url"]
NSE_API_URL = NSE_BASE_URL + NSE_CONFIG["api_endpoint"]
NSE_HOMEPAGE = NSE_CONFIG["homepage_url"]
TIMEOUT = NSE_CONFIG.get("timeout_seconds", 20)

# Headers
API_HEADERS = NSE_CONFIG["headers"]

HOMEPAGE_HEADERS = {
    "User-Agent": API_HEADERS["User-Agent"],
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": API_HEADERS.get("Accept-Language", "en-US,en;q=0.9"),
}


# ---------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------
class NSEFetchError(Exception):
    pass


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------
def fetch_nse_historical_data(
    symbol: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
    data_folder: Path | None = None,
) -> Path:
    """
    Fetch NSE historical CSV.
    Falls back to project defaults if args not provided.
    """

    logger = logging.getLogger("nse_fetcher")

    symbol = (symbol or PROJECT_SYMBOL).upper().strip()
    from_date = from_date or FROM_DATE
    to_date = to_date or TO_DATE

    logger.info(f"Initiating fetch for {symbol}: {from_date} -> {to_date}")

    target_folder = data_folder or Path(DATA_CONFIG["folder"])
    target_folder.mkdir(parents=True, exist_ok=True)

    session = requests.Session()

    try:
        # -------------------------------------------------------------
        # Step 1: Homepage hit (clean headers)
        # -------------------------------------------------------------
        _acquire_nse_cookies(session)

        # -------------------------------------------------------------
        # Step 2: API call (AJAX headers)
        # -------------------------------------------------------------
        session.headers.update(API_HEADERS)

        params = {
            "from": from_date,
            "to": to_date,
            "symbol": symbol,
            "type": "priceVolumeDeliverable",
            "series": PROJECT_SERIES,
            "csv": "true",
        }

        content = _download_csv(session, params)

        path = _save_to_disk(
            content=content,
            symbol=symbol,
            from_date=from_date,
            to_date=to_date,
            folder=target_folder,
        )

        logger.info(f"Data saved successfully: {path}")
        return path

    except Exception as e:
        logger.error(f"NSE fetch failed for {symbol}: {e}")
        raise NSEFetchError(e) from e


# ---------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------
def _acquire_nse_cookies(session: requests.Session) -> None:
    """Single homepage visit to obtain cookies."""
    logger = logging.getLogger("nse_fetcher")
    logger.debug("Acquiring NSE cookies (homepage request)")

    r = session.get(
        NSE_HOMEPAGE,
        headers=HOMEPAGE_HEADERS,
        timeout=TIMEOUT,
        allow_redirects=True,
    )

    if r.status_code == 403:
        raise NSEFetchError("403 Forbidden on NSE homepage")

    r.raise_for_status()

    if not session.cookies:
        raise NSEFetchError("No cookies received from NSE homepage")


def _download_csv(session: requests.Session, params: dict) -> bytes:
    """Download CSV from NSE API."""
    logger = logging.getLogger("nse_fetcher")
    logger.debug(f"NSE API params: {params}")

    r = session.get(
        NSE_API_URL,
        params=params,
        timeout=TIMEOUT,
    )

    if r.status_code == 403:
        raise NSEFetchError("403 Forbidden on NSE API")
    if r.status_code == 404:
        raise NSEFetchError("404 Not Found")

    r.raise_for_status()

    snippet = r.content[:100].lower()
    if b"<html" in snippet or b"<!doctype" in snippet:
        raise NSEFetchError("HTML received instead of CSV")

    return r.content


def _save_to_disk(
    content: bytes,
    symbol: str,
    from_date: str,
    to_date: str,
    folder: Path,
) -> Path:
    filename = DATA_CONFIG["filename_pattern"].format(
        symbol=symbol,
        from_date=from_date.replace("-", ""),
        to_date=to_date.replace("-", ""),
    )

    path = folder / filename
    path.write_bytes(content)
    return path


# ---------------------------------------------------------------------
# Manual Execution
# ---------------------------------------------------------------------
if __name__ == "__main__":
    setup_logging()

    print(f"--- Running Manual Test for {PROJECT_SYMBOL} ---")

    try:
        p = fetch_nse_historical_data()
        print(f"\n✅ SUCCESS: {p}")
        print(f"File size: {p.stat().st_size} bytes")
    except Exception as e:
        print(f"\n❌ FAILURE: {e}")
