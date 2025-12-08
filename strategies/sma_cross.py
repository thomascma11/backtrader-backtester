import backtrader as bt

class SMACross(bt.Strategy):
    params = (('fast', 10), ('slow', 30))

    def __init__(self):
        self.fast_ma = bt.ind.SMA(period=self.p.fast)
        self.slow_ma = bt.ind.SMA(period=self.p.slow)
        self.crossover = bt.ind.CrossOver(self.fast_ma, self.slow_ma)

    def next(self):
        # Buy when fast MA crosses above slow MA
        if not self.position:
            if self.crossover > 0:
                self.buy()
        # Sell when fast MA crosses below slow MA
        else:
            if self.crossover < 0:
                self.sell()
