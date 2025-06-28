from data_fetcher import fetch_stock_data
from strategy import generate_signals
from backtester import backtest_strategy
from ml_test import run_ml_test
from sheet_logger import connect_to_sheet, log_trade, log_accuracy

# 🔁 Three different NIFTY 50 companies
stocks = ["HDFCBANK.NS", "ITC.NS", "LT.NS"]


# 🔌 Connect to the Google Sheet
sheet = connect_to_sheet(sheet_name, creds_path)

# ♻️ Process each stock one by one
for stock in stocks:
    try:
        print(f"\n🔍 Processing {stock}")

        # 📊 Fetch stock data
        df = fetch_stock_data(stock, period="6mo")

        # 📈 Generate buy/sell signals
        df = generate_signals(df)

        # ⏪ Backtest the strategy
        trades, pnl = backtest_strategy(df)

        # 🧾 Log top 3 trades
        for action, date, price in trades[:3]:
            print(f"{action} on {date.date()} at ₹{price.item():.2f}")
            log_trade(sheet, stock, action, date.date(), price.item(), pnl)

        print(f"💰 Net Profit for {stock}: ₹{pnl:.2f}")

        # 🤖 Run ML prediction
        model, accuracy, prediction = run_ml_test(stock, period="6mo", model_type='tree')

        if accuracy == 0 or prediction is None:
            print(f"⚠️ ML model was not trained for {stock} due to insufficient data.")
        else:
            prediction_label = "📈 Price likely to go UP tomorrow" if prediction == 1 else "📉 Price likely to go DOWN or stay"

            # ✅ Show and log prediction
            print(f"✅ ML model for {stock} trained with accuracy: {accuracy*100:.2f}%")
            print(f"🔮 ML says: {prediction_label}")

            log_accuracy(sheet, stock, accuracy)
            log_prediction(sheet, stock, prediction_label)

    except Exception as e:
        print(f"❌ Error processing {stock}: {e}")
