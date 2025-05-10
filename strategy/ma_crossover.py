import backtrader as bt
from strategy.base_strategy import BaseStrategy
from strategy.utilities import *
from datetime import datetime


class MACrossover(BaseStrategy):
    params = (("slow_sma_period", 200), ("fast_sma_period", 50))

    def __init__(self):
        super().__init__()
        self.order = None

        self.slow_sma = bt.indicators.MovingAverageSimple(
            self.datas[0], period=self.params.slow_sma_period
        )
        self.fast_sma = bt.indicators.MovingAverageSimple(
            self.datas[0], period=self.params.fast_sma_period
        )

    def next(self):
        if check_order_pending(self.order) or self.liquidated:
            return

        if liquidation(self, True):
            return

        if not self.position:
            if self.slow_sma[0] < self.fast_sma[0]:
                self.order = self.buy(size=self.broker.get_cash() / self.datas[0].close)
            if self.slow_sma[0] > self.fast_sma[0]:
                self.order = self.sell(
                    size=self.broker.get_cash() / self.datas[0].close
                )
        else:
            if (self.position.size < 0 and self.slow_sma[0] < self.fast_sma[0]) or (
                self.position.size > 0 and self.slow_sma[0] > self.fast_sma[0]
            ):
                self.order = self.close()
