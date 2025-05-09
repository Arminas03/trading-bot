import backtrader as bt
from strategy.long import Long
from strategy.short import Short
from strategy.basic_sma import BasicSma
from strategy.ma_crossover import MACrossover
from utilities import add_data
from custom_analyzers import *
from strategy_analysis import strategy_analysis
from datetime import datetime


def add_analyzers(cerebro: bt.Cerebro):
    cerebro.addanalyzer(ReturnAnalyzer, _name="return_analyzer")
    cerebro.addanalyzer(TradePnlAnalyzer, _name="trade_pnl_analyzer")


def main():
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MACrossover)

    cerebro.broker.set_cash(10000)

    add_data(cerebro, ["AAPL"], start="2025-05-02", end="2025-05-09", interval="1m")
    add_analyzers(cerebro)

    run = cerebro.run()
    strategy_analysis(run)


if __name__ == "__main__":
    main()
