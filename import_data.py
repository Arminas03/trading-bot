import yfinance as yf
import backtrader as bt


SECURITIES = {security: i for i, security in enumerate([
    "SPY"
])}


def helper_add(cerebro: bt.Cerebro, ticker, start, end):
    cerebro.adddata(
        bt.feeds.PandasData(
            dataname = yf.download(
                ticker, start, end, multi_level_index = False
                )
        )
    )


def add_data(cerebro: bt.Cerebro):
    print(yf.download("SPY", "2015-1-5", "2015-1-6"))

    for security in SECURITIES.keys():
        helper_add(cerebro, security, "2015-01-01", "2025-01-01")


if __name__ == "__main__":
    pass