import backtrader as bt
from custom_analyzers import *
from strategy_analysis import strategy_analysis
from data import *

from strategy.long import Long
from strategy.short import Short
from strategy.basic_sma import BasicSma
from strategy.ma_crossover import MACrossover
from strategy.market_making import MarketMaking
from strategy.mean_reversion import MeanReversion


def add_analyzers(cerebro: bt.Cerebro):
    cerebro.addanalyzer(ReturnAnalyzer, _name="return_analyzer")
    cerebro.addanalyzer(TradePnlAnalyzer, _name="trade_pnl_analyzer")


def main():
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MeanReversion)

    cerebro.broker.set_cash(10000)

    add_polygon_data(
        cerebro,
        ["C:USDEUR"],
        PolygonDataConfig(
            multiplier=1, timespan="minute", from_="2024-01-01", to="2024-06-01"
        ),
    )

    add_analyzers(cerebro)

    run = cerebro.run()
    strategy_analysis(run, dash_name="Long BTC", annualisation_const=60 * 24 * 365)


if __name__ == "__main__":
    main()
