"""
Utility functions for config loading and logging setup.
"""

import json
import logging
from pathlib import Path
from datetime import datetime


def load_config(config_path: str = "config/settings.json") -> dict:
    """
    Load JSON configuration file.
    Returns the entire config dict.
    """
    path = Path(config_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def setup_logging(config: dict) -> None:
    """
    Configure file and console logging with sub-second timestamps.
    """
    log_config = config.get("logging", {})
    log_level = log_config.get("level", "INFO")
    log_file = log_config.get("file", "logs/app.log")
    console_enabled = log_config.get("console", True)
    
    # Ensure log directory exists
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Custom format with sub-second precision
    log_format = "%(asctime)s.%(msecs)03d [%(levelname)s] [%(name)s] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=[]
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    logging.getLogger().addHandler(file_handler)
    
    # Console handler (optional)
    if console_enabled:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_format, date_format))
        logging.getLogger().addHandler(console_handler)


def format_date_for_display(date_str: str) -> str:
    """
    Convert DD-MM-YYYY to a readable format.
    Example: "08-02-2025" -> "08 Feb 2025"
    """
    try:
        dt = datetime.strptime(date_str, "%d-%m-%Y")
        return dt.strftime("%d %b %Y")
    except ValueError:
        return date_str  # Return as-is if parsing fails


def validate_date_format(date_str: str) -> bool:
    """
    Check if date string matches DD-MM-YYYY format.
    """
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
        return True
    except ValueError:
        return False


def cleanup_old_files(folder: str, max_age_hours: int = 24) -> int:
    """
    Delete files older than max_age_hours from the specified folder.
    
    Returns count of deleted files.
    """
    import time
    
    folder_path = Path(folder)
    if not folder_path.exists():
        return 0
    
    now = time.time()
    max_age_seconds = max_age_hours * 3600
    deleted_count = 0
    
    for file_path in folder_path.glob("*.csv"):
        if file_path.is_file():
            age_seconds = now - file_path.stat().st_mtime
            if age_seconds > max_age_seconds:
                file_path.unlink()
                deleted_count += 1
                logging.getLogger("utils").debug(f"Deleted old file: {file_path.name}")
    
    return deleted_count