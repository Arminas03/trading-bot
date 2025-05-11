import backtrader as bt
from datetime import datetime
import numpy as np


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
        self.prev_portfolio_value = None

    def next(self):
        if not self.prev_portfolio_value or self.prev_portfolio_value == 0:
            self.prev_portfolio_value = self.strategy.broker.getvalue()
            return

        self.returns[self.data.datetime.datetime(0)] = (
            self.strategy.broker.getvalue() / self.prev_portfolio_value - 1
        )

        self.prev_portfolio_value = self.strategy.broker.getvalue()

    def get_return_dict(self):
        return self.returns

    def get_starting_cash(self):
        return self.strategy.broker.startingcash

    def get_final_return(self):
        ret = self.strategy.broker.startingcash
        for r in self.returns.values():
            ret *= 1 + r
        return ret - self.strategy.broker.startingcash

    def get_sharpe_ratio(self, risk_free_rate=0.0):
        excess_returns = np.array(list(self.returns.values())) - risk_free_rate
        return (
            np.mean(excess_returns) / np.std(excess_returns, ddof=1)
            if len(excess_returns) > 1
            else float("nan")
        )

    def get_sortino_ratio(self, risk_free_rate=0.0):
        excess_returns = np.array(list(self.returns.values())) - risk_free_rate
        negative_returns = excess_returns[excess_returns < 0]

        return (
            np.mean(excess_returns) / np.std(negative_returns, ddof=1)
            if len(negative_returns) > 1
            else float("nan")
        )
