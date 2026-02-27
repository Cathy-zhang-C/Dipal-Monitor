# Competitor Daily Monitor - Starter

Daily monitor for: Dipal (Instagram, YouTube, TikTok, X, Discord)
Runs daily via GitHub Actions, stores data to Google Sheets, performs anomaly detection,
sends report via webhook/email.

Setup summary:
1. Create GitHub repo and add these files.
2. Create Google Cloud project -> enable Sheets API + YouTube Data API.
   - Create Service Account, download JSON key. Add key JSON as secret `GOOGLE_SA_KEY`.
   - Create YouTube API key, add as secret `YOUTUBE_API_KEY`.
3. Add other secrets in repo Settings > Secrets:
   - WEBHOOK_URL (for notifications)
   - EMAIL_SMTP, EMAIL_USER, EMAIL_PASS (if using email)
   - DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID (optional)
4. Edit `config.yaml` with target accounts and Google Sheet ID.
5. Push to GitHub and enable Actions. Workflow runs daily.

Run locally:
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- fill config.yaml and GOOGLE_SA_KEY as file GOOGLE_SA.json for local tests
- python scripts/fetch_x.py
- python scripts/fetch_youtube.py
- python scripts/analyzer.py
