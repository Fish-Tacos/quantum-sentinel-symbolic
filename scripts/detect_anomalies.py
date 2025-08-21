#!/usr/bin/env python3
import json, pathlib
from collections import Counter, OrderedDict

LOG = pathlib.Path("data/logs/symbolic_log.json")
OUT = pathlib.Path("docs/anomalies.json")     # <- served by GitHub Pages
OUT.parent.mkdir(parents=True, exist_ok=True)

if not LOG.exists():
    OUT.write_text(json.dumps({"anomalies": [], "window_days": 14}, indent=2))
    raise SystemExit("no log yet")

entries = json.loads(LOG.read_text())
counts = Counter((e.get("ts","")[:10] for e in entries if e.get("ts")))
series = OrderedDict((d, counts[d]) for d in sorted(counts))

N = 14
anoms, keys, vals = [], list(series.keys()), list(series.values())
for i in range(len(vals)):
    if i < N: 
        continue
    window = vals[i-N:i]
    mu = sum(window)/N
    sd = (sum((x-mu)**2 for x in window)/N) ** 0.5
    z  = 0.0 if sd == 0 else (vals[i]-mu)/sd
    if sd > 0 and z >= 2.0:
        anoms.append({"date": keys[i], "count": vals[i], "z": round(z,2),
                      "baseline_mean": round(mu,2), "baseline_sd": round(sd,2)})

OUT.write_text(json.dumps({"anomalies": anoms, "window_days": N, "total_days": len(vals)}, indent=2))
print(f"wrote {OUT} with {len(anoms)} anomalies")
