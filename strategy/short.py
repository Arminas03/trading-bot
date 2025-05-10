from strategy.base_strategy import BaseStrategy
from strategy.utilities import *
from datetime import datetime


class Short(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.order = None

    def next(self):
        if check_order_pending(self.order) or self.liquidated:
            return

        if liquidation(self, True):
            return

        if not self.position:
            for data in self.datas:
                self.order = self.sell(
                    data=data,
                    size=(self.broker.get_cash() / len(self.datas)) / data.close,
                )
