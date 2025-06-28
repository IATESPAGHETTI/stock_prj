# ml_test.py
from data_fetcher import fetch_stock_data
from strategy import prepare_ml_data
from ml_model import train_and_evaluate

def run_ml_test(stock, period="6mo", model_type='logistic'):
    print(f"\n🔍 Running ML prediction for {stock} with period={period} and model={model_type}")
    df = fetch_stock_data(stock, period=period)

    X, y = prepare_ml_data(df)

    if X.empty or y.empty:
        print("⚠️ Not enough data for ML model. Skipping.")
        return None, 0

    model, accuracy = train_and_evaluate(X, y, model_type=model_type)
    print(f"🧠 ML Prediction Accuracy: {accuracy*100:.2f}%")
    return model, accuracy
