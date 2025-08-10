# test_logger_run.py
# Uses the archiving-enabled logger (Step 3.4)

from datetime import datetime
from logger_with_symbolic_inference import log_symbolic_event

def make_entry(symbol_type, symbol_value, notes, result_raw):
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "symbol_type": symbol_type,
        "symbol_value": symbol_value,
        "input_params": {"shots": 1024, "test_mode": True},
        "result_raw": result_raw,
        "anomaly_detected": False,
        "observer_notes": notes,
    }

if __name__ == "__main__":
    # 1) Natural Pattern — Spiral
    log_symbolic_event(
        make_entry(
            symbol_type="Natural Pattern",
            symbol_value="Spiral",
            notes="Occurs in galaxies and shells",
            result_raw={"0": 523, "1": 501},
        )
    )

    # 2) Celestial Event — Comet ATLAS 3I
    log_symbolic_event(
        make_entry(
            symbol_type="Celestial Event",
            symbol_value="Comet ATLAS 3I",
            notes="Comet is near Earth; potential resonance cue",
            result_raw={"0": 516, "1": 508},
        )
    )

    # 3) Ancient Symbol — Triskelion
    log_symbolic_event(
        make_entry(
            symbol_type="Ancient Symbol",
            symbol_value="Triskelion",
            notes="Symbol tied to motion, cycles, and resonance",
            result_raw={"0": 510, "1": 514},
        )
    )
