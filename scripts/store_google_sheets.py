import os, gspread, json
from oauth2client.service_account import ServiceAccountCredentials
from common import load_config, load_google_creds, ROOT

cfg = load_config()
sa_path = load_google_creds()  # returns path to JSON key
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(sa_path, scope)
gc = gspread.authorize(creds)

sheet = gc.open_by_key(cfg["google_sheet_id"])
# expects sheets named per platform, create if missing
def append_rows(sheet_name, rows):
    try:
        w = sheet.worksheet(sheet_name)
    except Exception:
        w = sheet.add_worksheet(sheet_name, rows=1000, cols=10)
    w.append_rows(rows, value_input_option='RAW')
