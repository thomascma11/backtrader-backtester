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

        # ➕ ADD QUANT ANALYZERS
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe', timeframe=bt.TimeFrame.Days)
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
        cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')

        print(f"\n💰 Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")

        results = cerebro.run()
        strat = results[0]

        print(f"💰 Final Portfolio Value: {cerebro.broker.getvalue():.2f}")

        # Extract analyzer results
        sharpe = strat.analyzers.sharpe.get_analysis()
        drawdown = strat.analyzers.drawdown.get_analysis()
        trades = strat.analyzers.trades.get_analysis()
        returns = strat.analyzers.returns.get_analysis()

        print("\n📊 PERFORMANCE METRICS")
        print("-" * 40)

        # Sharpe ratio
        print(f"📈 Sharpe Ratio: {sharpe.get('sharperatio', 'N/A')}")

        # Drawdown
        print(f"📉 Max Drawdown: {drawdown.max.drawdown:.2f}%")
        print(f"📉 Max Drawdown Duration: {drawdown.max.len} bars")

        # Returns
        print(f"📈 Total Return: {returns.get('rtot', 0):.4f}")
        print(f"📈 Annualized Return: {returns.get('rnorm', 0):.4f}")

        # Trades
        total_trades = trades.total.total if trades.total else 0
        won = trades.won.total if trades.won else 0
        lost = trades.lost.total if trades.lost else 0

        print(f"🔁 Total Trades: {total_trades}")
        print(f"✅ Winning Trades: {won}")
        print(f"❌ Losing Trades: {lost}")

        if total_trades > 0:
            win_rate = won / total_trades * 100
            print(f"🏆 Win Rate: {win_rate:.2f}%")

        print("-" * 40)

        # Plot equity curve
        cerebro.plot(style="candlestick")


if __name__ == "__main__":
    BacktestRunner().run()

