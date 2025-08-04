from logger_with_symbolic_inference import log_symbolic_event
from datetime import datetime

log_entry = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "symbol_type": "Test Run",
    "symbol_value": "2025-08-03",
    "input_params": {"shots": 1024, "test_mode": True},
    "result_raw": {"0": 512, "1": 512},
    "anomaly_detected": False,
    "observer_notes": "Sanity check for logger functionality."
}

log_symbolic_event(log_entry)
