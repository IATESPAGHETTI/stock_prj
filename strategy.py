# strategy.py
import pandas as pd

def calculate_indicators(df):
    df['20DMA'] = df['Close'].rolling(window=20).mean()
    df['50DMA'] = df['Close'].rolling(window=50).mean()
    
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    return df

def generate_signals(df):
    df = calculate_indicators(df)
    df['Buy_Signal'] = (df['RSI'] < 30) & (df['20DMA'] > df['50DMA'])
    return df

def add_macd(df):
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26
    return df

def prepare_ml_data(df):
    df = calculate_indicators(df)
    df = add_macd(df)

    # ✅ Ensure Volume exists
    if 'Volume' not in df.columns:
        df['Volume'] = 1
    else:
        # ✅ Only proceed if .all() returns True/False (not Series)
        if df['Volume'].isnull().all().item():  # <--- THIS FIXES IT
            df['Volume'] = 1

    # 🎯 Create target variable
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)

    # ✅ Keep only relevant features and drop NaNs
    df = df[['RSI', 'MACD', 'Volume', 'Target']].dropna()

    if df.empty:
        return pd.DataFrame(), pd.Series(dtype=int)

    X = df[['RSI', 'MACD', 'Volume']]
    y = df['Target']
    return X, y
