import backtrader as bt
from datetime import datetime, timedelta
import yfinance as yf


SECURITIES = {"SPY": 0}


class BuyHoldSpy(bt.Strategy):
    def __init__(self):
        self.order = None

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')


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
                data = self.datas[SECURITIES["SPY"]],
                size = self.broker.get_cash() // self.datas[SECURITIES["SPY"]].close
            )


    def notify_order(self, order):
        if order.status in [order.Rejected, order.Canceled, order.Margin]:
            self.log("Order Rejected/Canceled")
            return

        if order.status in [order.Completed]:
            self.log(f"{int(order.executed.size)}x{order.data._name} @ {round(order.executed.price, 2)}")


def add_data(cerebro: bt.Cerebro, start="2015-01-01"):
    cerebro.adddata(
        bt.feeds.PandasData(
            dataname = yf.download(
                "SPY", start, multi_level_index = False
                )
        )
    )


if __name__ == "__main__":
    pass