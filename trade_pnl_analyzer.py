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
