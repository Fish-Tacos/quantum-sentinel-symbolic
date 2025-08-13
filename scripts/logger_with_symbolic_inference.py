import os
import csv
import json
from datetime import datetime, timezone
import argparse
import shutil

# -----------------------------
# Paths (absolute, always within repo root)
# -----------------------------
# __file__ is ...\quantum-sentinel-symbolic\scripts\logger_with_symbolic_inference.py
# One dirname => scripts; two dirnames => repo root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
LOG_DIR = os.path.join(BASE_DIR, "data", "logs")
CSV_PATH = os.path.join(LOG_DIR, "symbolic_log.csv")
JSON_PATH = os.path.join(LOG_DIR, "symbolic_log.json")
SNAPSHOT_STEM = "symbolic_log"

os.makedirs(LOG_DIR, exist_ok=True)

# -----------------------------
# Unified schema
# -----------------------------
FIELDNAMES = [
    "timestamp",                 # ISO 8601 local time
    "symbol_type",
    "symbol_value",
    "input_params",              # JSON
    "result_raw",                # JSON
    "anomaly_detected",          # bool
    "observer_notes",
    "auto_symbolic_metadata"     # JSON
]

# -----------------------------
# Auto symbolic metadata
# -----------------------------
def _is_fibonacci_day(day_of_year: int) -> bool:
    a, b = 1, 1
    while a < 400:
        if a == day_of_year:
            return True
        a, b = b, a + b
    return False

def _moon_phase_cycle(date: datetime) -> float:
    """Approximate moon phase as a fraction [0..1)."""
    synodic = 29.53058867
    epoch = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    days = (date.astimezone(timezone.utc) - epoch).total_seconds() / 86400.0
    return (days % synodic) / synodic

def _symbolic_music_interval(weekday: int) -> str:
    intervals = [
        "Perfect Fifth", "Minor Third", "Major Sixth", "Tritone",
        "Minor Seventh", "Perfect Fourth", "Major Third"
    ]
    return intervals[weekday % len(intervals)]

def get_auto_symbolic_metadata() -> dict:
    now_local = datetime.now().astimezone()
    doy = int(now_local.strftime("%j"))
    return {
        "date": now_local.date().isoformat(),
        "day_of_year": doy,
        "is_fibonacci_day": _is_fibonacci_day(doy),
        "moon_phase_cycle": round(_moon_phase_cycle(now_local), 4),
        "symbolic_music_interval": _symbolic_music_interval(now_local.weekday())
    }

# -----------------------------
# I/O helpers
# -----------------------------
def _json_dump(obj) -> str:
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False)

def write_csv(entry: dict):
    write_header = not os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if write_header:
            w.writeheader()
        row = entry.copy()
        row["input_params"] = _json_dump(entry.get("input_params", {}))
        row["result_raw"] = _json_dump(entry.get("result_raw", {}))
        row["auto_symbolic_metadata"] = _json_dump(entry.get("auto_symbolic_metadata", {}))
        w.writerow(row)

def write_json(entry: dict):
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []
    else:
        data = []
    data.append(entry)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def snapshot_logs():
    """
    Create timestamped copies of current CSV/JSON in data/logs and
    return the absolute paths of the snapshots that were created.
    """
    ts = datetime.now().astimezone().strftime("%Y-%m-%d_%H-%M-%S")
    csv_snap = None
    json_snap = None
    if os.path.exists(CSV_PATH):
        csv_snap = os.path.join(LOG_DIR, f"{SNAPSHOT_STEM}_{ts}.csv")
        shutil.copyfile(CSV_PATH, csv_snap)
    if os.path.exists(JSON_PATH):
        json_snap = os.path.join(LOG_DIR, f"{SNAPSHOT_STEM}_{ts}.json")
        shutil.copyfile(JSON_PATH, json_snap)
    return csv_snap, json_snap

# -----------------------------
# API
# -----------------------------
def log_symbolic_event(partial: dict) -> dict:
    entry = {
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "symbol_type": partial.get("symbol_type", ""),
        "symbol_value": partial.get("symbol_value", ""),
        "input_params": partial.get("input_params", {}),
        "result_raw": partial.get("result_raw", {}),
        "anomaly_detected": bool(partial.get("anomaly_detected", False)),
        "observer_notes": partial.get("observer_notes", ""),
        "auto_symbolic_metadata": get_auto_symbolic_metadata(),
    }
    write_csv(entry)
    write_json(entry)
    return entry

# -----------------------------
# CLI
# -----------------------------
def _parse_args():
    p = argparse.ArgumentParser(description="Quantum Sentinel logger (local-time, snapshots, metadata-only).")
    p.add_argument("--symbol-type", default="Test")
    p.add_argument("--symbol-value", default="Manual Run")
    p.add_argument("--observer-notes", default="Manual Step 3.4 Test")
    p.add_argument("--metadata-only", action="store_true",
                   help="If set, omit quantum result payloads.")
    p.add_argument("--shots", type=int, default=512,
                   help="Included in input_params if not metadata-only.")
    return p.parse_args()

def main():
    args = _parse_args()
    input_params = {"shots": args.shots} if not args.metadata_only else {}
    result_raw = {"0": args.shots // 2, "1": args.shots // 2} if not args.metadata_only else {}

    entry = log_symbolic_event({
        "symbol_type": args.symbol_type,
        "symbol_value": args.symbol_value,
        "input_params": input_params,
        "result_raw": result_raw,
        "anomaly_detected": False,
        "observer_notes": args.observer_notes
    })

    csv_snap, json_snap = snapshot_logs()

    # Console confirmations with absolute paths
    print(f"[OK] Logged at {entry['timestamp']} | meta: {_json_dump(entry['auto_symbolic_metadata'])}")
    print(f"[PATH] Rolling CSV: {os.path.abspath(CSV_PATH)}")
    print(f"[PATH] Rolling JSON: {os.path.abspath(JSON_PATH)}")
    if csv_snap:
        print(f"[SNAP] CSV snapshot:  {os.path.abspath(csv_snap)}")
    if json_snap:
        print(f"[SNAP] JSON snapshot: {os.path.abspath(json_snap)}")

if __name__ == "__main__":
    main()
