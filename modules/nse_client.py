"""
NSE Historical Data Fetcher - SACRED CODE
DO NOT MODIFY THE FETCH SEQUENCE - This is the only version that works.
"""

import requests
import logging
import sys
from pathlib import Path

# Allow standalone execution
if __name__ == "__main__":
    sys.path.append(str(Path(__file__).parent.parent))

from modules.utils import load_config, setup_logging


class NSEFetchError(Exception):
    """Raised when NSE data fetch fails"""
    pass


def fetch_csv(state: dict) -> Path:
    """
    Download historical CSV from NSE using the HOLY GRAIL sequence.
    
    Updates state['transaction']['csv_path'] on success.
    Raises NSEFetchError on failure.
    
    CRITICAL: Do not modify headers or request sequence.
    """
    logger = logging.getLogger("nse_client")
    
    # Extract from state
    symbol = state["transaction"]["symbol"]
    from_date = state["transaction"]["from_date"]
    to_date = state["transaction"]["to_date"]
    
    config = state["config"]
    nse_config = config["nse"]
    data_config = config["data"]
    
    logger.info(f"Fetching NSE data: {symbol} ({from_date} → {to_date})")
    
    # Prepare output path
    data_folder = Path(data_config["folder"])
    data_folder.mkdir(parents=True, exist_ok=True)
    
    # Build filename
    filename = data_config["filename_pattern"].format(
        symbol=symbol,
        from_date=from_date.replace("-", ""),
        to_date=to_date.replace("-", "")
    )
    csv_path = data_folder / filename
    
    # HOLY GRAIL FETCH SEQUENCE - DO NOT MODIFY
    try:
        session = requests.Session()
        
        # Sacred headers that work
        session.headers.update(nse_config["headers"])
        
        # Step 1: Homepage hit for cookies (MANDATORY - don't check response)
        logger.debug("Acquiring NSE cookies...")
        session.get("https://www.nseindia.com", timeout=10)
        
        # Step 2: API call with params
        api_url = "https://www.nseindia.com/api/historicalOR/generateSecurityWiseHistoricalData"
        
        params = {
            "from": from_date,
            "to": to_date,
            "symbol": symbol.upper(),
            "type": "priceVolumeDeliverable",
            "series": "ALL",
            "csv": "true"
        }
        
        logger.debug(f"Calling NSE API with params: {params}")
        
        api_response = session.get(
            api_url,
            params=params,
            timeout=20
        )
        
        # Check for common failures
        if api_response.status_code == 403:
            raise NSEFetchError("403 Forbidden - NSE blocked the request")
        
        if api_response.status_code == 404:
            raise NSEFetchError(f"404 Not Found - Invalid symbol or date range")
        
        api_response.raise_for_status()
        
        # Verify we got CSV, not HTML error page
        content_preview = api_response.content[:100].lower()
        if b"<html" in content_preview or b"<!doctype" in content_preview:
            raise NSEFetchError("Received HTML instead of CSV (possible error page)")
        
        # Save to disk
        csv_path.write_bytes(api_response.content)
        
        logger.info(f"CSV saved: {csv_path.name} ({csv_path.stat().st_size} bytes)")
        
        # Update state
        state["transaction"]["csv_path"] = csv_path
        
        return csv_path
        
    except requests.exceptions.Timeout:
        raise NSEFetchError("Request timed out after 20s")
    
    except requests.exceptions.RequestException as e:
        raise NSEFetchError(f"Network error: {e}")
    
    except Exception as e:
        raise NSEFetchError(f"Unexpected error: {e}")


# ---------------------------------------------------------------------
# Manual Testing
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("NSE Client - Manual Test Mode")
    print("=" * 60)
    
    # Load config
    config = load_config()
    setup_logging(config)
    
    logger = logging.getLogger("nse_client")
    
    # Build a minimal state dict for testing
    project_config = config["project"]
    
    test_state = {
        "config": config,
        "transaction": {
            "symbol": project_config["instrument"]["symbol"],
            "from_date": project_config["date_range"]["from_date"],
            "to_date": project_config["date_range"]["to_date"],
            "csv_path": None
        }
    }
    
    print(f"\nTest Parameters:")
    print(f"  Symbol:     {test_state['transaction']['symbol']}")
    print(f"  From Date:  {test_state['transaction']['from_date']}")
    print(f"  To Date:    {test_state['transaction']['to_date']}")
    print(f"\nFetching data...\n")
    
    try:
        csv_path = fetch_csv(test_state)
        print(f"\n{'=' * 60}")
        print(f"✅ SUCCESS")
        print(f"{'=' * 60}")
        print(f"File saved: {csv_path}")
        print(f"File size:  {csv_path.stat().st_size:,} bytes")
        print(f"Updated state path: {test_state['transaction']['csv_path']}")
        
    except NSEFetchError as e:
        print(f"\n{'=' * 60}")
        print(f"❌ FETCH FAILED")
        print(f"{'=' * 60}")
        print(f"Error: {e}")
        logger.error(f"Manual test failed: {e}")
        sys.exit(1)