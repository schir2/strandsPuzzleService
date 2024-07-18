import random
from abc import ABC, abstractmethod


class SpangramPlacementStrategy(ABC):
    rows: int = None
    cols: int = None
    spangram: str = None
    valid_boards = []

    def __init__(self, rows, cols, spangram, board):
        self.rows = rows
        self.cols = cols
        self.spangram = spangram

    def crossed_diagonally(self, row: int, col: int) -> bool:
        return False

    @property
    @abstractmethod
    def direction(self) -> tuple:
        raise NotImplementedError

    @property
    @abstractmethod
    def positive_direction_transforms(self) -> list[tuple[int, int]]:
        ...

    @property
    @abstractmethod
    def negative_direction_transforms(self) -> list[tuple[int, int]]:
        ...

    @property
    @abstractmethod
    def neutral_direction_transforms(self) -> list[tuple[int, int]]:
        ...

    def get_next_spangram_letter_position(self, index: int) -> tuple[int, int]:
        ...

    def place_spangram(self):
        starting_row, starting_col = self.select_starting_position()

        board[starting_row][starting_col] = self.spangram[0]
        self.path.append((starting_row, starting_col))

        self.dfs(1)

        for i in range(1, len(self.spangram)):
            next_row, next_col = self.get_next_spangram_letter_position(index=i)
            board[next_row][next_col] = self.spangram[i]
            self.path.append((next_row, next_col))
            vertices.add((self.path[-2], self.path[-1]))

    def dfs(self, row: int, col: int, i: int, path: list[tuple[int, int]], vertices: set[tuple[tuple[int, int]]], board: list[list[str]]) -> None:
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False
        if board[row][col]:
            return False

        distance_from_end = self.distance_form_end(*path[-1])
        if distance_from_end > len(self.spangram) - i:
            return False
        if distance_from_end == 0 and i == len(self.spangram) - 1:
            return True
        if self.crossed_diagonally(row=row, col=col):
            return False

        path.append((row, col))
        vertices.add((path[-2], path[-1]))

        directions = []

        if distance_from_end >= 2:
            for dr, dc in self.negative_direction_transforms:
                directions.append((row + dr, col + dc))
        if distance_from_end >= 1:
            for dr, dc in self.neutral_direction_transforms:
                directions.append((row + dr, col + dc))
        for dr, dc in self.positive_direction_transforms:
            directions.append((row + dr, col + dc))

        for next_row, next_col in directions:
            if not self.dfs(row=next_row, col=next_col, i=i + 1):
                vertices.remove((path[-2], path[-1]))
                path.pop()


    @abstractmethod
    def distance_form_end(self, row, col):
        raise NotImplementedError

    @abstractmethod
    def select_starting_position(self) -> tuple[int, int]:
        raise NotImplementedError


class LeftToRightStrategy(SpangramPlacementStrategy):
    direction = (0, 1)
    positive_direction_transforms = [(0, 1), (-1, 1), (1, 1)]
    negative_direction_transforms = ((0, -1), (-1, -1), (1, -1))
    neutral_direction_transforms = [(1, 0), (-1, 0)]

    def distance_form_end(self, row, col):
        return self.cols - col

    def select_starting_position(self) -> tuple[int, int]:
        return random.randint(0, self.rows - 1), 0


class RightToLeftStrategy(SpangramPlacementStrategy):
    direction = (0, -1)
    positive_direction_transforms = [(0, -1), (-1, -1), (1, -1)]
    negative_direction_transforms = ((0, 1), (-1, 1), (1, 1))
    neutral_direction_transforms = [(1, 0), (-1, 0)]

    def distance_form_end(self, row, col):
        return col

    def select_starting_position(self) -> tuple[int, int]:
        return random.randint(0, self.rows - 1), self.cols - 1


class UpToDownStrategy(SpangramPlacementStrategy):
    direction = (1, 0)
    positive_direction_transforms = [(1, 1), (1, 0), (1, -1)]
    negative_direction_transforms = ((-1, 1), (-1, 0), (-1, -1))
    neutral_direction_transforms = [(0, 1), (0, -1)]

    def distance_form_end(self, row, col):
        return self.rows - row

    def select_starting_position(self):
        return 0, random.randint(0, self.cols - 1)


class DownToUpStrategy(SpangramPlacementStrategy):
    direction = (-1, 0)
    positive_direction_transforms = [(1, 1), (1, 0), (1, -1)]
    negative_direction_transforms = ((-1, 1), (-1, 0), (-1, -1))
    neutral_direction_transforms = [(0, 1), (0, -1)]

    def distance_form_end(self, row, col):
        return row

    def select_starting_position(self):
        return self.rows - 1, random.randint(0, self.cols - 1)
