import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt
from strategies.sma_cross import SmaCross


class BacktestRunner:
    def __init__(self, csv_path="data/AAPL.csv", cash=10000, commission=0.001):
        self.csv_path = csv_path
        self.cash = cash
        self.commission = commission

    def load_data(self):
        df = pd.read_csv(self.csv_path, index_col="Date", parse_dates=True)
        df = df.sort_index()
        return bt.feeds.PandasData(dataname=df)

    def run(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(self.cash)
        cerebro.broker.setcommission(commission=self.commission)

        data = self.load_data()
        cerebro.adddata(data)

        cerebro.addstrategy(SmaCross)

        print(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")
        results = cerebro.run()
        print(f"Final Portfolio Value: {cerebro.broker.getvalue():.2f}")

        # Plot equity + strategy
        cerebro.plot(style="candlestick")


if __name__ == "__main__":
    runner = BacktestRunner()
    runner.run()
