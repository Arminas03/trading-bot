import backtrader as bt
from datetime import datetime, timedelta
from strategy.base_strategy import BaseStrategy


class BasicSma(BaseStrategy):
    params = (("sma_period", 30),)

    def __init__(self):
        self.order = None
        self.sma = bt.indicators.MovingAverageSimple(self.datas[0], period = self.params.sma_period)


    def next(self):
        if self.order:
            if self.order.status in [self.order.Completed, self.order.Margin, self.order.Rejected]:
                self.order = None
            else:
                return
            
        if self.datas[0].datetime.date(0) >= datetime.now().date() - timedelta(days=3):
            self.order = self.close()
            return

        if not self.position:
            if self.datas[0].close > self.sma[0]:
                self.order = self.buy(
                    size = self.broker.get_cash() // self.datas[0].close
                )
        elif self.datas[0].close < self.sma[0]:
            self.order = self.sell(
                size = self.position.size
            )
