"""
Universal state dictionary initialization and management.
"""

import logging
from modules.utils import load_config


def init_state() -> dict:
    """
    Initialize the universal state dictionary.
    
    Returns a fresh state dict with:
    - config: Loaded from settings.json
    - resources: Empty slots for runtime objects
    - transaction: Clean slate for each pipeline run
    """
    logger = logging.getLogger("state")
    
    # Load configuration
    config = load_config()
    logger.info("Configuration loaded successfully")
    
    # Build the universal state structure
    state = {
        "config": config,
        
        "resources": {
            "sheets_client": None,      # gspread client object
            "spreadsheet": None,         # active spreadsheet object
            "http_session": None,        # reusable requests session (future)
            "shutdown_flag": False       # set by signal handlers
        },
        
        "transaction": {
            # User inputs
            "symbol": None,
            "from_date": None,
            "to_date": None,
            
            # File paths
            "csv_path": None,
            
            # Processed data
            "raw_data": [],              # List of lists for bulk sheet update
            "metrics": {},               # Summary stats (avg, max, min delivery %)
            
            # Status tracking
            "error": None,
            "stage": "IDLE"              # FETCHING -> PROCESSING -> WRITING -> IDLE
        }
    }
    
    logger.info("Universal state initialized")
    return state


def reset_transaction(state: dict) -> None:
    """
    Wipe transaction data clean for next pipeline run.
    
    Preserves config and resources.
    Called after each pipeline execution (success or failure).
    """
    logger = logging.getLogger("state")
    
    state["transaction"] = {
        "symbol": None,
        "from_date": None,
        "to_date": None,
        "csv_path": None,
        "raw_data": [],
        "metrics": {},
        "error": None,
        "stage": "IDLE"
    }
    
    logger.debug("Transaction state reset")


def update_stage(state: dict, stage: str) -> None:
    """
    Update the current pipeline stage for logging/monitoring.
    
    Valid stages: IDLE, FETCHING, PROCESSING, WRITING, ERROR
    """
    state["transaction"]["stage"] = stage
    logging.getLogger("state").debug(f"Stage: {stage}")


def set_error(state: dict, error: str) -> None:
    """
    Record an error in the transaction state.
    """
    state["transaction"]["error"] = error
    state["transaction"]["stage"] = "ERROR"
    logging.getLogger("state").error(f"Transaction error: {error}")