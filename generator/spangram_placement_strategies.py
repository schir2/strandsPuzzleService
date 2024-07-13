import random
from abc import ABC, abstractmethod


class SpangramPlacementStrategy(ABC):
    rows: int = None
    cols: int = None
    spangram: str = None
    board: list[list[str | None]]
    vertices: set[tuple[tuple[int, int], tuple[int, int]]]

    def __init__(self, rows, cols, spangram, board):
        self.rows = rows
        self.cols = cols
        self.board = board
        self.spangram = spangram
        self.path = []

    def crossed_diagonally(self, row: int, col: int) -> bool:
        return False

    @property
    @abstractmethod
    def direction(self) -> tuple:
        raise NotImplementedError

    def get_next_spangram_letter_position(self, index: int) -> tuple[int, int]:
        raise NotImplementedError

    def place_spangram(self):
        starting_row, starting_col = self.select_starting_position()

        self.board[starting_row][starting_col] = self.spangram[0]
        self.path.append((starting_row, starting_col))

        for i in range(1, len(self.spangram)):
            next_row, next_col = self.get_next_spangram_letter_position(index=i)
            self.board[next_row][next_col] = self.spangram[i]
            self.path.append((next_row, next_col))
            self.vertices.add((self.path[-2], self.path[-1]))

    def dfs(self, i):
        if i == len(self.spangram) - 1:
            ...

    @abstractmethod
    def distance_form_end(self, row, col):
        raise NotImplementedError

    @abstractmethod
    def select_starting_position(self) -> tuple[int, int]:
        raise NotImplementedError


class LeftToRightStrategy(SpangramPlacementStrategy):
    direction = (0, 1)

    def distance_form_end(self, row, col):
        return self.cols - col

    def select_starting_position(self) -> tuple[int, int]:
        return random.randint(0, self.rows - 1), 0


class RightToLeftStrategy(SpangramPlacementStrategy):
    direction = (0, -1)

    def distance_form_end(self, row, col):
        return col

    def select_starting_position(self) -> tuple[int, int]:
        return random.randint(0, self.rows - 1), self.cols - 1


class UpToDownStrategy(SpangramPlacementStrategy):
    direction = (1, 0)

    def distance_form_end(self, row, col):
        return self.rows - row

    def select_starting_position(self):
        return 0, random.randint(0, self.cols - 1)


class DownToUpStrategy(SpangramPlacementStrategy):
    direction = (-1, 0)

    def distance_form_end(self, row, col):
        return row

    def select_starting_position(self):
        return self.rows - 1, random.randint(0, self.cols - 1)
