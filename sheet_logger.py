import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_sheet(sheet_name, creds_path="google_creds.json"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    return sheet

def log_trade(sheet, stock, action, date, price, pnl):
    row = [stock, action, str(date), price, pnl]
    sheet.append_row(row)

def log_accuracy(sheet, stock, accuracy):
    row = [stock, "ML Accuracy", "", "", round(accuracy, 4)]
    sheet.append_row(row)

def log_prediction(sheet, stock, prediction_label):
    row = [stock, "ML Prediction", "", "", prediction_label]
    sheet.append_row(row)
