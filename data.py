import backtrader as bt
import yfinance as yf
from dataclasses import dataclass
import os
from dotenv import load_dotenv
from polygon import RESTClient
import pandas as pd
from datetime import datetime


@dataclass
class PolygonDataConfig:
    multiplier: int
    timespan: str
    from_: str
    to: str
    adjusted: str = "true"
    sort: str = "asc"
    limit: int = 50_000


def add_yfinance_data(
    cerebro, tickers, start="2014-01-01", end="2025-01-01", interval="1d"
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


def add_polygon_data(cerebro, tickers, polygon_config: PolygonDataConfig):
    load_dotenv()
    client = RESTClient(api_key=os.getenv("POLYGON_IO_API_KEY"))

    for ticker in tickers:
        aggs = list(client.list_aggs(ticker=ticker, **polygon_config.__dict__))

        cerebro.adddata(
            bt.feeds.PandasData(
                dataname=pd.DataFrame(
                    {
                        "date": [
                            datetime.fromtimestamp(agg.timestamp / 1000) for agg in aggs
                        ],
                        "open": [agg.open for agg in aggs],
                        "high": [agg.high for agg in aggs],
                        "low": [agg.low for agg in aggs],
                        "close": [agg.close for agg in aggs],
                        "volume": [agg.volume for agg in aggs],
                    }
                ).set_index("date")
            ),
            name=ticker,
        )
