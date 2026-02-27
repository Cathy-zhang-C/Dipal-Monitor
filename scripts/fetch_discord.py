# Minimal approach: if you cannot read history, skip. If you have BOT token, use REST API to fetch messages.
import os, requests, json
from common import load_config, ROOT

cfg = load_config()
channel_id = cfg["platforms"]["discord"].get("channel_id")
token = os.getenv("DISCORD_BOT_TOKEN")
OUT = ROOT / "../data"
OUT.mkdir(parents=True, exist_ok=True)

if not token:
    print("No DISCORD_BOT_TOKEN set, skipping discord fetch")
else:
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages?limit=50"
    headers = {"Authorization": f"Bot {token}"}
    r = requests.get(url, headers=headers)
    if r.status_code==200:
        (OUT / f"discord_{channel_id}.json").write_text(r.text)
        print("saved discord messages")
    else:
        print("discord fetch failed", r.status_code, r.text)
