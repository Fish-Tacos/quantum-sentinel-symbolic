import csv
import json
from datetime import datetime
import os
import math

LOG_DIR = "logs"
CSV_PATH = os.path.join(LOG_DIR, "symbolic_log.csv")
JSON_PATH = os.path.join(LOG_DIR, "symbolic_log.json")
os.makedirs(LOG_DIR, exist_ok=True)

FIELDNAMES = [
    "timestamp", "symbol_type", "symbol_value",
    "input_params", "result_raw", "anomaly_detected", "observer_notes",
    "auto_symbolic_metadata"
]

def get_auto_symbolic_metadata():
    today = datetime.utcnow().date()
    day_of_year = today.timetuple().tm_yday

    def is_fibonacci(n):
        def is_perfect_square(x):
            s = int(math.sqrt(x))
            return s * s == x
        return is_perfect_square(5 * n * n + 4) or is_perfect_square(5 * n * n - 4)

    def moon_phase(date):
        known_new_moon = datetime(2000, 1, 6).date()
        days_since = (date - known_new_moon).days
        return round((days_since % 29.53) / 29.53, 2)

    intervals = [
        "Perfect Fifth", "Minor Third", "Major Sixth", "Tritone",
        "Minor Seventh", "Perfect Fourth", "Major Third"
    ]
    symbolic_music = intervals[today.weekday()]

    return {
        "date": today.isoformat(),
        "day_of_year": day_of_year,
        "is_fibonacci_day": is_fibonacci(day_of_year),
        "moon_phase_cycle": moon_phase(today),
        "symbolic_music_interval": symbolic_music
    }

def update_symbolic_resonance_tracker(entry):
    tracker_path = "symbolic_resonance_tracker.json"
    if not os.path.exists(tracker_path):
        return  # Tracker not initialized

    with open(tracker_path, "r", encoding="utf-8") as f:
        tracker = json.load(f)

    symbols = tracker.get("known_resonant_symbols", [])
    freq_map = tracker.get("symbol_frequency_map", {})
    anomaly_map = tracker.get("symbol_anomaly_map", {})
    strength_scores = tracker.get("symbol_strength_scores", {})

    symbol = entry.get("symbol_value")
    if symbol:
        freq_map[symbol] = freq_map.get(symbol, 0) + 1
        if entry.get("anomaly_detected"):
            anomaly_map[symbol] = anomaly_map.get(symbol, 0) + 1

        strength = anomaly_map.get(symbol, 0) / max(1, freq_map.get(symbol, 0))
        strength_scores[symbol] = round(strength, 3)

    tracker["symbol_frequency_map"] = freq_map
    tracker["symbol_anomaly_map"] = anomaly_map
    tracker["symbol_strength_scores"] = strength_scores

    with open(tracker_path, "w", encoding="utf-8") as f:
        json.dump(tracker, f, indent=2)

def log_symbolic_event(entry):
    entry["auto_symbolic_metadata"] = get_auto_symbolic_metadata()
    write_csv(entry)
    write_json(entry)
    update_symbolic_resonance_tracker(entry)
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
        csv_entry["auto_symbolic_metadata"] = json.dumps(csv_entry["auto_symbolic_metadata"])
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
