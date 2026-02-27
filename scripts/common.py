import os, json, yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def load_config():
    return yaml.safe_load(open(ROOT.parent / "config.yaml"))

def load_google_creds():
    # In GitHub Actions, GOOGLE_SA_KEY stored as secret with JSON content
    key = os.getenv("GOOGLE_SA_KEY")
    if not key:
        # local dev: expect file GOOGLE_SA.json
        if Path("GOOGLE_SA.json").exists():
            return "GOOGLE_SA.json"
        raise RuntimeError("GOOGLE_SA_KEY not set")
    # write to temp file
    p = ROOT / "sa_key.json"
    p.write_text(key)
    return str(p)
