import backtrader as bt
from strategy.base_strategy import BaseStrategy
from utilities import check_order_pending
from datetime import datetime, timedelta


class MACrossover(BaseStrategy):
    params = (
        ("slow_sma_period", 200),
        ("fast_sma_period", 30),
    )

    def __init__(self):
        self.order = None
        
        self.slow_sma = bt.indicators.MovingAverageSimple(
            self.datas[0], period = self.params.slow_sma_period
        )
        self.fast_sma = bt.indicators.MovingAverageSimple(
            self.datas[0], period = self.params.fast_sma_period
        )


    def next(self):
        if check_order_pending(self.order):
            return

        if self.datas[0].datetime.date(0) >= datetime.now().date() - timedelta(days=3):
            self.order = self.close()
            return
        
        if not self.position:
            if self.slow_sma[0] < self.fast_sma[0]:
                self.order = self.buy(size = 10)
            if self.slow_sma[0] > self.fast_sma[0]:
                self.order = self.sell(size = 10)
        else:
            if (
                (self.position.size < 0 and self.slow_sma[0] < self.fast_sma[0]) or
                (self.position.size > 0 and self.slow_sma[0] > self.fast_sma[0])
            ):
                self.order = self.close()