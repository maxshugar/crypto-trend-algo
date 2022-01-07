from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils
import time


import matplotlib.pyplot as plt
import numpy as np


class ExampleStrategy(Strategy):
    def should_long(self) -> bool:
        # ema13 = ta.ema(self.candles, period=13, source_type="close", sequential=False)
        # ema20 = ta.ema(self.candles, period=20, source_type="close", sequential=False)
        # if(ema13 > ema20 and self.low <= ema13):
        #     return True
        return False

    def should_short(self) -> bool:
        return False

    def should_cancel(self) -> bool:
        return False

    def go_long(self):
        # qty = utils.risk_to_qty(self.capital, 1, self.price, self.low - 10, self.fee_rate)
        # self.buy = qty, self.price
        # self.stop_loss = qty, self.low - 10
        # self.take_profit = qty, self.high + 20
        pass

    def go_short(self):
        pass

    def update_position(self):
        # qty = self.position.qty 
        # ema20 = ta.ema(self.candles, period=20, source_type="close", sequential=False)
        # print(ema20, self.close)
        # if(self.is_long and self.close < ema20):
        #     self.liquidate()
        pass

    def before(self):
        print(self.candles[0])
        time.sleep(1)
        # plt.figure()
        #x = self.candles
        # y = np.sin(x)
        # plt.plot(x, y)
        # plt.show()
