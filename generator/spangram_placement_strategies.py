from abc import ABC, abstractmethod


class SpangramPlacementStrategy(ABC):
    rows: int = None
    cols: int = None

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

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

    @abstractmethod
    def distance_form_end(self, row, col):
        raise NotImplementedError

    @abstractmethod
    def starting_positions(self) -> list[tuple[int, int]]:
        raise NotImplementedError


class LeftToRightStrategy(SpangramPlacementStrategy):
    direction = (0, 1)
    positive_direction_transforms = [(0, 1), (-1, 1), (1, 1)]
    negative_direction_transforms = ((0, -1), (-1, -1), (1, -1))
    neutral_direction_transforms = [(1, 0), (-1, 0)]

    def distance_form_end(self, row, col):
        return self.cols - col - 1

    def starting_positions(self) -> list[tuple[int, int]]:
        return [(row, 0) for row in range(self.rows)]


class RightToLeftStrategy(SpangramPlacementStrategy):
    direction = (0, -1)
    positive_direction_transforms = [(0, -1), (-1, -1), (1, -1)]
    negative_direction_transforms = ((0, 1), (-1, 1), (1, 1))
    neutral_direction_transforms = [(1, 0), (-1, 0)]

    def distance_form_end(self, row, col):
        return col

    def starting_positions(self) -> list[tuple[int, int]]:
        return [(row, self.cols - 1) for row in range(self.rows)]


class TopToBottomStrategy(SpangramPlacementStrategy):
    direction = (1, 0)
    positive_direction_transforms = [(1, 1), (1, 0), (1, -1)]
    negative_direction_transforms = ((-1, 1), (-1, 0), (-1, -1))
    neutral_direction_transforms = [(0, 1), (0, -1)]

    def distance_form_end(self, row, col):
        return self.rows - (row + 1)

    def starting_positions(self):
        return [(0, col) for col in range(self.cols)]


class BottomToTopStrategy(SpangramPlacementStrategy):
    direction = (-1, 0)
    positive_direction_transforms = [(1, 1), (1, 0), (1, -1)]
    negative_direction_transforms = ((-1, 1), (-1, 0), (-1, -1))
    neutral_direction_transforms = [(0, 1), (0, -1)]

    def distance_form_end(self, row, col):
        return row

    def starting_positions(self):
        return [(self.rows - 1, col) for col in range(self.cols)]