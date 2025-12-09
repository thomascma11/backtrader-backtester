import yfinance as yf
import pandas as pd

def download_data(symbol="AAPL", start="2015-01-01", end="2025-01-01"):
    df = yf.download(symbol, start=start, end=end)
    df.to_csv(f"data/{symbol}.csv")
    print(f"Saved data/{symbol}.csv")

if __name__ == "__main__":
    download_data()
