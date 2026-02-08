import time
import logging
from modules.utils import is_shutdown_requested

def start_monitoring_loop(config: dict) -> None:
    """
    Main monitoring loop - polls Google Sheets every N seconds.
    Runs indefinitely until shutdown signal.
    """
    logger = logging.getLogger("sheets_reader")
    poll_interval = config['google_sheets']['poll_interval_seconds']
    
    logger.info(f"Monitoring loop started. Polling every {poll_interval} seconds.")
    
    # This is the 'Blocking' loop mentioned in the design
    while not is_shutdown_requested():
        try:
            # Placeholder for Phase 2 Logic:
            # 1. Check Trigger
            # 2. Fetch Data
            # 3. Update Sheets
            logger.debug("Heartbeat: Checking for trigger...")
            
            time.sleep(poll_interval)
            
        except Exception as e:
            logger.error(f"Error in monitoring loop: {e}", exc_info=True)
            time.sleep(poll_interval)  # Prevent tight loop on error

    logger.info("Monitoring loop stopped gracefully.")