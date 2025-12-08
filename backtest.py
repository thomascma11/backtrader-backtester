import backtrader as bt
import pandas as pd

class SMACross(bt.Strategy):
    params = (('fast', 10), ('slow', 30),)

    def __init__(self):
        self.fast_ma = bt.ind.SMA(period=self.p.fast)
        self.slow_ma = bt.ind.SMA(period=self.p.slow)
        self.crossover = bt.ind.CrossOver(self.fast_ma, self.slow_ma)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        else:
            if self.crossover < 0:
                self.sell()

def run_backtest(csv_path):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SMACross)

    df = pd.read_csv(csv_path, index_col='Date', parse_dates=True)
    data = bt.feeds.PandasData(dataname=df)

    cerebro.adddata(data)
    cerebro.broker.set_cash(10000)
    cerebro.broker.setcommission(commission=0.001)

    print("Starting Portfolio Value:", cerebro.broker.getvalue())
    cerebro.run()
    print("Final Portfolio Value:", cerebro.broker.getvalue())
    cerebro.plot()

if __name__ == "__main__":
    run_backtest("data/AAPL.csv")
