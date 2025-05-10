import backtrader as bt
from strategy.long import Long
from strategy.short import Short
from strategy.basic_sma import BasicSma
from strategy.ma_crossover import MACrossover
from custom_analyzers import *
from strategy_analysis import strategy_analysis
from data import *


def add_analyzers(cerebro: bt.Cerebro):
    cerebro.addanalyzer(ReturnAnalyzer, _name="return_analyzer")
    cerebro.addanalyzer(TradePnlAnalyzer, _name="trade_pnl_analyzer")


def main():
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MACrossover)

    cerebro.broker.set_cash(10000)

    add_polygon_data(
        cerebro,
        ["X:BTCUSD"],
        PolygonDataConfig(
            multiplier=1, timespan="minute", from_="2025-01-01", to="2025-05-09"
        ),
    )

    add_analyzers(cerebro)

    run = cerebro.run()
    strategy_analysis(run)


if __name__ == "__main__":
    main()
