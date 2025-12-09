import backtrader as bt

class RSIStrategy(bt.Strategy):
    params = dict(period=14, rsi_low=30, rsi_high=70)

    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=self.p.period)

    def next(self):
        if not self.position:
            if self.rsi < self.p.rsi_low:
                self.buy()

        else:
            if self.rsi > self.p.rsi_high:
                self.sell()
