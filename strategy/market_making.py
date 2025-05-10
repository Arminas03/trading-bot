from strategy.base_strategy import BaseStrategy
from datetime import timedelta
from strategy.utilities import liquidation
from backtrader import Order


class MarketMaking(BaseStrategy):
    params = (
        ("bid_spread", 1000),
        ("ask_spread", 1000),
        ("size_multiplier", 0.05),
        ("valid_for_min", 5),
        ("mm_depth", 3),
        ("bid_increment", 500),
        ("ask_increment", 500),
        ("quote_every_n_min", 5),
    )

    def __init__(self):
        super().__init__()

    def next(self):
        if self.liquidated or liquidation(self):
            return

        if (
            self.datas[0].datetime.datetime(0).minute % self.params.quote_every_n_min
            != 0
        ):
            return

        curr_price = self.datas[0].close

        for i in range(self.params.mm_depth):
            self.buy(
                price=curr_price
                - (self.params.bid_spread + i * self.params.bid_increment),
                size=self.broker.get_cash() / curr_price * self.params.size_multiplier,
                valid=self.datas[0].datetime.datetime(0)
                + timedelta(minutes=self.params.valid_for_min),
                exectype=Order.Limit,
            )
            self.sell(
                price=curr_price
                + (self.params.ask_spread + i * self.params.ask_increment),
                size=self.broker.get_cash() / curr_price * self.params.size_multiplier,
                valid=self.datas[0].datetime.datetime(0)
                + timedelta(minutes=self.params.valid_for_min),
                exectype=Order.Limit,
            )
