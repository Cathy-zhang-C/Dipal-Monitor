import json, glob, os
import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from common import load_config, ROOT

cfg = load_config()
DATA = ROOT / "../data"
analyzer = SentimentIntensityAnalyzer()

# read saved json files
files = glob.glob(str(DATA / "*.json"))
records = []
for f in files:
    j = json.load(open(f, 'r', encoding='utf-8'))
    platform = j.get("platform")
    if platform=="youtube":
        for v in j.get("videos",[]):
            stats = v.get("statistics",{})
            rec = {"platform":"youtube","id":v["id"],"title":v["snippet"]["title"],"views":int(stats.get("viewCount",0))}
            records.append(rec)
    elif platform in ("x","instagram","tiktok"):
        profile = j.get("profile")
        followers = j.get("followers")
        for p in j.get("posts",[]):
            text = p.get("content") or p.get("caption") or p.get("rawContent") or p.get("text", "")
            likes = p.get("likeCount") or p.get("likes") or p.get("likesCount") or p.get("likes",0)
            comments = p.get("replyCount") or p.get("comments") or p.get("commentsCount") or 0
            engagement = (int(likes or 0) + int(comments or 0))
            sentiment = analyzer.polarity_scores(text)["compound"]
            records.append({"platform":platform,"profile":profile,"id":p.get("id") or p.get("shortcode"),"engagement":engagement,"sentiment":sentiment,"followers":followers})
# convert to df
df = pd.DataFrame(records)
if df.empty:
    print("no records")
    exit(0)

# simple anomaly detection per platform: engagement z-score
out_anoms = []
for plat in df['platform'].unique():
    d = df[df['platform']==plat]
    if 'engagement' in d.columns and not d['engagement'].isna().all():
        mean = d['engagement'].mean()
        std = d['engagement'].std(ddof=0) if d['engagement'].std(ddof=0)!=0 else 1
        d['z'] = (d['engagement'] - mean) / std
        for _, row in d.iterrows():
            if row['z'] >= cfg['anomaly']['zscore_threshold']:
                out_anoms.append({"platform":plat,"id":row['id'],"type":"high_engagement","engagement":int(row['engagement']),"z":float(row['z'])})
# sentiment drop simple check (requires historical storage to be meaningful)
# For starter, report average sentiment today
sent_summary = df.groupby('platform')['sentiment'].mean().to_dict()

report = {"summary": {"rows": len(df), "sentiment_avg": sent_summary}, "anomalies": out_anoms}
open(ROOT.parent / "report.json","w", encoding='utf-8').write(json.dumps(report, ensure_ascii=False, indent=2))
print("wrote report.json")
