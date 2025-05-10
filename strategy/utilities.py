def check_order_pending(order):
    if order:
        if order.status in [order.Completed, order.Margin, order.Rejected]:
            order = None
        else:
            return True

    return False


def liquidation(strategy, only_short=False):
    if (
        strategy.broker.get_value()
        < strategy.broker.startingcash * strategy.liquidation_threshold
        and (strategy.position.size < 0 or not only_short)
    ):
        for data in strategy.datas:
            strategy.order = strategy.close(data=data)
        for order in list(strategy.broker.orders):
            strategy.cancel(order)
        strategy.liquidated = True
        strategy.log(f"Liquidated")
        return True

    return False


if __name__ == "__main__":
    pass
