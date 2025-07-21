import streamlit as st
import os
import csv
import json
from datetime import datetime
import pandas as pd

# Paths
LOG_DIR = "logs"
CSV_PATH = os.path.join(LOG_DIR, "symbolic_log.csv")
JSON_PATH = os.path.join(LOG_DIR, "symbolic_log.json")

FIELDNAMES = [
    "timestamp", "symbol_types", "symbol_values",
    "input_params", "result_raw", "anomaly_detected", "observer_notes"
]

os.makedirs(LOG_DIR, exist_ok=True)

# Logging Functions
def write_csv(entry):
    write_header = not os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()
        csv_entry = entry.copy()
        csv_entry["input_params"] = json.dumps(csv_entry["input_params"])
        csv_entry["result_raw"] = json.dumps(csv_entry["result_raw"])
        csv_entry["symbol_types"] = json.dumps(csv_entry["symbol_types"])
        csv_entry["symbol_values"] = json.dumps(csv_entry["symbol_values"])
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

def log_symbolic_event(entry):
    write_csv(entry)
    write_json(entry)

def load_log():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        return df
    return pd.DataFrame(columns=FIELDNAMES)

def is_anomaly(value):
    if isinstance(value, bool):
        return value
    try:
        return float(value) > 0.7
    except:
        return False

# UI Setup
st.set_page_config(page_title="Quantum Watchtower V3", layout="centered")
st.title("🔬 Quantum Watchtower — Multi-Symbol Logger")

symbol_options = [
    "Fibonacci", "Full Moon", "Music", "Golden Ratio", "Prime Number",
    "Dream", "Synchronicity", "Numerology", "Planetary Alignment", "Other"
]

symbol_value_menus = {
    "Fibonacci": [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144],
    "Full Moon": "date",
    "Music": ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"],
    "Golden Ratio": ["1.618", "0.618", "1.0"],
    "Prime Number": [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31],
    "Numerology": list(range(1, 10)) + [11, 22, 33],
    "Dream": "text",
    "Synchronicity": "text",
    "Planetary Alignment": ["Conjunction", "Opposition", "Retrograde", "Transit"],
    "Other": "text"
}

# Entry Form
with st.form("symbolic_log_form"):
    st.subheader("📅 Symbol Entry")
    symbol_types = st.multiselect("Select Symbol Types", options=symbol_options, default=["Fibonacci"])
    symbol_values = []

    for sym in symbol_types:
        st.markdown(f"**{sym} Value**")
        menu = symbol_value_menus.get(sym)
        if menu == "text":
            val = st.text_input(f"{sym} Description", key=sym)
        elif menu == "date":
            val = st.date_input(f"{sym} Date", key=sym).isoformat()
        else:
            val = st.selectbox(f"{sym} Options", options=menu, key=sym)
        symbol_values.append(val)

    input_params_str = st.text_area("Input Params (JSON)", value='{"shots": 1024, "gate": "H"}')
    result_raw_str = st.text_area("Result Raw (JSON)", value='{"0": 600, "1": 424}')

    anomaly_choice = st.radio("Anomaly Detected?", ["No", "Yes", "Score (enter below)"])
    anomaly_score = st.text_input("Anomaly Score (optional)", placeholder="0.85 if not Yes/No")
    notes = st.text_area("Observer Notes")

    submitted = st.form_submit_button("Log Symbolic Event")

    if submitted:
        try:
            input_params = json.loads(input_params_str)
            result_raw = json.loads(result_raw_str)
        except json.JSONDecodeError as e:
            st.error(f"JSON error: {e}")
            st.stop()

        if anomaly_choice == "Yes":
            anomaly = True
        elif anomaly_choice == "No":
            anomaly = False
        else:
            try:
                anomaly = float(anomaly_score)
            except ValueError:
                anomaly = None

        timestamp = datetime.utcnow().isoformat() + "Z"

        entry = {
            "timestamp": timestamp,
            "symbol_types": symbol_types,
            "symbol_values": symbol_values,
            "input_params": input_params,
            "result_raw": result_raw,
            "anomaly_detected": anomaly,
            "observer_notes": notes
        }

        log_symbolic_event(entry)
        st.success(f"✅ Logged at {timestamp}")

# Analysis Section
df = load_log()
if not df.empty:
    st.markdown("---")
    st.subheader("📊 Timeline of Symbolic Logs")
    df['date'] = df['timestamp'].dt.date
    chart_data = df.groupby('date').size().rename("Entries").reset_index()
    st.line_chart(chart_data, x="date", y="Entries")

    st.markdown("---")
    st.subheader("🧠 Recent Entries")

    for _, row in df.sort_values("timestamp", ascending=False).head(10).iterrows():
        anomaly_flag = is_anomaly(row["anomaly_detected"])
        color = "red" if anomaly_flag else "green"
        symbols = ", ".join(json.loads(row["symbol_types"]))
        values = ", ".join(map(str, json.loads(row["symbol_values"])))
        st.markdown(f"""
        <div style='border-left: 5px solid {color}; padding: 0.5em 1em; margin-bottom: 0.5em;'>
        <strong>{row['timestamp']}</strong><br>
        <b>Symbols:</b> {symbols} → <code>{values}</code><br>
        <b>Anomaly:</b> {row['anomaly_detected']}<br>
        <b>Notes:</b> {row['observer_notes']}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No logs yet. Enter your first symbolic resonance event.")
