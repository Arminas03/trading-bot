import backtrader as bt
from datetime import datetime
import yfinance as yf


def add_data(
    cerebro: bt.Cerebro,
    tickers: list,
    start="2014-01-01",
    end="2025-01-01",
    interval="1d",
):
    for ticker in tickers:
        cerebro.adddata(
            bt.feeds.PandasData(
                dataname=yf.download(
                    ticker, start, end, multi_level_index=False, interval=interval
                )
            ),
            name=ticker,
        )


def check_order_pending(order):
    if order:
        if order.status in [order.Completed, order.Margin, order.Rejected]:
            order = None
        else:
            return True

    return False


def short_liquidation(strategy):
    if (
        strategy.broker.get_value()
        < strategy.initial_cash * strategy.params.liquidation_threshold
        and strategy.position.size < 0
    ):
        for data in strategy.datas:
            strategy.order = strategy.close(data=data)
        strategy.liquidated = True
        strategy.log(f"Liquidated")
        return True

    return False


if __name__ == "__main__":
    pass
