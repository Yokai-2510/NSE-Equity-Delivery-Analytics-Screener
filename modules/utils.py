import yaml
import logging
import logging.config
import signal
import time
import functools
import re
import os
from pathlib import Path
from typing import Dict, Any, Callable, Tuple
from datetime import datetime, timedelta

# Global flag for shutdown
_SHUTDOWN_FLAG = False

# --------------------------------------------------------------------------
# Configuration & Logging
# --------------------------------------------------------------------------

def load_config(config_path: str = "config/settings.yaml") -> Dict[str, Any]:
    """Load application configuration from YAML file."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path.absolute()}")
        
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def setup_logging(config_path: str = "config/logging_config.yaml") -> None:
    """Configure logging based on YAML configuration."""
    path = Path(config_path)
    Path("logs").mkdir(exist_ok=True)
    
    if path.exists():
        with open(path, 'r') as f:
            try:
                config = yaml.safe_load(f)
                logging.config.dictConfig(config)
                return
            except Exception as e:
                print(f"Failed to load logging config: {e}")
    
    # Fallback
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# --------------------------------------------------------------------------
# Date & Input Validation
# --------------------------------------------------------------------------

def parse_date_string(date_str: str, fmt: str = "%d-%m-%Y") -> datetime:
    """Strictly parse a date string."""
    try:
        return datetime.strptime(date_str, fmt)
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Expected {fmt}")

def format_date_for_nse(date_obj: datetime) -> str:
    """Convert datetime to NSE API format (DD-MM-YYYY)."""
    return date_obj.strftime("%d-%m-%Y")

def validate_symbol(symbol: str) -> bool:
    """
    Check if symbol format is valid.
    Rules: Uppercase, Alphanumeric, 1-20 chars.
    """
    if not symbol or not isinstance(symbol, str):
        return False
    return bool(re.match(r'^[A-Z0-9]{1,20}$', symbol))

def validate_date_range(from_date: str, to_date: str) -> Tuple[bool, str]:
    """
    Validate date logical consistency.
    Returns: (is_valid, error_message)
    """
    try:
        start = parse_date_string(from_date)
        end = parse_date_string(to_date)
        
        if start > end:
            return False, "From Date cannot be after To Date"
        
        if end > datetime.now() + timedelta(days=1):
            return False, "Cannot fetch data for future dates"
            
        if (end - start).days > 365:
            return False, "Date range exceeds 1 year limit"
            
        return True, ""
    except ValueError as e:
        return False, str(e)

# --------------------------------------------------------------------------
# File & System Operations
# --------------------------------------------------------------------------

def cleanup_old_csvs(data_folder: str, max_age_hours: int = 24) -> int:
    """
    Delete CSV files older than specified hours.
    Returns count of deleted files.
    """
    folder = Path(data_folder)
    if not folder.exists():
        return 0
    
    deleted_count = 0
    cutoff_time = time.time() - (max_age_hours * 3600)
    
    for file_path in folder.glob("*.csv"):
        if file_path.stat().st_mtime < cutoff_time:
            try:
                file_path.unlink()
                deleted_count += 1
                logging.getLogger("utils").debug(f"Deleted old file: {file_path.name}")
            except Exception as e:
                logging.getLogger("utils").error(f"Failed to delete {file_path.name}: {e}")
                
    return deleted_count

def retry_on_failure(max_retries: int = 3, delay: int = 2):
    """Decorator to retry operations on exception."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logging.getLogger("utils").warning(
                        f"Attempt {attempt}/{max_retries} failed for {func.__name__}: {e}. Retrying in {delay}s..."
                    )
                    time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

# --------------------------------------------------------------------------
# Signal Handling
# --------------------------------------------------------------------------

def register_shutdown_handlers() -> None:
    signal.signal(signal.SIGINT, _shutdown_handler)
    signal.signal(signal.SIGTERM, _shutdown_handler)

def _shutdown_handler(signum, frame) -> None:
    global _SHUTDOWN_FLAG
    _SHUTDOWN_FLAG = True
    logging.getLogger("utils").info("Shutdown signal received.")

def is_shutdown_requested() -> bool:
    return _SHUTDOWN_FLAG