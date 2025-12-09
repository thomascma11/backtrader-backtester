import numpy as np
import pandas as pd

# Build daily portfolio series from equity curve
values = [float(p["value"]) for p in equity_curve]
dates = pd.to_datetime([p["date"] for p in equity_curve])

series = pd.Series(values, index=dates)

# Daily returns
daily_returns = series.pct_change().dropna()

# Annualized return
annual_return = (1 + daily_returns.mean()) ** 252 - 1

# Annualized volatility
annual_volatility = daily_returns.std() * np.sqrt(252)

# Sharpe Ratio (assume 0% risk-free rate)
sharpe_ratio = annual_return / annual_volatility if annual_volatility != 0 else 0

# Max Drawdown
rolling_max = series.cummax()
drawdowns = (series - rolling_max) / rolling_max
max_drawdown = drawdowns.min()

# Max Drawdown Duration
drawdown_duration = (drawdowns == 0).astype(int)
max_drawdown_duration = (drawdowns < 0).astype(int).groupby((drawdowns == 0).cumsum()).cumcount().max()

# Save into metrics JSON
metrics["annual_return"] = float(annual_return)
metrics["annual_volatility"] = float(annual_volatility)
metrics["sharpe_ratio"] = float(sharpe_ratio)
metrics["max_drawdown"] = float(max_drawdown)
metrics["max_drawdown_duration"] = int(max_drawdown_duration)

import backtrader as bt
import yfinance as yf
import json
import os

import matplotlib.pyplot as plt

# Equity curve chart
plt.plot(series.index, series.values)
plt.title("Equity Curve")
plt.savefig("results/equity_curve.png")
plt.close()

# Buy/sell signal chart placeholder
plt.plot(series.index, series.values)
plt.title("Buy/Sell Signals")
plt.savefig("results/signals.png")
plt.close()

# Import strategies
from strategies.sma_cross import SmaCross
from strategies.rsi_strategy import RSIStrategy
from strategies.macd_strategy import MACDStrategy
from strategies.bollinger_strategy import BollingerStrategy
from strategies.ema_cross import EMACross

# Strategy selection table
STRATEGIES = {
    "sma": SmaCross,
    "rsi": RSIStrategy,
    "macd": MACDStrategy,
    "bollinger": BollingerStrategy,
    "ema": EMACross
}


class BacktestRunner:

    def __init__(self, config_path="config.json"):
        with open(config_path, "r") as f:
            config = json.load(f)

        self.ticker = config["ticker"]
        self.strategy = config["strategy"]
        self.start_cash = config["start_cash"]
        self.commission = config["commission"]
        self.data_start = config["data_start"]
        self.data_end = config["data_end"]

    def load_data(self):
        df = yf.download(self.ticker, start=self.data_start, end=self.data_end)
        df.to_csv("data/price_data.csv")
        return bt.feeds.PandasData(dataname=df)

    def run(self):
        cerebro = bt.Cerebro()

        # Set cash + commission
        cerebro.broker.setcash(self.start_cash)
        cerebro.broker.setcommission(commission=self.commission)

        # Load data
        data = self.load_data()
        cerebro.adddata(data)

        # ADD SELECTED STRATEGY
        cerebro.addstrategy(STRATEGIES[self.strategy])

        # Add analyzers
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trades")
        cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")

        print(f"\n🔥 Running {self.strategy.upper()} strategy on {self.ticker}")
        print(f"💰 Starting Portfolio Value: {cerebro.broker.getvalue():,.2f}")

        results = cerebro.run()
        strat = results[0]

        print(f"💰 Final Portfolio Value: {cerebro.broker.getvalue():,.2f}")

        # Equity curve tracking
        equity_curve = []
        for i in range(len(cerebro.datas[0])):
            dt = cerebro.datas[0].datetime.datetime(i)
            value = cerebro.broker.getvalue()
            equity_curve.append({"date": str(dt), "value": value})

        metrics["equity_curve"] = equity_curve

# Buy/Sell signal indices
metrics["buy_signals"] = [i for i, v in enumerate(strat.buy_signals)]
metrics["sell_signals"] = [i for i, v in enumerate(strat.sell_signals)]

        # Extract metrics
        sharpe = strat.analyzers.sharpe.get_analysis()
        drawdown = strat.analyzers.drawdown.get_analysis()
        trades = strat.analyzers.trades.get_analysis()
        returns = strat.analyzers.returns.get_analysis()

        total_trades = trades.total.total if trades.total.total else 0
        win = trades.won.total if trades.won.total else 0
        lose = trades.lost.total if trades.lost.total else 0
        win_rate = (win / total_trades * 100) if total_trades else 0

        metrics = {
            "ticker": self.ticker,
            "strategy": self.strategy,
            "starting_value": self.start_cash,
            "ending_value": cerebro.broker.getvalue(),
            "sharpe_ratio": sharpe.get("sharperatio", None),
            "max_drawdown_pct": drawdown.max.drawdown,
            "max_drawdown_len": drawdown.max.len,
            "returns_total": returns.get("rtot", 0),
            "returns_annualized": returns.get("rnorm", 0),
            "total_trades": total_trades,
            "winning_trades": win,
            "losing_trades": lose,
            "win_rate": win_rate
        }

        # Save to results folder
        if not os.path.exists("results"):
            os.makedirs("results")

        with open("results/metrics.json", "w") as f:
            json.dump(metrics, f, indent=4)

        print("📁 Results saved to results/metrics.json")


if __name__ == "__main__":
    bt = BacktestRunner()
    bt.run()
