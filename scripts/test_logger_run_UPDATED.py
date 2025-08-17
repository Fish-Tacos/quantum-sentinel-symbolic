from datetime import datetime
import os
import json

# 1. Spiral Symbol
log_entry_1 = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "symbol_type": "Natural Pattern",
    "symbol_value": "Spiral",
    "input_params": {"shots": 1024, "test_mode": True},
    "result_raw": {"r0": 523, "r1": 501},
    "anomaly_detected": False,
    "observer_notes": "Occurs in galaxies and shells"
}

# 2. Comet ATLAS 3I
log_entry_2 = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "symbol_type": "Celestial Event",
    "symbol_value": "Comet ATLAS 3I",
    "input_params": {"shots": 1024, "test_mode": True},
    "result_raw": {"r0": 516, "r1": 508},
    "anomaly_detected": False,
    "observer_notes": "Comet is near Earth; potential resonance cue"
}

# 3. Triskelion Symbol
log_entry_3 = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "symbol_type": "Ancient Symbol",
    "symbol_value": "Triskelion",
    "input_params": {"shots": 1024, "test_mode": True},
    "result_raw": {"r0": 510, "r1": 514},
    "anomaly_detected": False,
    "observer_notes": "Symbol tied to motion, cycles, and resonance"
}

# Combine all logs
log_entries = [log_entry_1, log_entry_2, log_entry_3]

# Save to logs/symbolic_log.json
os.makedirs("logs", exist_ok=True)
with open("logs/symbolic_log.json", "w") as f:
    json.dump(log_entries, f, indent=2)
