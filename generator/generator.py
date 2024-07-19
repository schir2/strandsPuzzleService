import copy
from itertools import combinations

from spangram_placement_strategies import SpangramPlacementStrategy, RightToLeftStrategy


class InvalidRegionLengthException(Exception):
    pass


class BoardGenerator:
    board: list[list[str | None]] = None
    rows: int = None
    cols: int = None
    words: list[str] = None
    spangram: str = None
    valid_boards: list = []
    df = ((0, 1), (0, -1), (1, 0), (-1, 0))
    spangram_placement_strategy: SpangramPlacementStrategy = None

    def __init__(self, rows: int, cols: int, words: list[str], spangram: str,
                 spangram_placement_strategy_class):
        self.board = [[None] * cols for _ in range(rows)]
        self.rows = rows
        self.cols = cols
        self.words = words
        self.spangram = spangram
        self.spangram_placement_strategy = spangram_placement_strategy_class(rows=rows, cols=cols)
        self.region_length_combinations = self.generate_region_length_combinations(words)

    def generate_board(self, spangram: str, words: list) -> list[list[str]]:
        """
        :param spangram:
        :param words:

        1. Spangram will split the board so on both ends the board must have a sufficient amount of tiles to cover the rest of the words.
        """

    @staticmethod
    def generate_region_length_combinations(words):
        # TODO This needs to generate the actual combinations of words
        total_length = sum(len(word) for word in words)
        region_length_combinations = set()

        for num_words in range(1, len(words)):
            for combo in combinations(words, num_words):
                combo_length = sum(len(word) for word in combo)
                complementary_length = total_length - combo_length
                if combo_length > 0 and complementary_length > 0:
                    region_length_combinations.add((combo_length, complementary_length))
                    region_length_combinations.add((complementary_length, combo_length))

        return region_length_combinations

    def generate_spangram_boards(self):
        starting_positions = self.spangram_placement_strategy.starting_positions()
        for starting_row, starting_col in starting_positions:
            self.generate_spangram_board(starting_row, starting_col, 0, [(starting_row, starting_col)], set(),
                                         self.create_empty_board())
        return self.valid_boards

    def create_empty_board(self) -> list[list[str | None]]:
        board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        return board

    def crossed_diagonally(self, row: int, col: int) -> bool:
        return False

    def generate_spangram_board(self, row: int, col: int, i: int, path: list[tuple[int, int]],
                                vertices: set[tuple[tuple[int, int], tuple[int, int]]],
                                board: list[list[str]]) -> bool:
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False
        if board[row][col]:
            return False

        board[row][col] = self.spangram[i]
        distance_from_end = self.spangram_placement_strategy.distance_form_end(*path[-1])
        letters_to_go = len(self.spangram) - i - 1

        if distance_from_end > letters_to_go:
            board[row][col] = None
            return False
        if letters_to_go == 0 and distance_from_end == 0:
            board_tuple = copy.deepcopy(board)
            self.valid_boards.append(board_tuple)
            board[row][col] = None
            return True
        if self.crossed_diagonally(row=row, col=col):
            board[row][col] = None
            return False

        if len(path) > 1:
            vertices.add((path[-2], path[-1]))

        directions = []

        if letters_to_go - distance_from_end >= 2:
            for dr, dc in self.spangram_placement_strategy.negative_direction_transforms:
                directions.append((row + dr, col + dc))
        if letters_to_go - distance_from_end >= 1:
            for dr, dc in self.spangram_placement_strategy.neutral_direction_transforms:
                directions.append((row + dr, col + dc))
        for dr, dc in self.spangram_placement_strategy.positive_direction_transforms:
            directions.append((row + dr, col + dc))

        for next_row, next_col in directions:
            next_row_col_tuple = (next_row, next_col)
            self.generate_spangram_board(row=next_row, col=next_col, i=i + 1, path=path + [next_row_col_tuple],
                                         vertices=vertices | {next_row_col_tuple}, board=board)

        board[row][col] = None

    @classmethod
    def get_unfilled_regions(cls, board) -> list:
        regions = []
        for row in range(len(board)):
            for col, cell in enumerate(board[row]):
                if cell is None:
                    regions.append(set())
                    cls._create_region(row=row, col=col, board=board, regions=regions)
        if len(regions) != 2:
            raise InvalidRegionLengthException
        return regions

    @classmethod
    def _create_region(cls, row: int, col: int, board, regions):
        if not (0 <= row < len(board) and 0 <= col < len(board[0])) or board[row][col] is not None:
            return
        board[row][col] = ''
        regions[-1].add((row, col))
        for dr, dc in cls.df:
            cls._create_region(row=row + dr, col=col + dc, board=board, regions=regions)

    def validate_spangram_board(cls, board):
        try:
            unfilled_regions = cls.get_unfilled_regions(board)
        except InvalidRegionLengthException:
            return False

        return unfilled_regions


if __name__ == '__main__':
    results = []
    for strategy_class in (RightToLeftStrategy,):
        generator = BoardGenerator(4, 4, ['flap', 'test', 'brown'], 'test', strategy_class)
        boards = generator.generate_spangram_boards()
        for board in boards:
            for row in board:
                print(row)
            print(10 * '_')
            unfilled_regions = generator.validate_spangram_board(board)
            print(unfilled_regions)
            print(10 * '_')
