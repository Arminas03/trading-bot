from strategy.base_strategy import BaseStrategy
from utilities import *
from datetime import datetime


class Short(BaseStrategy):
    params = (("liquidation_threshold", 0.1),)

    def __init__(self):
        self.order = None
        self.liquidated = False
        self.initial_cash = self.broker.get_cash()

    def next(self):
        if check_order_pending(self.order) or self.liquidated:
            return

        if self.datas[0].datetime.date(0) >= datetime(2024, 12, 30).date():
            self.order = self.close()
            return

        if short_liquidation(self):
            return

        if not self.position:
            self.order = self.sell(
                data=self.datas[0], size=self.broker.get_cash() // self.datas[0].close
            )
