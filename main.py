import logging
import time
from modules.utils import setup_logging, load_config, register_shutdown_handlers, is_shutdown_requested

def main():
        
    # 1. Setup Infrastructure
    setup_logging()
    logger = logging.getLogger("main")
    
    try:
        # 2. Load Configuration
        config = load_config()
        logger.info("Configuration loaded successfully.")
        
        # 3. Setup Signal Handlers
        register_shutdown_handlers()
        logger.info("Signal handlers registered. Press Ctrl+C to test shutdown.")
        
        # 4. Verify Settings (Print specific value to prove read worked)
        nse_url = config['nse']['base_url']
        sheet_id = config['google_sheets']['spreadsheet_id']
        logger.info(f"Target NSE URL: {nse_url}")
        logger.info(f"Target Sheet ID: {sheet_id}")
        
        # 5. Simple Keep-Alive Loop (Phase 1 Test)
        logger.info("Phase 1 System Check: Running... (Waiting for Ctrl+C)")
        
        while not is_shutdown_requested():
            time.sleep(1)
            
        logger.info("Main loop exited cleanly.")
        
    except Exception as e:
        logger.critical(f"Fatal startup error: {e}", exc_info=True)
        exit(1)

if __name__ == "__main__":
    main()