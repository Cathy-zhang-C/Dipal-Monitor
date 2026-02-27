import os, json, requests
from pathlib import Path
cfg = json.load(open("config.yaml","r"))
WEBHOOK = os.getenv("WEBHOOK_URL") or cfg["targets"]["webhook_url"]
summary = Path("summary.txt").read_text() if Path("summary.txt").exists() else "No summary"
if WEBHOOK:
    payload = {"text": summary}
    try:
        requests.post(WEBHOOK, json=payload, timeout=10)
        print("webhook posted")
    except Exception as e:
        print("webhook error", e)
# simple email via SMTP (optional)
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = cfg["targets"]["email"]["to"]
if EMAIL_USER and EMAIL_PASS:
    import smtplib
    from email.mime.text import MIMEText
    msg = MIMEText(summary)
    msg["Subject"] = "Daily Competitor Monitor"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO
    s = smtplib.SMTP_SSL(os.getenv("EMAIL_SMTP","smtp.gmail.com"), 465)
    s.login(EMAIL_USER, EMAIL_PASS)
    s.sendmail(EMAIL_USER, [EMAIL_TO], msg.as_string())
    s.quit()
    print("email sent")
