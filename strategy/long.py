from datetime import datetime
from strategy.base_strategy import BaseStrategy
from utilities import check_order_pending


class Long(BaseStrategy):
    def __init__(self):
        self.order = None

    def next(self):
        if check_order_pending(self.order):
            return

        if self.datas[0].datetime.date(0) >= datetime(2024, 12, 30).date():
            self.order = self.close()
            return

        if not self.position:
            self.order = self.buy(
                data=self.datas[0], size=self.broker.get_cash() // self.datas[0].close
            )
