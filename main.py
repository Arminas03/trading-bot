import backtrader as bt
from buy_hold_spy import BuyHoldSpy, add_data


def add_analyzers(cerebro: bt.Cerebro):
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name = "sharpe_ratio")
    cerebro.addanalyzer(bt.analyzers.Returns, _name = "returns")
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name = "trade_analyzer")


def print_analysis(run):
    print(f"Sharpe: {round(
        run[0].analyzers.sharpe_ratio.get_analysis()["sharperatio"], 4
    )}")
    trade_analysis = run[0].analyzers.trade_analyzer.get_analysis()
    print(f"Net profit: {round(trade_analysis.pnl.net.total, 2)}")


def main():
    cerebro = bt.Cerebro()
    cerebro.addstrategy(BuyHoldSpy)
    cerebro.broker.set_cash(10000)

    add_data(cerebro)
    add_analyzers(cerebro)
    
    run = cerebro.run()

    cerebro.plot()
    print_analysis(run)


if __name__ == "__main__":
    main()