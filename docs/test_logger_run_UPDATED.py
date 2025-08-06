from logger_with_symbol_learning import log_symbolic_event
from datetime import datetime

# 1. Spiral Symbol
log_entry = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "symbol_type": "Natural Pattern",
    "symbol_value": "Spiral",
    "input_params": {"shots": 1024, "test_mode": True},
    "result_raw": {"0": 523, "1": 501},
    "anomaly_detected": False,
    "observer_notes": "Occurs in galaxies and shells"
}
log_symbolic_event(log_entry)

# 2. Comet ATLAS 3I
log_entry = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "symbol_type": "Celestial Event",
    "symbol_value": "Comet ATLAS 3I",
    "input_params": {"shots": 1024, "test_mode": True},
    "result_raw": {"0": 516, "1": 508},
    "anomaly_detected": False,
    "observer_notes": "Comet is near Earth; potential resonance cue"
}
log_symbolic_event(log_entry)

# 3. Triskelion Symbol
log_entry = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "symbol_type": "Ancient Symbol",
    "symbol_value": "Triskelion",
    "input_params": {"shots": 1024, "test_mode": True},
    "result_raw": {"0": 510, "1": 514},
    "anomaly_detected": False,
    "observer_notes": "Symbol tied to motion, cycles, and resonance"
}
log_symbolic_event(log_entry)
