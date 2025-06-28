import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_sheet(sheet_name, creds_path="google_creds.json"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1  # Use first worksheet
    return sheet

def log_trade(sheet, stock, action, date, price, pnl):
    sheet.append_row([stock, action, str(date), round(price, 2), round(pnl, 2)])

def log_accuracy(sheet, stock, accuracy):
    sheet.append_row([stock, "ML Accuracy", "", "", round(accuracy * 100, 2)])
