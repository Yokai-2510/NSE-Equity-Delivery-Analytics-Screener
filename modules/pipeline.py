"""
Pipeline orchestrator - Executes single fetch-process-write cycle.
"""

import logging

from modules import nse_client, processor, sheets_io, state
from modules.utils import cleanup_old_files


def run(state_dict: dict) -> None:
    """
    Execute full pipeline for one transaction:
    1. Fetch CSV from NSE
    2. Process data (placeholder for now)
    3. Write to Google Sheets (placeholder for now)
    4. Reset transaction state
    5. Cleanup old files
    
    Handles errors gracefully and ensures transaction reset.
    """
    logger = logging.getLogger("pipeline")
    
    symbol = state_dict["transaction"]["symbol"]
    logger.info(f"Pipeline started for {symbol}")
    
    try:
        # -------------------------------------------------------------
        # Stage 1: Fetch Data
        # -------------------------------------------------------------
        state.update_stage(state_dict, "FETCHING")
        nse_client.fetch_csv(state_dict)
        logger.info("✓ Fetch complete")
        
        # -------------------------------------------------------------
        # Stage 2: Process Data
        # -------------------------------------------------------------
        state.update_stage(state_dict, "PROCESSING")
        processor.process_csv(state_dict)
        logger.info("✓ Processing complete")
        
        # -------------------------------------------------------------
        # Stage 3: Write to Sheets
        # -------------------------------------------------------------
        state.update_stage(state_dict, "WRITING")
        sheets_io.write_results(state_dict)
        logger.info("✓ Write complete")
        
        logger.info(f"Pipeline completed successfully for {symbol}")
        
    except nse_client.NSEFetchError as e:
        error_msg = f"NSE fetch failed: {e}"
        logger.error(error_msg)
        state.set_error(state_dict, error_msg)
        sheets_io.write_error(state_dict)
        
    except Exception as e:
        error_msg = f"Pipeline error: {e}"
        logger.error(error_msg)
        state.set_error(state_dict, error_msg)
        sheets_io.write_error(state_dict)
        
    finally:
        # Always reset transaction state
        state.reset_transaction(state_dict)
        
        # Cleanup old CSV files if enabled
        config = state_dict["config"]
        data_config = config["data"]
        
        if data_config.get("cleanup_enabled", True):
            max_age = data_config.get("max_age_hours", 24)
            deleted = cleanup_old_files(data_config["folder"], max_age)
            if deleted > 0:
                logger.info(f"Cleaned up {deleted} old CSV file(s)")