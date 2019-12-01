import numpy as np
from dataclasses import dataclass
from enum import Enum


class ProfitCalculator(object):

    @dataclass()
    class Context:
        class Flag(Enum):
            BUY = 1
            HOLD = 0
            SELL = -1

        class Mode(Enum):
            WITH_HOLD = 0
            WITHOUT_HOLD = 1

        price_list: list
        flag_list: list
        mode: Mode
        spread: float


    def __init__(self, context:Context):
        self._context = context
        self._check_data()
        self._position = None
        self._position_flag = None

    def _check_data(self):
        if len(self._context.price_list) != len(self._context.flag_list):
            raise ValueError("Size of lists does not match.")

    def get_total_profit(self):
        return self.get_profit_list().sum()

    def get_profit_list(self):
        import numpy as np
        result = np.zeros((len(self._context.price_list)), dtype=float)
        for i, v in enumerate(self._context.price_list):
            result[i] = self._check_period(self._context.price_list[i], self._context.flag_list[i])
        return result

    def _check_period(self, current, flag):
        if self._context.mode == self.Context.Mode.WITH_HOLD:
            if flag == self.Context.Flag.HOLD:
                return 0
        if flag == self._position_flag:
            return 0
        answer = self.close_posision(current, flag)
        self.create_position(current, flag)
        return answer

    def create_position(self, current, flag):
        if flag == self.Context.Flag.HOLD or self._position is not None or self._position_flag is not None:
            return
        self._position = current
        self._position_flag = flag

    def close_posision(self, current, flag):
        try:
            if self._position is None or self._position_flag is None:
                return 0
            if self._position_flag == self.Context.Flag.BUY:
                return current - self._position - self._context.spread
            elif self._position_flag == self.Context.Flag.SELL:
                return self._position - current - self._context.spread
        finally:
            self._position = None
            self._position_flag = None
