from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
from data_fetcher import fetch_stock_data  # Assumes this function is implemented

def prepare_ml_data(df):
    # Ensure there's enough data and 'Close' column
    if 'Close' not in df.columns or len(df) < 20:
        return pd.DataFrame(), pd.Series()

    # Feature Engineering
    df['Return'] = df['Close'].pct_change()
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA10'] = df['Close'].rolling(window=10).mean()
    df['Volatility'] = df['Return'].rolling(window=5).std()

    # Target: 1 if price goes up next day, else 0
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)

    # Drop NaNs
    df.dropna(inplace=True)

    # Features and target
    X = df[['Return', 'MA5', 'MA10', 'Volatility']]
    y = df['Target']

    return X, y

def train_and_evaluate(X, y, model_type='logistic'):
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Select model
    if model_type == 'tree':
        model = DecisionTreeClassifier(max_depth=4)
    else:
        model = LogisticRegression(max_iter=1000)

    # Train and evaluate
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return model, accuracy

def run_ml_test(stock, period="6mo", model_type='logistic'):
    print(f"\n🔍 Running ML prediction for {stock} with period={period} and model={model_type}")
    df = fetch_stock_data(stock, period=period)

    # Prepare features and labels
    X, y = prepare_ml_data(df)

    # Guard clause for empty data
    if X.empty or y.empty:
        print("⚠️ Not enough data for ML model. Skipping.")
        return None, 0, None

    # Train and evaluate model
    model, accuracy = train_and_evaluate(X, y, model_type=model_type)

    # Predict for the latest day
    latest_features = X.iloc[[-1]]
    predicted = model.predict(latest_features)[0]

    prediction_label = "📈 Price likely to go UP tomorrow" if predicted == 1 else "📉 Price likely to go DOWN or stay"

    print(f"🧠 ML Prediction Accuracy: {accuracy*100:.2f}%")
    print(f"🔮 ML says: {prediction_label}")

    return model, accuracy, predicted  # ✅ Now returns 3 values
