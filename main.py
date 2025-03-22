import backtrader as bt
from strategy.long import Long
from strategy.short import Short
from strategy.basic_sma import BasicSma
from strategy.ma_crossover import MACrossover
from utilities import add_data
import plotly.graph_objects as go


def add_analyzers(cerebro: bt.Cerebro):
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name = "sharpe_ratio")
    cerebro.addanalyzer(bt.analyzers.Returns, _name = "returns")
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name = "trade_analyzer")
    cerebro.addanalyzer(bt.analyzers.TimeReturn, _name = "time_return")


def plot_strategy_equity(returns, dates):
    open_returns = returns[:-1]
    close_returns = returns[1:]

    go.Figure(
        data = go.Candlestick(
            x = dates,
            open = open_returns,
            high = returns,
            low = returns,
            close = close_returns
        )
    ).show()


def strategy_analysis(run, initial_cash):
    dates = list(run[0].analyzers.time_return.get_analysis().keys())
    time_returns = list(run[0].analyzers.time_return.get_analysis().values())
    
    for i in range(len(time_returns)):
        if i == 0:
            time_returns[i] = 10000
            continue
        time_returns[i] = time_returns[i-1] * (1 + time_returns[i])
    
    print(f"Sharpe: {round(
        run[0].analyzers.sharpe_ratio.get_analysis()["sharperatio"], 4
    )}")
    print(f"Net profit: {round(time_returns[-1] - initial_cash, 2)}")
    plot_strategy_equity(time_returns, dates)


def main():
    initial_cash = 10000
    cerebro = bt.Cerebro()
    cerebro.addstrategy(Short)

    cerebro.broker.set_cash(initial_cash)

    add_data(cerebro, ["SPY"], start = "2014-01-01")
    add_analyzers(cerebro)
    
    run = cerebro.run()
    strategy_analysis(run, initial_cash)


if __name__ == "__main__":
    main()
