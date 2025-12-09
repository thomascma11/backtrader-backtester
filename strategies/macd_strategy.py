import backtrader as bt

class MACDStrategy(bt.Strategy):
    def __init__(self):
        self.macd = bt.indicators.MACD(self.data.close)
        self.signal = bt.indicators.MACD(self.data.close).signal

    def next(self):
        if not self.position and self.macd > self.signal:
            self.buy()

        elif self.position and self.macd < self.signal:
            self.sell()
