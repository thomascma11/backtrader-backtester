import backtrader as bt


class SmaCross(bt.Strategy):
    params = dict(
        fast=10,   # fast SMA
        slow=30    # slow SMA
    )

    def __init__(self):
        sma_fast = bt.ind.SMA(period=self.p.fast)
        sma_slow = bt.ind.SMA(period=self.p.slow)
        self.crossover = bt.ind.CrossOver(sma_fast, sma_slow)

    def next(self):
        if not self.position:  
            if self.crossover > 0:  
                self.buy()
        else:
            if self.crossover < 0:  
                self.sell()
