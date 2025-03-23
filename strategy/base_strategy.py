import backtrader as bt


class BaseStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()} {txt}")

    def notify_order(self, order):
        if order.status in [order.Rejected, order.Canceled, order.Margin]:
            self.log("Order Rejected/Canceled")
            return

        if order.status in [order.Completed]:
            self.log(
                f"{int(order.executed.size)}x{order.data._name} @ {round(order.executed.price, 2)}"
            )
