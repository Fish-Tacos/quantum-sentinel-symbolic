import os
import json

def log_symbolic_event(log_entry):
    """
    Save a log entry to a cumulative log file AND 
    save an individual timestamped file in /logs (with safe filename).
    """
    os.makedirs("logs", exist_ok=True)
    os.makedirs("logs/archive", exist_ok=True)

    # Get values
    timestamp = log_entry.get("timestamp", "unknown")
    symbol = log_entry.get("symbol_value", "unknown")

    # Clean timestamp for filename: replace ':' with '-'
    safe_timestamp = timestamp.replace(":", "-")

    # Clean symbol for filename: alphanumeric and safe characters only
    safe_symbol = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in symbol)

    # File paths
    archive_path = f"logs/archive/{safe_symbol}_{safe_timestamp}.json"
    cumulative_path = "logs/symbolic_log.json"

    # Write individual archive file
    with open(archive_path, "w") as f:
        json.dump(log_entry, f, indent=2)

    # Append to cumulative log
    cumulative_data = []
    if os.path.exists(cumulative_path):
        with open(cumulative_path, "r") as f:
            cumulative_data = json.load(f)

    cumulative_data.append(log_entry)

    with open(cumulative_path, "w") as f:
        json.dump(cumulative_data, f, indent=2)
