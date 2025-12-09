import backtrader as bt

class EMACross(bt.Strategy):
    params = dict(fast=12, slow=26)

    def __init__(self):
        ema_fast = bt.ind.EMA(period=self.p.fast)
        ema_slow = bt.ind.EMA(period=self.p.slow)
        self.crossover = bt.ind.CrossOver(ema_fast, ema_slow)

    def next(self):
        if not self.position and self.crossover > 0:
            self.buy()
        elif self.position and self.crossover < 0:
            self.sell()
