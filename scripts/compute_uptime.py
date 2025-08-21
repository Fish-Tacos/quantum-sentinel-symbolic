#!/usr/bin/env python3
import json, os, datetime as dt, requests

REPO = "Fish-Tacos/quantum-sentinel-symbolic"
OWNER, NAME = REPO.split("/")
WORKFLOW = "symbolic_logger_daily.yml"   # <-- your logger filename
WINDOW_DAYS = int(os.getenv("WINDOW_DAYS", "30"))
TOKEN = os.getenv("GITHUB_TOKEN")

API = f"https://api.github.com/repos/{OWNER}/{NAME}/actions/workflows/{WORKFLOW}/runs?per_page=100&status=completed"
HEAD = {"Authorization": f"Bearer {TOKEN}", "X-GitHub-Api-Version": "2022-11-28"}

def fetch_runs(url):
    out, nxt = [], url
    while nxt:
        r = requests.get(nxt, headers=HEAD, timeout=30)
        r.raise_for_status()
        out.extend(r.json().get("workflow_runs", []))
        nxt = None
        link = r.headers.get("Link", "")
        if link:
            for part in [p.strip() for p in link.split(",")]:
                if 'rel="next"' in part:
                    nxt = part[part.find("<")+1:part.find(">")]
    return out

since = dt.datetime.utcnow() - dt.timedelta(days=WINDOW_DAYS)
runs = fetch_runs(API)
filtered = [x for x in runs if dt.datetime.strptime(x["created_at"], "%Y-%m-%dT%H:%M:%SZ") >= since]
total = len(filtered)
success = sum(1 for x in filtered if x.get("conclusion") == "success")
uptime = (success / total * 100.0) if total else 0.0

os.makedirs("status", exist_ok=True)
status = {
  "window_days": WINDOW_DAYS,
  "total_runs": total,
  "success_runs": success,
  "uptime_pct": round(uptime, 2),
  "updated_at": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
}
open("status/uptime.json","w").write(json.dumps(status, indent=2))

color = "red"
if uptime >= 99: color = "brightgreen"
elif uptime >= 95: color = "green"
elif uptime >= 90: color = "yellowgreen"
elif uptime >= 80: color = "yellow"

shield = {"schemaVersion":1,"label":f"logger uptime ({WINDOW_DAYS}d)","message":f"{round(uptime,1)}%","color":color}
open("status/uptime_shield.json","w").write(json.dumps(shield))
print(json.dumps(status))
