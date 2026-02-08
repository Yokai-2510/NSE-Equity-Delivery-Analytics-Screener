"""
CSV passthrough processor.
Reads CSV, prepares raw data for Google Sheets, and calculates delivery metrics.
"""

import logging
from pathlib import Path
import pandas as pd


class ProcessorError(Exception):
    pass


def process_csv(state: dict) -> None:
    """
    Load CSV, dump it to state['transaction']['raw_data'], and calculate metrics.
    """
    logger = logging.getLogger("processor")

    csv_path = state["transaction"].get("csv_path")

    if not csv_path or not Path(csv_path).exists():
        raise ProcessorError("CSV file not found")

    logger.info(f"Processing CSV: {Path(csv_path).name}")

    try:
        df = pd.read_csv(csv_path)

        if df.empty:
            logger.warning("CSV has headers but no rows")

        # Convert dataframe to list-of-lists for Sheets
        header = df.columns.tolist()
        rows = df.values.tolist()

        raw_data = [header] + rows

        state["transaction"]["raw_data"] = raw_data

        # --------------------------------------------------
        # Calculate actual delivery metrics
        # --------------------------------------------------
        metrics = {
            "total_rows": len(rows),
            "avg_delivery_pct": 0,
            "max_delivery_pct": 0,
            "min_delivery_pct": 0,
        }

        # Find delivery % column (usually last column or "% Dly Qt to Traded Qty")
        delivery_col = None
        for idx, col in enumerate(header):
            if "%" in col.lower() and ("dly" in col.lower() or "delivery" in col.lower()):
                delivery_col = idx
                break

        if delivery_col is not None and len(rows) > 0:
            # Extract delivery % values
            delivery_values = []
            for row in rows:
                try:
                    val = float(row[delivery_col])
                    delivery_values.append(val)
                except (ValueError, TypeError, IndexError):
                    continue

            if delivery_values:
                metrics["avg_delivery_pct"] = round(sum(delivery_values) / len(delivery_values), 2)
                metrics["max_delivery_pct"] = round(max(delivery_values), 2)
                metrics["min_delivery_pct"] = round(min(delivery_values), 2)

        state["transaction"]["metrics"] = metrics

        logger.info(f"CSV processed: {len(rows)} rows | Avg Delivery: {metrics['avg_delivery_pct']}%")

        # --------------------------------------------------
        # Cleanup old CSV files
        # --------------------------------------------------
        _cleanup_old_csvs(state, csv_path)

    except Exception as e:
        raise ProcessorError(f"Failed to process CSV: {e}")


def _cleanup_old_csvs(state: dict, current_csv: Path) -> None:
    """
    Delete all CSV files in data folder except:
    - The current CSV just downloaded
    - nse_equity_list.CSV
    """
    logger = logging.getLogger("processor")

    data_folder = Path(state["config"]["data"]["folder"])

    if not data_folder.exists():
        return

    # Files to preserve
    preserve_files = {
        current_csv.name,
        "nse_equity_list.CSV",
        "nse_equity_list.csv"  # Case-insensitive match
    }

    deleted_count = 0

    for file in data_folder.glob("*.csv"):
        if file.name not in preserve_files and file.name.lower() not in {f.lower() for f in preserve_files}:
            try:
                file.unlink()
                deleted_count += 1
                logger.debug(f"Deleted old CSV: {file.name}")
            except Exception as e:
                logger.warning(f"Failed to delete {file.name}: {e}")

    # Also delete .CSV files
    for file in data_folder.glob("*.CSV"):
        if file.name not in preserve_files:
            try:
                file.unlink()
                deleted_count += 1
                logger.debug(f"Deleted old CSV: {file.name}")
            except Exception as e:
                logger.warning(f"Failed to delete {file.name}: {e}")

    if deleted_count > 0:
        logger.info(f"🗑️  Cleaned up {deleted_count} old CSV file(s)")