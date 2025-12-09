import backtrader as bt
import yfinance as yf
import pandas as pd
import numpy as np
import json
import os

# ================================
# Import strategies
# ================================
from strategies.sma_cross import SmaCross
from strategies.rsi_strategy import RSIStrategy
from strategies.macd_strategy import MACDStrategy
from strategies.bollinger_strategy import BollingerStrategy
from strategies.ema_cross import EMACross

# Strategy registry
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
        self.strategy_name = config["strategy"]
        self.start_cash = config["start_cash"]
        self.commission = config["commission"]
        self.start_date = config["data_start"]
        self.end_date = config["data_end"]

    # -----------------------------------------
    # Load price data (Yahoo Finance)
    # -----------------------------------------
    def load_data(self):
        df = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        df.to_csv("data/price_data.csv")
        return bt.feeds.PandasData(dataname=df)

    # -----------------------------------------
    # Run the backtest
    # -----------------------------------------
    def run(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(self.start_cash)
        cerebro.broker.setcommission(commission=self.commission)

        data = self.load_data()
        cerebro.adddata(data)

        cerebro.addstrategy(STRATEGIES[self.strategy_name])

        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")
        cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trades")

        print(f"\n🔥 Running {self.strategy_name.upper()} on {self.ticker}")
        print(f"Starting Portfolio Value: {cerebro.broker.getvalue():,.2f}")

        results = cerebro.run()
        strat = results[0]

        final_value = cerebro.broker.getvalue()
        print(f"Final Portfolio Value: {final_value:,.2f}")

        # -----------------------------------------
        # Extract analyzer results
        # -----------------------------------------
        sharpe = strat.analyzers.sharpe.get_analysis()
        drawdown = strat.analyzers.drawdown.get_analysis()
        returns = strat.analyzers.returns.get_analysis()
        trades = strat.analyzers.trades.get_analysis()

        # -----------------------------------------
        # Build equity curve
        # -----------------------------------------
        equity_curve = []
        for i in range(len(cerebro.datas[0])):
            dt = cerebro.datas[0].datetime.datetime(i)
            val = cerebro.broker.getvalue()
            equity_curve.append({"date": str(dt), "value": float(val)})

        # -----------------------------------------
        # Portfolio statistics
        # -----------------------------------------
        values = np.array([p["value"] for p in equity_curve])
        dates = pd.to_datetime([p["date"] for p in equity_curve])
        series = pd.Series(values, index=dates)

        # daily returns
        daily = series.pct_change().dropna()

        # annual metrics
        annual_return = (1 + daily.mean()) ** 252 - 1
        annual_vol = daily.std() * np.sqrt(252)
        sharpe_manual = annual_return / annual_vol if annual_vol != 0 else 0

        # max drawdown
        roll_max = series.cummax()
        dd = (series - roll_max) / roll_max
        max_dd = dd.min()
        max_dd_duration = int(
            (dd < 0).astype(int).groupby((dd == 0).cumsum()).cumcount().max()
        )

        # -----------------------------------------
        # Benchmark SPY
        # -----------------------------------------
        spy = yf.download("SPY", start=self.start_date, end=self.end_date)["Adj Close"]
        spy_ret = spy.pct_change().dropna()

        spy_ann_return = (1 + spy_ret.mean()) ** 252 - 1
        spy_vol = spy_ret.std() * np.sqrt(252)
        spy_sharpe = spy_ann_return / spy_vol if spy_vol != 0 else 0

        # -----------------------------------------
        # Build metrics JSON
        # -----------------------------------------
        metrics = {
            "ticker": self.ticker,
            "strategy": self.strategy_name,
            "starting_value": self.start_cash,
            "ending_value": final_value,

            "annual_return": float(annual_return),
            "annual_volatility": float(annual_vol),
            "sharpe_ratio": float(sharpe_manual),

            "max_drawdown": float(max_dd),
            "max_drawdown_duration": max_dd_duration,

            "benchmark_annual_return": float(spy_ann_return),
            "benchmark_volatility": float(spy_vol),
            "benchmark_sharpe": float(spy_sharpe),

            "equity_curve": equity_curve
        }

        if not os.path.exists("results"):
            os.makedirs("results")

        with open("results/metrics.json", "w") as f:
            json.dump(metrics, f, indent=4)

        print("📁 Metrics saved to results/metrics.json")

        return metrics


if __name__ == "__main__":
    BacktestRunner().run()
