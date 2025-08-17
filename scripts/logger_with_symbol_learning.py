import os
import json
import csv
from datetime import datetime

def log_symbolic_event(log_entry):
    """
    Save a log entry in:
    1. Timestamped JSON file in daily archive
    2. symbolic_log.json (latest log for GitHub artifact)
    3. symbolic_log_cumulative.jsonl (appended JSONL log)
    4. symbolic_log_cumulative.csv (updated CSV)
    """

    # Create log directories
    os.makedirs("logs", exist_ok=True)
    archive_dir = f"logs/archive/{datetime.utcnow().date()}"
    os.makedirs(archive_dir, exist_ok=True)

    # Extract core info
    timestamp = log_entry.get("timestamp", datetime.utcnow().isoformat() + "Z")
    symbol = log_entry.get("symbol_value", "unknown")

    # Sanitize filename symbol
    safe_symbol = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in symbol)

    # File paths
    filename_archive = f"{archive_dir}/{safe_symbol}_{timestamp}.json"
    filename_latest = "logs/symbolic_log.json"
    filename_jsonl = "logs/symbolic_log_cumulative.jsonl"
    filename_csv = "logs/symbolic_log_cumulative.csv"

    # 1. Save archive log
    with open(filename_archive, "w") as f:
        json.dump(log_entry, f, indent=2)

    # 2. Save latest single log
    with open(filename_latest, "w") as f:
        json.dump(log_entry, f, indent=2)

    # 3. Append to JSONL
    with open(filename_jsonl, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    # 4. Append to CSV
    fieldnames = [
        "timestamp", "symbol_type", "symbol_value",
        "input_params", "result_raw", "anomaly_detected", "observer_notes"
    ]
    file_exists = os.path.isfile(filename_csv)
    with open(filename_csv, "a", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        # Flatten nested dicts for CSV
        flat_entry = {
            "timestamp": log_entry.get("timestamp", ""),
            "symbol_type": log_entry.get("symbol_type", ""),
            "symbol_value": log_entry.get("symbol_value", ""),
            "input_params": json.dumps(log_entry.get("input_params", {})),
            "result_raw": json.dumps(log_entry.get("result_raw", {})),
            "anomaly_detected": log_entry.get("anomaly_detected", False),
            "observer_notes": log_entry.get("observer_notes", "")
        }

        writer.writerow(flat_entry)
