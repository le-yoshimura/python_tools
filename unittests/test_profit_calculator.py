import unittest
import pandas as pd
import numpy as np
from mylib.aspects.aop_unittest import AOPUnitTest
from mylib.fx.profit_calculator import ProfitCalculator


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        flags = ProfitCalculator.Context.Flag
        cls.modes = ProfitCalculator.Context.Mode
        cls._price = [100.0, 100.5, 101, 101.5, 101,
                      100.5, 100, 99.5, 99.0, 99.5,
                      100.0, 100.5, 101, 101.5, 101,
                      100.5, 100, 99.5, 99.0, 99.5, 100, 100.5]
        cls._flag = [flags.HOLD, flags.BUY, flags.HOLD, flags.SELL, flags.HOLD,
                     flags.HOLD, flags.BUY, flags.HOLD, flags.SELL, flags.HOLD,
                     flags.BUY, flags.BUY, flags.HOLD, flags.SELL, flags.SELL,
                     flags.HOLD, flags.BUY, flags.BUY, flags.SELL, flags.SELL, flags.HOLD, flags.BUY
                     ]
        cls._context = ProfitCalculator.Context(cls._price, cls._flag, cls.modes.WITHOUT_HOLD, 0.03)
        cls._calculator = ProfitCalculator(cls._context)

    @AOPUnitTest()
    def test_without_hold(self):
        answer_list = self._calculator.get_profit_list()
        self.assertTrue(sum(answer_list[:5]) > 0)
        self.assertTrue(sum(answer_list[5:]) < 0)
        self.assertTrue(sum(answer_list[10:15]) > 0)
        self.assertTrue(sum(answer_list[15:]) < 0)
        self.assertTrue(round(sum(answer_list), 3) == -0.24)
        df = pd.DataFrame(np.vstack((self._context.price_list, self._context.flag_list, answer_list)).T)
        print(df)

    @AOPUnitTest()
    def test_with_hold(self):
        self._context = ProfitCalculator.Context(self._price, self._flag, self.modes.WITH_HOLD, 0.03)
        self._calculator = ProfitCalculator(self._context)
        answer_list = self._calculator.get_profit_list()
        self.assertTrue(sum(answer_list[3:7]) > 0)
        self.assertTrue(sum(answer_list[7:11]) < 0)
        self.assertTrue(sum(answer_list[11:17]) > 0)
        self.assertTrue(sum(answer_list[17:]) < 0)
        self.assertTrue(round(sum(answer_list), 3) == 0.76)
        df = pd.DataFrame(np.vstack((self._context.price_list, self._context.flag_list, answer_list)).T)
        print(df)

if __name__ == '__main__':
    unittest.main()
