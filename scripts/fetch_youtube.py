# fetch recent videos from channel username using YouTube Data API
import os, json
from googleapiclient.discovery import build
from common import load_config, load_google_creds, ROOT

cfg = load_config()
api_key = os.getenv("YOUTUBE_API_KEY")
if not api_key:
    raise RuntimeError("YOUTUBE_API_KEY missing")

youtube = build("youtube", "v3", developerKey=api_key)
OUT = ROOT / "../data"
OUT.mkdir(parents=True, exist_ok=True)

for ch in cfg["platforms"]["youtube"]["channels"]:
    # get channel id by forUsername (may fail if handle different) -> use search
    search = youtube.search().list(q=ch, part="snippet", type="channel", maxResults=1).execute()
    items = search.get("items", [])
    if not items:
        print("channel not found:", ch); continue
    channelId = items[0]["snippet"]["channelId"]
    # list recent videos
    res = youtube.search().list(channelId=channelId, part="snippet", order="date", maxResults=10, type="video").execute()
    videos = []
    for it in res.get("items", []):
        vid = it["id"]["videoId"]
        stats = youtube.videos().list(part="statistics,snippet", id=vid).execute()
        if stats.get("items"):
            videos.append(stats["items"][0])
    out = {"platform":"youtube","channel":ch,"channelId":channelId,"videos":videos}
    (OUT / f"youtube_{ch}.json").write_text(json.dumps(out, ensure_ascii=False))
    print("saved youtube", ch)
