# uses snscrape for TikTok user
import json, subprocess
from common import load_config, ROOT

cfg = load_config()
profiles = cfg["platforms"]["tiktok"]["profiles"]
OUT = ROOT / "../data"
OUT.mkdir(parents=True, exist_ok=True)

for p in profiles:
    cmd = ["snscrape", "tiktok-user", p, "--jsonl"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = res.stdout.strip().splitlines()
        posts = [json.loads(l) for l in lines[-50:]]
    except Exception as e:
        print("tiktok snscrape error", e); posts=[]
    out = {"platform":"tiktok","profile":p,"posts":posts}
    (OUT / f"tiktok_{p}.json").write_text(json.dumps(out, ensure_ascii=False))
    print("saved tiktok", p)
