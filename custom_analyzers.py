import backtrader as bt
from datetime import datetime


class TradePnlAnalyzer(bt.Analyzer):
    def __init__(self):
        self.trades = dict()

    def notify_trade(self, trade: bt.Trade):
        if trade.isclosed:
            self.trades[trade.ref] = {
                "close_date": trade.close_datetime().date(),
                "pnl": trade.pnl,
            }

    def get_analysis(self):
        return self.trades


class ReturnAnalyzer(bt.Analyzer):
    def __init__(self):
        self.returns = dict()

    def start(self):
        self.initial_cash = self.strategy.broker.startingcash

    def next(self):
        if len(self.data) <= 1:
            return

        self.returns[self.data.datetime.datetime(0)] = (
            self.data.close[0] / self.data.close[-1] - 1
        )

    def get_return_dict(self):
        return self.returns

    def get_final_return(self):
        ret = self.initial_cash
        for r in self.returns.values():
            ret *= 1 + r
        return ret - 1
