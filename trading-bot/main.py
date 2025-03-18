# region imports
from AlgorithmImports import *
# endregion

class SquareLightBrownBuffalo(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2013, 1, 1)
        self.set_end_date(2020, 1, 1)
        self.set_cash(100000)
        self.add_equity("SPY", Resolution.Daily)
        self.spy = self.symbol("SPY")


    def on_data(self, data: Slice):
        if not self.portfolio.invested:
            self.set_holdings(self.spy, 1)
            self.log("bought SPY")
        self.log(f"Total Portfolio Value: {self.portfolio.total_portfolio_value}")
