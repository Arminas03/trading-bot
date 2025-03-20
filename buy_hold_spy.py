from datetime import datetime, timedelta
from base_strategy import BaseStrategy


class BuyHoldSpy(BaseStrategy):
    def __init__(self):
        self.order = None


    def next(self):
        if self.order:
            if self.order.status in [self.order.Completed]:
                self.order = None
            else:
                return

        if self.datas[0].datetime.date(0) >= datetime.now().date() - timedelta(days=3):
            self.order = self.close()
            return

        if not self.position:
            self.order = self.buy(
                data = self.datas[0],
                size = self.broker.get_cash() // self.datas[0].close
            )
