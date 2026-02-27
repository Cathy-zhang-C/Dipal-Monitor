# basic instaloader usage to get profile metadata and recent posts metadata
import instaloader, json
from common import load_config, ROOT

cfg = load_config()
profiles = cfg["platforms"]["instagram"]["profiles"]
L = instaloader.Instaloader(download_pictures=False, download_videos=False, save_metadata=False, compress_json=False)
OUT = ROOT / "../data"
OUT.mkdir(parents=True, exist_ok=True)

for p in profiles:
    try:
        profile = instaloader.Profile.from_username(L.context, p)
        posts = []
        for i, post in enumerate(profile.get_posts()):
            if i>=20: break
            posts.append({
                "id": post.shortcode,
                "date": post.date_iso,
                "likes": post.likes,
                "comments": post.comments,
                "caption": post.caption
            })
        out = {"platform":"instagram","profile":p,"followers":profile.followers,"posts":posts}
        (OUT / f"instagram_{p}.json").write_text(json.dumps(out, ensure_ascii=False))
        print("saved instagram", p)
    except Exception as e:
        print("insta error", p, e)
