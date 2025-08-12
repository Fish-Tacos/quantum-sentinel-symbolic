## 🧠 Simulator-Ready Symbolic Notebooks

This repository now includes updated notebooks and logging logic designed for symbolic anomaly detection using quantum simulations.

### ✅ Features Added
- **AerSimulator Support**:
  - All quantum circuits now run on `qiskit_aer.AerSimulator()` with proper transpilation.
  - Compatible with Qiskit ≥ 1.0.

- **Impulse-Based Symbolic Logging**:
  - Each notebook run ends with a symbolic logger prompt.
  - Captures observer notes, raw counts, and system parameters.

- **Automatic Symbolic Context Detection**:
  - Background logging of:
    - Moon phase (as lunar cycle fraction)
    - Fibonacci alignment (is today a Fibonacci-numbered day?)
    - Symbolic musical interval (assigned by weekday)

- **Dual-Format Log Output**:
  - `logs/symbolic_log.csv` and `logs/symbolic_log.json`
  - Ready for downstream statistical or symbolic analysis

### 📄 Files to Explore
- `qs_phase2_1_bell_state_generation_2025_06_22_SIMULATOR_READY_WITH_LOGGER.ipynb`
- `qs_phase2.6_symbolic_scheduler_pilot_SIMULATOR_READY_WITH_LOGGER.ipynb`
- `logger_with_symbolic_inference.py`
