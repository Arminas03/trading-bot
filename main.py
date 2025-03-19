import backtrader as bt
from buy_hold_spy import BuyHoldSpy
from import_data import add_data


def add_analyzers(cerebro: bt.Cerebro):
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name = "sharpe_ratio")
    cerebro.addanalyzer(bt.analyzers.Returns, _name = "returns")


def print_analysis(run, cerebro):
    print(f"Sharpe: {round(
        run[0].analyzers.sharpe_ratio.get_analysis()["sharperatio"], 4
    )}")
    print(f"Net profit: {round(cerebro.broker.get_value() - 100_000, 2)}")


def main():
    cerebro = bt.Cerebro()
    cerebro.addstrategy(BuyHoldSpy)
    cerebro.broker.set_cash(100_000)

    add_data(cerebro)
    add_analyzers(cerebro)
    
    run = cerebro.run()

    cerebro.plot()
    print_analysis(run, cerebro)


if __name__ == "__main__":
    main()