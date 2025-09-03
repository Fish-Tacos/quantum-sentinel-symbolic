#!/usr/bin/env python3
import os, sys, json, pathlib, requests
from datetime import datetime as dt
from pathlib import Path

OWNER, NAME = os.environ.get("GITHUB_REPOSITORY", "OWNER/NAME").split("/")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEAD = {"Authorization": f"Bearer {TOKEN}", "X-GitHub-Api-Version": "2022-11-28"}
FAILS = []


def check_wf(file):
    """Check last run status of a workflow file in GitHub Actions"""
    uri = f"https://api.github.com/repos/{OWNER}/{NAME}/actions/workflows/{file}/runs?per_page=1"
    try:
        r = requests.get(uri, headers=HEAD, timeout=30).json()
        runs = r.get("workflow_runs", [])
        if not runs:
            FAILS.append(f"No runs for {file}")
            return
        if runs[0].get("conclusion") != "success":
            FAILS.append(f"Last run of {file}: {runs[0].get('conclusion')}")
    except Exception as e:
        FAILS.append(f"Workflow ({file}) error: {e}")


# --- 1) Check key workflows ---
for wf in ["symbolic_logger_daily.yml", "uptime.yml", "anomaly.yml"]:
    check_wf(wf)


# --- 2) uptime threshold ---
try:
    st = json.load(open("status/uptime.json"))
    if float(st.get("uptime_pct", 0)) < float(os.getenv("UPTIME_MIN", "90")):
        FAILS.append(f"Uptime below threshold: {st.get('uptime_pct')}")
except Exception as e:
    FAILS.append(f"status/uptime.json missing or invalid: {e}")


# --- 3) log freshness (tolerate entries missing 'ts') ---
SYMBOLIC_LOG = Path("data/logs/symbolic_log.json")
WARN_HOURS = 24       # print a warning if stale
HARD_FAIL_HOURS = 72  # fail only if older than this

try:
    sl = json.loads(SYMBOLIC_LOG.read_text())
    entries = sl.get("entries", sl) if isinstance(sl, dict) else sl

    ts_list = []
    for e in entries:
        if isinstance(e, dict) and "ts" in e:
            ts_list.append(e["ts"])

    if ts_list:
        ts_last = max(ts_list)
        # Support ISO8601 or epoch seconds
        if isinstance(ts_last, str):
            dt_last = dt.fromisoformat(ts_last.replace("Z", "+00:00")).astimezone()
        else:
            dt_last = dt.fromtimestamp(float(ts_last)).astimezone()

        age_h = (dt.now().astimezone() - dt_last).total_seconds() / 3600.0

        if age_h > HARD_FAIL_HOURS:
            FAILS.append(f"{SYMBOLIC_LOG} age {age_h:.1f}h > {HARD_FAIL_HOURS}h")
        elif age_h > WARN_HOURS:
            print(f"READINESS CHECK: WARN - {SYMBOLIC_LOG} age {age_h:.1f}h > {WARN_HOURS}h")
    else:
        FAILS.append(f"{SYMBOLIC_LOG} has no usable timestamps")
except Exception as e:
    FAILS.append(f"{SYMBOLIC_LOG} issue: {e}")


# --- 4) anomalies file present ---
if not Path("docs/anomalies.json").exists():
    FAILS.append("docs/anomalies.json missing")


# --- 5) preregister milestone present ---
if not Path("preregister/2025-08-pilot-01.md").exists():
    FAILS.append("preregister/2025-08-pilot-01.md missing")


# --- Final report ---
if FAILS:
    print("READINESS CHECK: FAIL - " + "; ".join(FAILS))
    sys.exit(1)
else:
    print("READINESS CHECK: OK")
