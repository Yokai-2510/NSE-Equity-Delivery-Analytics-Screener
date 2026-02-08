"""
System lifecycle management - Signal handlers and graceful shutdown.
"""

import signal
import logging


def register_shutdown_handlers(state: dict) -> None:
    """
    Register SIGINT and SIGTERM handlers to enable graceful shutdown.
    
    Sets state['resources']['shutdown_flag'] = True when triggered.
    """
    logger = logging.getLogger("lifecycle")
    
    def shutdown_handler(signum, frame):
        sig_name = signal.Signals(signum).name
        logger.warning(f"Received {sig_name} - initiating graceful shutdown")
        state["resources"]["shutdown_flag"] = True
    
    # Register handlers
    signal.signal(signal.SIGINT, shutdown_handler)   # Ctrl+C
    signal.signal(signal.SIGTERM, shutdown_handler)  # kill command
    
    logger.info("Shutdown handlers registered (SIGINT, SIGTERM)")


def is_running(state: dict) -> bool:
    """
    Check if system should continue running.
    
    Returns False when shutdown has been requested.
    """
    return not state["resources"]["shutdown_flag"]


def initiate_shutdown(state: dict, reason: str = "Manual trigger") -> None:
    """
    Manually trigger shutdown from within the application.
    """
    logger = logging.getLogger("lifecycle")
    logger.warning(f"Shutdown initiated: {reason}")
    state["resources"]["shutdown_flag"] = True