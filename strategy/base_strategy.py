import backtrader as bt
import pandas as pd


class BaseStrategy(bt.Strategy):
    def __init__(self):
        self.logs = []
        self.liquidated = False
        self.liquidation_threshold = 0.1

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()} {txt}")

    def notify_order(self, order):
        if order.status in [order.Rejected, order.Canceled, order.Margin]:
            # self.log("Order Rejected/Canceled")
            return

        if order.status in [order.Completed]:
            self.logs.append(
                {
                    "date": f"{self.datas[0].datetime.datetime(0).strftime("%Y-%m-%d %H:%M:%S")}",
                    "product": order.data._name,
                    "quantity": round(order.executed.size, 2),
                    "price": round(order.executed.price, 2),
                }
            )

    def stop(self):
        pd.DataFrame(self.logs).to_excel("trades.xlsx", index=False)
