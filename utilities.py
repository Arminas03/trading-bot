import backtrader as bt
from datetime import datetime
import yfinance as yf


def add_data(cerebro: bt.Cerebro, tickers: list, start = "2015-01-01", end = datetime.today()):
    for ticker in tickers:
        cerebro.adddata(
            bt.feeds.PandasData(
                dataname = yf.download(
                    ticker, start, end, multi_level_index = False
                )
            ), name = ticker
        )


if __name__ == "__main__":
    pass