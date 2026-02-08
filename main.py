"""
NSE Equity Delivery Analytics System

"""

from modules import init_state, setup_logging, lifecycle, monitor
import logging

# ---------------------------------------------------------------------
# Step 1: Initialize Universal State
# ---------------------------------------------------------------------
state = init_state()

# ---------------------------------------------------------------------
# Step 2: Setup Logging System
# ---------------------------------------------------------------------
setup_logging(state["config"])

# ---------------------------------------------------------------------
# Step 3: Log System Start
# ---------------------------------------------------------------------
logger = logging.getLogger("main")
logger.info("=" * 60)
logger.info("NSE Equity Delivery Analytics System - STARTING")
logger.info("=" * 60)

# ---------------------------------------------------------------------
# Step 4: Register Shutdown Handlers
# ---------------------------------------------------------------------
lifecycle.register_shutdown_handlers(state)

# ---------------------------------------------------------------------
# Step 5: Connect to Google Sheets
# ---------------------------------------------------------------------
monitor.connect_sheets(state)

# ---------------------------------------------------------------------
# Step 6: Start Monitoring Loop
# ---------------------------------------------------------------------
logger.info("Entering monitoring loop...")
monitor.poll_loop(state)

# ---------------------------------------------------------------------
# Step 7: Graceful Shutdown
# ---------------------------------------------------------------------
logger.info("=" * 60)
logger.info("NSE Equity Delivery Analytics System - SHUTDOWN COMPLETE")
logger.info("=" * 60)