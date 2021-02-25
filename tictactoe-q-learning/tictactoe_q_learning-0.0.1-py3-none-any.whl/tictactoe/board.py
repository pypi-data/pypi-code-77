import numpy as np


class Board:
    array: np.ndarray
    ROWS: int = 3
    COLUMNS: int = 3

    def __init__(self) -> None:
        self.size = self.ROWS * self.COLUMNS
        self.reset()

    @property
    def state(self) -> np.ndarray:
        return self.array.reshape(self.size)

    def reset(self):
        self.array = np.zeros((self.ROWS, self.COLUMNS))

    def set_value(self, row: int, column: int, value: float):
        self.array[row][column] = value

    def print(self, symbol1: str, symbol2: str, void_symbol: str):
        for i, row in enumerate(self.array):
            row_values = [int(x) for x in row.tolist()]
            row_symbols = [symbol1 if x > 0 else symbol2 if x <
                           0 else void_symbol for x in row_values]
            print(' | '.join(row_symbols))
            if i < len(row) - 1:
                print('--'*(len(row)*2-1))

    def winner(self) -> int:
        for i in range(self.ROWS):
            total_column = sum(self.array[:, i])
            total_row = sum(self.array[i, :])
            if total_row == 3 or total_column == 3:
                return 1
            if total_row == -3 or total_column == -3:
                return -1

        total_diag_1 = sum([self.array[i, i] for i in range(self.COLUMNS)])
        total_diag_2 = sum([self.array[i, self.COLUMNS - i - 1]
                            for i in range(self.COLUMNS)])
        if total_diag_1 == 3 or total_diag_2 == 3:
            return 1
        if total_diag_1 == -3 or total_diag_2 == -3:
            return -1

        return 0
