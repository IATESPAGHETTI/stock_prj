# 📊 Algo-Trading Backtest & ML Logger

This project fetches stock data, applies a basic trading strategy, backtests the performance, optionally runs a machine learning model, and logs the results to a Google Sheet.

---

## 📁 Project Structure

| File / Module         | Description                                               |
|-----------------------|-----------------------------------------------------------|
| `main.py`             | Runs the end-to-end pipeline for backtesting + ML         |
| `data_fetcher.py`     | Downloads stock data using Yahoo Finance (`yfinance`)     |
| `strategy.py`         | Generates trading signals (e.g., RSI + DMA)               |
| `backtester.py`       | Simulates trades and calculates profit                    |
| `ml_model.py`         | Trains and evaluates an ML model (logistic/tree)          |
| `ml_test.py`          | Wrapper for quick ML testing                              |
| `sheet_logger.py`     | Logs trades and model accuracy to Google Sheets           |

---

## ✅ Requirements

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Recommended packages include:
- `yfinance`
- `pandas`
- `numpy`
- `scikit-learn`
- `gspread`
- `oauth2client`

---

## 🔑 Google Sheets Setup (Manual Step)

To log trades and ML accuracy to Google Sheets, you **must set up your own credentials**:

### 1. Enable Google Sheets API

1. Visit: https://console.cloud.google.com/
2. Create or select a project
3. Enable the following APIs:
   - Google Sheets API
   - Google Drive API

### 2. Create a Service Account

1. Go to: **APIs & Services > Credentials**
2. Click **Create Credentials > Service Account**
3. Once created, go to the **Keys** section
4. Click **Add Key > JSON** → this downloads a `.json` file

### 3. Add the Credentials to the Project

- Rename the JSON file to:
  ```
  add_your_own_google_creds.json
  ```
- Place it in the root of your project folder.

### 4. Share the Sheet with the Service Account

- Create a Google Sheet named:
  ```
  trade_log
  ```
- Share the sheet with the **client_email** from the JSON file.
  - Example: `my-bot@my-project.iam.gserviceaccount.com`
- Give it **Editor** access.

---

## 🚀 How to Run

```bash
python main.py
```

This will:
- Fetch historical stock data
- Generate signals & backtest them
- Optionally run a machine learning model
- Log top trades and ML accuracy to your connected Google Sheet

---

## ✏️ Notes

- If you don’t need Google Sheets logging, you can comment out or remove the `sheet_logger.py` imports and function calls.
- Logging will silently fail if the credentials are missing or the sheet isn’t shared properly — watch for print/debug messages!
