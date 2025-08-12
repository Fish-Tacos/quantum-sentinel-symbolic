import csv
import json
from datetime import datetime
import os

LOG_DIR = "logs"
CSV_PATH = os.path.join(LOG_DIR, "symbolic_log.csv")
JSON_PATH = os.path.join(LOG_DIR, "symbolic_log.json")

os.makedirs(LOG_DIR, exist_ok=True)

FIELDNAMES = [
    "timestamp", "symbol_type", "symbol_value",
    "input_params", "result_raw", "anomaly_detected", "observer_notes"
]

def log_symbolic_event(entry):
    write_csv(entry)
    write_json(entry)
    print(f"[LOGGED] Entry recorded at {entry['timestamp']}")

def write_csv(entry):
    write_header = not os.path.exists(CSV_PATH)
    with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()
        csv_entry = entry.copy()
        csv_entry["input_params"] = json.dumps(csv_entry["input_params"])
        csv_entry["result_raw"] = json.dumps(csv_entry["result_raw"])
        writer.writerow(csv_entry)

def write_json(entry):
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def safe_json_input(prompt):
    while True:
        try:
            raw = input(prompt)
            return json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON. Try again. Error: {e}")

def main():
    print("\n🚀 Quantum Watchtower Interactive Logger")
    print("Enter symbolic observation details below:\n")

    symbol_type = input("Enter symbol type (e.g. Fibonacci, Full Moon, Music): ").strip()
    symbol_value = input("Enter symbol value (e.g. 21, 2025-07-20): ").strip()
    input_params = safe_json_input("Enter input_params as JSON (e.g. {\"shots\": 1024, \"gate\": \"H\"}): ")
    result_raw = safe_json_input("Enter result_raw as JSON (e.g. {\"0\": 600, \"1\": 424}): ")
    
    anomaly_str = input("Anomaly detected? (yes/no or 0–1 score): ").strip().lower()
    if anomaly_str in ['yes', 'y', 'true']:
        anomaly_detected = True
    elif anomaly_str in ['no', 'n', 'false']:
        anomaly_detected = False
    else:
        try:
            anomaly_detected = float(anomaly_str)
        except ValueError:
            anomaly_detected = None
    
    observer_notes = input("Enter any observer notes: ").strip()
    
    timestamp = datetime.utcnow().isoformat() + "Z"

    entry = {
        "timestamp": timestamp,
        "symbol_type": symbol_type,
        "symbol_value": symbol_value,
        "input_params": input_params,
        "result_raw": result_raw,
        "anomaly_detected": anomaly_detected,
        "observer_notes": observer_notes
    }

    log_symbolic_event(entry)

if __name__ == "__main__":
    main()
