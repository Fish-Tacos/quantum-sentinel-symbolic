import os
import json

def log_symbolic_event(log_entry):
    """
    Save a log entry as both a timestamped JSON file 
    and a standardized file (symbolic_log.json) for GitHub artifact upload.
    """
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    # Extract fields
    timestamp = log_entry.get("timestamp", "unknown")
    symbol = log_entry.get("symbol_value", "unknown")

    # Clean filename: remove unsafe characters
    safe_symbol = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in symbol)
    filename_timestamped = f"logs/{safe_symbol}_{timestamp}.json"
    filename_latest = "logs/symbolic_log.json"

    # Save timestamped version
    with open(filename_timestamped, "w") as f:
        json.dump(log_entry, f, indent=2)

    # Save latest version for artifact collection
    with open(filename_latest, "w") as f:
        json.dump(log_entry, f, indent=2)
