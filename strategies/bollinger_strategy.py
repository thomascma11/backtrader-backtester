import backtrader as bt

class BollingerStrategy(bt.Strategy):
    params = dict(period=20, devfactor=2)

    def __init__(self):
        self.boll = bt.indicators.BollingerBands(
            period=self.p.period,
            devfactor=self.p.devfactor
        )

    def next(self):
        if not self.position:
            if self.data.close < self.boll.bot:
                self.buy()

        else:
            if self.data.close > self.boll.top:
                self.sell()
