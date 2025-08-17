import os
import json
import shutil
from datetime import datetime

def log_symbolic_event(entry):
    log_path = "logs/symbolic_log.json"
    archive_dir = "logs/archive"
    
    # Ensure both logs/ and logs/archive/ directories exist
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    os.makedirs(archive_dir, exist_ok=True)

    # Backup existing log before writing new data
    if os.path.exists(log_path):
        timestamp = datetime.utcnow().isoformat().replace(":", "-").replace(".", "-")
        backup_filename = f"symbolic_log_{timestamp}.json"
        backup_path = os.path.join(archive_dir, backup_filename)
        shutil.copy2(log_path, backup_path)

    # Load existing log if it exists
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Append new entry and save log
    data.append(entry)
    with open(log_path, "w") as f:
        json.dump(data, f, indent=4)

