import backtrader as bt
from strategy.long import Long
from strategy.short import Short
from strategy.basic_sma import BasicSma
from strategy.ma_crossover import MACrossover
from utilities import add_data
import plotly.graph_objects as go
from trade_pnl_analyzer import TradePnlAnalyzer


def add_analyzers(cerebro: bt.Cerebro):
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe_ratio")
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trade_analyzer")
    cerebro.addanalyzer(bt.analyzers.TimeReturn, _name="time_return")
    cerebro.addanalyzer(TradePnlAnalyzer, _name="trade_pnl_analyzer")


def performance_metrics(run):
    print(
        f"Sharpe: {round(
        run[0].analyzers.sharpe_ratio.get_analysis()["sharperatio"], 4
    )}"
    )
    print(
        f"Net profit: {round(
            run[0].analyzers.trade_analyzer.get_analysis().pnl.net.total, 2
    )}"
    )


def plot_strategy_equity(returns, dates):
    open_returns = returns[:-1]
    close_returns = returns[1:]

    figure = go.Figure(
        data=go.Candlestick(
            x=dates, open=open_returns, high=returns, low=returns, close=close_returns
        )
    )
    figure.update_layout(title="Equity", yaxis_title="$")
    figure.show()


def time_return_analysis(time_returns, dates):
    for i in range(len(time_returns)):
        if i == 0:
            time_returns[i] = 10000
            continue
        time_returns[i] = time_returns[i - 1] * (1 + time_returns[i])

    plot_strategy_equity(time_returns, dates)


def pnl_distribution_analysis(trade_pnl):
    pnl_figure = go.Figure(
        data=[
            go.Histogram(
                x=[trade_pnl[trade_ref]["pnl"] for trade_ref in trade_pnl.keys()]
            )
        ]
    )
    pnl_figure.update_layout(
        title="Trade P&L", xaxis_title="P&L", yaxis_title="Frequency"
    )
    pnl_figure.show()


def strategy_analysis(run):
    performance_metrics(run)
    time_return_analysis(
        list(run[0].analyzers.time_return.get_analysis().values()),
        list(run[0].analyzers.time_return.get_analysis().keys()),
    )
    pnl_distribution_analysis(run[0].analyzers.trade_pnl_analyzer.get_analysis())


def main():
    cerebro = bt.Cerebro()
    cerebro.addstrategy(Long)

    cerebro.broker.set_cash(10000)

    add_data(cerebro, ["SPY"], start="2001-01-01")
    add_analyzers(cerebro)

    run = cerebro.run()
    strategy_analysis(run)


if __name__ == "__main__":
    main()
