import os
import json

def log_symbolic_event(log_entry):
    """
    Save a log entry as a timestamped JSON file inside the /logs directory.
    """
    os.makedirs("logs", exist_ok=True)

    timestamp = log_entry.get("timestamp", "unknown")
    symbol = log_entry.get("symbol_value", "unknown")

    # Clean filename of characters that can't be used in filenames
    safe_symbol = "".join(c if c.isalnum() or c in (" ", "_") else "_" for c in symbol)
    filename = f"logs/{safe_symbol}_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(log_entry, f, indent=2)

