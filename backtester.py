# backtester.py
import pandas as pd

def backtest_strategy(df, initial_cash=100000):
    cash = initial_cash
    shares = 0.0
    trade_log = []

    for i in range(1, len(df)):
        if df['Buy_Signal'].iloc[i] and cash > 0:
            shares = cash / df['Close'].iloc[i].item()
            cash = 0
            trade_log.append(("BUY", df.index[i], df['Close'].iloc[i]))

        elif shares > 0 and pd.notna(df['RSI'].iloc[i]) and df['RSI'].iloc[i] > 70:
            cash = shares * df['Close'].iloc[i].item()
            shares = 0
            trade_log.append(("SELL", df.index[i], df['Close'].iloc[i]))

    portfolio_value = cash + (shares * df['Close'].iloc[-1].item())
    profit = portfolio_value - initial_cash
    return trade_log, profit
