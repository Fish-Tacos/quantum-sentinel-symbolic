#!/usr/bin/env python3
import argparse, json, pathlib, time

LOG = pathlib.Path("data/logs/symbolic_log.json")
LOG.parent.mkdir(parents=True, exist_ok=True)
data = json.loads(LOG.read_text()) if LOG.exists() else []

ap = argparse.ArgumentParser()
ap.add_argument("--symbol", required=True)
ap.add_argument("--resonance", type=lambda s: s.lower() in ["1","true","yes","y"], default=False)
ap.add_argument("--hr", type=int)
ap.add_argument("--hrv", type=int)
ap.add_argument("--notes", default="")
ap.add_argument("--source", default="cli")
args = ap.parse_args()

now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
entry = {
  "ts": now, "schema_version": "1.2", "symbol": args.symbol,
  "resonance": bool(args.resonance), "hr": args.hr, "hrv": args.hrv,
  "notes": args.notes, "source": args.source, "anomaly": None
}
data.append(entry)
LOG.write_text(json.dumps(data, indent=2))
print(f"Appended: {entry}")
