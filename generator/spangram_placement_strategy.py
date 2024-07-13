import abc


class SpangramPlacementStrategy:
    rows: int = None
    cols: int = None
    spangram: str = None
    board: list[list[str | None]]

    def __init__(self, rows, cols, spangram, board):
        self.rows = rows
        self.cols = cols
        self.board = board
        self.spangram = spangram

    @property
    @abc.abstractmethod
    def direction(self) -> tuple:
        raise NotImplementedError

    def place_spangram_letter(self, index: int, spangram: str, board_state: list[list[str | None]]) -> str:
        raise NotImplementedError

    def place_spangram(self, string):
        ...

    @abc.abstractmethod
    def distance_form_end(self, row, col):
        raise NotImplementedError


class LeftToRightStrategy(SpangramPlacementStrategy):
    direction = (0, 1)

    def distance_form_end(self, row, col):
        return self.cols - col


class RightToLeftStrategy(SpangramPlacementStrategy):
    direction = (0, -1)

    def distance_form_end(self, row, col):
        return col


class UpToDownStrategy(SpangramPlacementStrategy):
    direction = (1, 0)

    def distance_form_end(self, row, col):
        return self.rows - row


class DownToUpStrategy(SpangramPlacementStrategy):
    direction = (-1, 0)

    def distance_form_end(self, row, col):
        return row