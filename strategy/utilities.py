def check_order_pending(order):
    if order:
        if order.status in [order.Completed, order.Margin, order.Rejected]:
            order = None
        else:
            return True

    return False


def short_liquidation(strategy):
    if (
        strategy.broker.get_value()
        < strategy.initial_cash * strategy.params.liquidation_threshold
        and strategy.position.size < 0
    ):
        for data in strategy.datas:
            strategy.order = strategy.close(data=data)
        strategy.liquidated = True
        strategy.log(f"Liquidated")
        return True

    return False


if __name__ == "__main__":
    pass
