import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt
import os
import yfinance as yf

from strategies.sma_cross import SmaCross


class BacktestRunner:
    def __init__(self, ticker="AAPL", csv_path="data/AAPL.csv",
                 cash=10000, commission=0.001):
        self.ticker = ticker
        self.csv_path = csv_path
        self.cash = cash
        self.commission = commission

    def load_data(self):
        # Check if CSV exists
        if os.path.exists(self.csv_path):
            print(f"📁 Loading local dataset: {self.csv_path}")
            df = pd.read_csv(self.csv_path, index_col="Date", parse_dates=True)
        else:
            print(f"⬇️ Downloading {self.ticker} data using yfinance...")
            df = yf.download(self.ticker, start="2023-01-01", end="2024-01-01")
            df.to_csv(self.csv_path)
            print(f"📄 Saved downloaded data to {self.csv_path}")

        df = df.sort_index()

        # Convert column names for Backtrader
        df = df.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        })

        return bt.feeds.PandasData(dataname=df)

    def run(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(self.cash)
        cerebro.broker.setcommission(commission=self.commission)

        data_feed = self.load_data()
        cerebro.adddata(data_feed)

        cerebro.addstrategy(SmaCross)

        print(f"\n💰 Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")
        cerebro.run()
        print(f"💰 Final Portfolio Value: {cerebro.broker.getvalue():.2f}")

        # Create performance chart
        cerebro.plot(style="candlestick")


if __name__ == "__main__":
    BacktestRunner().run()
