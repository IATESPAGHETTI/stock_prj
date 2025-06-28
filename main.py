from data_fetcher import fetch_stock_data
from strategy import generate_signals
from backtester import backtest_strategy
from ml_test import run_ml_test
from sheet_logger import connect_to_sheet, log_trade, log_accuracy

stock = "TCS.NS"
sheet_name = "add sheet name here after giving editorial access"
creds_path = "google_creds.json"

# Connect to the sheet
sheet = connect_to_sheet(sheet_name, creds_path)

print(f"\n🔍 Processing {stock}")
df = fetch_stock_data(stock, period="2y")
df = generate_signals(df)
trades, pnl = backtest_strategy(df)

# Log top 3 trades
for action, date, price in trades[:3]:
    print(f"{action} on {date.date()} at ₹{price.item():.2f}")
    log_trade(sheet, stock, action, date.date(), price.item(), pnl)

print(f"💰 Net Profit: ₹{pnl:.2f}")

# ML test
model, accuracy = run_ml_test(stock, period="6mo", model_type='tree')

if accuracy == 0:
    print("⚠️ ML model was not trained due to insufficient data.")
else:
    print(f"✅ ML model trained with accuracy: {accuracy*100:.2f}%")
    log_accuracy(sheet, stock, accuracy)
