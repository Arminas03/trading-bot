import backtrader as bt
from import_data import SECURITIES

class BuyHoldSpy(bt.Strategy):
    def __init__(self):
        self.order = None

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')


    def next(self):
        if self.order:
            return
        if not self.position:
            print(self.datas[SECURITIES["SPY"]].close)
            self.order = self.buy(
                data = self.datas[SECURITIES["SPY"]],
                size = self.broker.get_cash() // self.datas[SECURITIES["SPY"]].close
            )


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            self.log("Order sent")
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"long {int(order.executed.size)}x{order.data._name} @ {round(order.executed.price, 2)}")