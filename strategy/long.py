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
            for data in self.datas:
                self.order = self.close(data=data)
            return

        if not self.position:
            for data in self.datas:
                self.order = self.buy(
                    data=data,
                    size=(self.broker.get_cash() // len(self.datas)) // data.close,
                )
