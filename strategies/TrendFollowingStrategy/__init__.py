from jesse.strategies import Strategy
from jesse import utils
import numpy as np
import jesse.indicators as ta

class TrendFollowingStrategy(Strategy):

    @property
    def trend(self):
        # short_ema = ta.ema(self.candles, 50)
        # long_ema = ta.ema(self.candles, 100)
        # longer_ema = ta.ema(self.candles, 200)

        # if short_ema > long_ema > longer_ema:
        #     return 1
        # elif short_ema < long_ema < longer_ema:
        #     return -1
        # else:
        #     return 0


        short_ema = ta.ema(self.candles, 13)
        long_ema = ta.ema(self.candles, 20)
        longer_ema = ta.ema(self.candles, 50)
        
        if short_ema > long_ema > longer_ema:
            return 1
        elif short_ema < long_ema < longer_ema:
            return -1
        else:
            return 0

    @property
    def current_candle_touches_long_ema(self):
        long_ema = ta.ema(self.candles, 20)
        return self.high >= long_ema >= self.low

    def should_long(self) -> bool:
        return self.current_candle_touches_long_ema and self.trend == 1

    def should_short(self) -> bool:
        return self.current_candle_touches_long_ema and self.trend == -1

    def should_cancel(self) -> bool:
        return True

    def go_long(self):
        entry = self.high
        stop = entry - ta.atr(self.candles)*3
        qty = utils.risk_to_qty(self.capital, 5, entry, stop, self.fee_rate)

        # highest price of the last 20 bars
        last_20_highs = self.candles[-20:, 3]
        previous_high = np.max(last_20_highs)

        self.buy = qty, entry
        self.stop_loss = qty, stop
        self.take_profit = qty/2, previous_high

    def go_short(self):
        entry = self.low
        stop = entry + ta.atr(self.candles) * 3
        qty = utils.risk_to_qty(self.capital, 5, entry, stop, self.fee_rate)

        # lowest price of the last 20 bars
        last_20_lows = self.candles[-20:, 4]
        previous_low = np.min(last_20_lows)

        self.sell = qty, entry
        self.stop_loss = qty, stop
        self.take_profit = qty / 2, previous_low

    def on_reduced_position(self, order):
        self.stop_loss = self.position.qty, self.position.entry_price

    def update_position(self):
        # the RSI logic is intended for the second half of the trade
        if self.reduced_count > 0:
            rsi = ta.rsi(self.candles)

            if self.is_long and rsi > 80:
                # self.liquidate() closes the position with a market order
                self.liquidate()
            elif self.is_short and rsi < 20:
                self.liquidate()

    def reward_to_risk_filter(self):
        profit = abs(self.average_entry_price - self.average_take_profit)
        loss = abs(self.average_entry_price - self.average_stop_loss)
        win_loss_ratio = profit / loss
        return win_loss_ratio > 1

    def filters(self):
        return [
            self.reward_to_risk_filter,
        ]