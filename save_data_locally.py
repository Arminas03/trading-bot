import sqlite3
from polygon import RESTClient
from dotenv import load_dotenv
from datetime import datetime
import os
import pandas as pd
from data import PolygonDataConfig


def get_data_from_polygon(ticker, polygon_data_config):
    client = RESTClient(api_key=os.getenv("POLYGON_IO_API_KEY"))
    aggs = list(client.list_aggs(ticker=ticker, **polygon_data_config.__dict__))

    return pd.DataFrame(
        {
            "ticker": ticker,
            "date": [datetime.fromtimestamp(agg.timestamp / 1000) for agg in aggs],
            "open": [agg.open for agg in aggs],
            "high": [agg.high for agg in aggs],
            "low": [agg.low for agg in aggs],
            "close": [agg.close for agg in aggs],
            "volume": [agg.volume for agg in aggs],
        }
    ).set_index(["ticker", "date"])


def update_db(df, multiplier, timespan):
    conn = sqlite3.connect("ohlcv_data.sqlite")

    df.to_sql(f"stock_{multiplier}_{timespan}", conn, if_exists="append", index=True)
    conn.commit()

    conn.close()


def main():
    tickers = ["SPY", "MSFT"]
    multiplier, timespan = 1, "minute"

    polygon_data_config = PolygonDataConfig(
        multiplier=multiplier, timespan=timespan, from_="2025-01-01", to="2025-05-01"
    )
    for ticker in tickers:
        df = get_data_from_polygon(ticker, polygon_data_config)
        update_db(df, multiplier=multiplier, timespan=timespan)


if __name__ == "__main__":
    load_dotenv()
    main()
