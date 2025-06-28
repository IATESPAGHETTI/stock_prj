from data_fetcher import fetch_stock_data
from strategy import generate_signals
from backtester import backtest_strategy
from ml_test import run_ml_test
from sheet_logger import connect_to_sheet, log_trade, log_accuracy

# 🔁 Three different NIFTY 50 companies
stocks = ["HDFCBANK.NS", "ITC.NS", "LT.NS"]

# Google Sheet setup
sheet_name = "trade_log"
creds_path = "google_creds.json"

# Connect to the Google Sheet
sheet = connect_to_sheet(sheet_name, creds_path)

# Loop through each stock
for stock in stocks:
    print(f"\n🔍 Processing {stock}")

    # Fetch historical stock data
    df = fetch_stock_data(stock, period="6mo")

    # Generate buy/sell signals using strategy
    df = generate_signals(df)

    # Backtest strategy to get trades and PnL
    trades, pnl = backtest_strategy(df)

    # Log top 3 trades to Google Sheet
    for action, date, price in trades[:3]:
        print(f"{action} on {date.date()} at ₹{price.item():.2f}")
        log_trade(sheet, stock, action, date.date(), price.item(), pnl)

    print(f"💰 Net Profit for {stock}: ₹{pnl:.2f}")

    # Run ML test to check predictive performance
    model, accuracy = run_ml_test(stock, period="6mo", model_type='tree')

    if accuracy == 0:
        print(f"⚠️ ML model was not trained for {stock} due to insufficient data.")
    else:
        print(f"✅ ML model for {stock} trained with accuracy: {accuracy*100:.2f}%")
        log_accuracy(sheet, stock, accuracy)
