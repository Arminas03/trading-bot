from strategy.base_strategy import BaseStrategy
from datetime import timedelta
from strategy.utilities import liquidation
from backtrader import Order


class MarketMaking(BaseStrategy):
    def __init__(self):
        super().__init__()

    def next(self):
        if self.liquidated or liquidation(self):
            return

        curr_price = self.datas[0].close

        if not self.position:
            self.buy(
                price=curr_price - 200,
                size=self.broker.get_cash() / curr_price / 20,
                valid=self.datas[0].datetime.datetime(0) + timedelta(minutes=10),
                exectype=Order.Limit,
            )
            self.sell(
                price=curr_price + 200,
                size=self.broker.get_cash() / curr_price / 20,
                valid=self.datas[0].datetime.datetime(0) + timedelta(minutes=10),
                exectype=Order.Limit,
            )
