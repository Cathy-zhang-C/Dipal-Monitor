import json
from pathlib import Path
p = Path(__file__).resolve().parent.parent / "report.json"
if not p.exists():
    print("no report.json"); exit(0)
r = json.load(open(p, 'r', encoding='utf-8'))
lines = []
lines.append(f"Daily Competitor Monitor — total items: {r['summary']['rows']}")
lines.append("Average sentiment by platform:")
for k,v in r['summary']['sentiment_avg'].items():
    lines.append(f"- {k}: {v:.3f}")
if r['anomalies']:
    lines.append("Anomalies detected:")
    for a in r['anomalies']:
        lines.append(f"- {a['platform']} | {a['type']} | id={a['id']} | engagement={a['engagement']} | z={a['z']:.2f}")
else:
    lines.append("No anomalies found.")
out = "\n".join(lines)
open(Path(__file__).resolve().parent.parent / "summary.txt","w", encoding='utf-8').write(out)
print("wrote summary.txt")
