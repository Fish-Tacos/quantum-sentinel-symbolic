#!/usr/bin/env python3
import os, sys, json, pathlib, datetime as dt, requests
REPO = "Fish-Tacos/quantum-sentinel-symbolic"
OWNER, NAME = REPO.split("/")
TOKEN = os.getenv("GITHUB_TOKEN")
HEAD = {"Authorization": f"Bearer {TOKEN}", "X-GitHub-Api-Version":"2022-11-28"}
FAILS = []

def check_wf(file):
    url = f"https://api.github.com/repos/{OWNER}/{NAME}/actions/workflows/{file}/runs?per_page=1"
    try:
        r = requests.get(url, headers=HEAD, timeout=30).json()
        runs = r.get("workflow_runs", [])
        if not runs:
            FAILS.append(f"no runs for {file}")
            return
        if runs[0].get("conclusion") != "success":
            FAILS.append(f"last run of {file}: {runs[0].get('conclusion')}")
    except Exception as e:
        FAILS.append(f"workflow {file} error: {e}")

# 1) workflows green
for wf in ["symbolic_logger_daily.yml","uptime.yml","anomaly.yml"]:
    check_wf(wf)

# 2) uptime threshold
try:
    st = json.load(open("status/uptime.json"))
    if float(st.get("uptime_pct",0)) < float(os.getenv("UPTIME_MIN","90")):
        FAILS.append(f"uptime below threshold: {st.get('uptime_pct')}")
except Exception as e:
    FAILS.append(f"status/uptime.json missing or invalid: {e}")

# 3) log freshness (tolerate entries missing 'ts')
from pathlib import Path

SYMBOLIC_LOG = Path("data/logs/symbolic_log.json")
WARN_HOURS = 24       # print a warning if stale
HARD_FAIL_HOURS = 72  # fail only if older than this

try:
    sl = json.loads(SYMBOLIC_LOG.read_text())
    # accept dict or {"entries": [...]} style
    entries = sl.get("entries", sl) if isinstance(sl, dict) else sl

    ts_list = []
    for e in entries:
        if isinstance(e, dict) and "ts" in e:
            ts_list.append(e["ts"])

    if ts_list:
        ts_last = max(ts_list)
        # support iso8601 or epoch seconds
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

# 4) anomalies present
if not pathlib.Path("docs/anomalies.json").exists():
    FAILS.append("docs/anomalies.json missing")

# 5) prereg present
if not pathlib.Path("preregister/2025-08-pilot-01.md").exists():
    FAILS.append("preregister/2025-08-pilot-01.md missing")

if FAILS:
    print("READINESS CHECK: FAIL\n- " + "\n- ".join(FAILS))
    sys.exit(1)
print("READINESS CHECK: OK")
