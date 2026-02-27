# uses snscrape to fetch latest user posts and follower count
import json, subprocess, sys
from common import load_config, ROOT

cfg = load_config()
profiles = cfg["platforms"]["x"]["profiles"]

OUT = ROOT / "../data"
OUT.mkdir(parents=True, exist_ok=True)

for p in profiles:
    # snscrape user tweets
    cmd = ["snscrape", "twitter-user", p, "--jsonl"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = res.stdout.strip().splitlines()
        posts = [json.loads(l) for l in lines[-50:]]  # keep recent 50
    except Exception as e:
        print("snscrape error", e)
        posts = []
    # get followers from last tweet user field if available
    followers = None
    if posts and "user" in posts[0]:
        followers = posts[0]["user"].get("followersCount")
    out = {"platform":"x","profile":p,"followers":followers,"posts":posts}
    (OUT / f"x_{p}.json").write_text(json.dumps(out, ensure_ascii=False))
    print("saved", p)
