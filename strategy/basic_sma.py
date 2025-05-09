import backtrader as bt
from datetime import datetime, timedelta
from strategy.base_strategy import BaseStrategy
from utilities import check_order_pending


class BasicSma(BaseStrategy):
    params = (("sma_period", 30),)

    def __init__(self):
        super().__init__()
        self.order = None
        self.sma = bt.indicators.MovingAverageSimple(
            self.datas[0], period=self.params.sma_period
        )

    def next(self):
        if check_order_pending(self.order):
            return

        if not self.position:
            if self.datas[0].close > self.sma[0]:
                self.order = self.buy(
                    size=self.broker.get_cash() // self.datas[0].close
                )
        elif self.datas[0].close < self.sma[0]:
            self.order = self.sell(size=self.position.size)
