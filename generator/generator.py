from spangram_placement_strategies import SpangramPlacementStrategy


class BoardGenerator:
    board: list[list[str | None]] = None
    rows: int = None
    cols: int = None
    words: list[str] = None
    spangram: str = None
    spangram_placement_strategy: SpangramPlacementStrategy = None

    def __init__(self, rows: int, cols: int, words: list[str], spangram: str,
                 spangram_placement_strategy_class):
        self.board = [[None] * cols for _ in range(rows)]
        self.rows = rows
        self.cols = cols
        self.words = words
        self.spangram = spangram
        self.spangram_placement_strategy = spangram_placement_strategy_class(rows=rows, cols=cols)

    def generate_board(self, spangram: str, words: list) -> list[list[str]]:
        """
        :param spangram:
        :param words:

        1. Spangram will split the board so on both ends the board must have a sufficient amount of tiles to cover the rest of the words.
        """

    def place_spangram(self, spangram: str):
        for ch in spangram:
            row, col = self.spangram_placement_strategy.get_next_spangram_letter_position(index, spangram, board_state)

    def get_split_board_counts(self) -> list[int]:
        return [1, 2]