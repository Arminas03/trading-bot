from strategy.base_strategy import BaseStrategy
from strategy.utilities import liquidation


class MeanReversion(BaseStrategy):
    params = (
        ("ma_period", 200),
        ("n_std_to_enter", 2),
        ("n_std_to_close", 1),
        ("n_std_stop_loss", 1),
    )

    def __init__(self):
        super().__init__()
        self.moving_window = []
        self.price_to_close = -1
        self.stop_loss = -1

    def next(self):
        if self.liquidated or liquidation(self):
            return

        if len(self.moving_window) < self.params.ma_period:
            self.moving_window.append(self.datas[0].close)
            return

        mean_price = sum(self.moving_window) / self.params.ma_period
        std_price = sum((price - mean_price) ** 2 for price in self.moving_window) / (
            self.params.ma_period - 1
        )

        if not self.position:
            self.enter_far_from_mean(self.datas[0].close, mean_price, std_price)
        elif self.check_to_close_position(self.datas[0].close, self.position.size > 0):
            self.close()

        self.moving_window.append(self.datas[0].close)
        self.moving_window.pop(0)

    def enter_far_from_mean(self, curr_price, mean_price, std_price):
        if curr_price > mean_price + self.params.n_std_to_enter * std_price:
            self.sell(size=self.broker.get_cash() / curr_price)

            self.price_to_close = mean_price + self.params.n_std_to_close * std_price
            self.stop_loss = curr_price + self.params.n_std_stop_loss * std_price
        if curr_price < mean_price - self.params.n_std_to_enter * std_price:
            self.buy(size=self.broker.get_cash() / curr_price)

            self.price_to_close = mean_price - self.params.n_std_to_close * std_price
            self.stop_loss = curr_price - self.params.n_std_stop_loss * std_price

    def check_to_close_position(self, curr_price, is_position_long):
        if is_position_long:
            return curr_price > self.price_to_close or curr_price < self.stop_loss
        else:
            return curr_price < self.price_to_close or curr_price > self.stop_loss
