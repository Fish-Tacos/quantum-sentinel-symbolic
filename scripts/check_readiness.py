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
try:
    raw = json.load(open("data/logs/symbolic_log.json"))
    entries = raw.get("entries", []) if isinstance(raw, dict) else raw
    ts_values = [e["ts"] for e in entries if isinstance(e, dict) and "ts" in e]
    if not ts_values:
        raise ValueError("no entries with 'ts'")
    last_ts = max(ts_values)
    t = dt.datetime.strptime(last_ts, "%Y-%m-%dT%H:%M:%SZ")
    if (dt.datetime.utcnow()-t).total_seconds() > 24*3600:
        FAILS.append("data/logs/symbolic_log.json not updated in last 24h")
except Exception as e:
    FAILS.append(f"data/logs/symbolic_log.json issue: {e}")

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
