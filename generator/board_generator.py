import copy
from collections import defaultdict
from itertools import combinations

from generator.spangram_placement_strategies import SpangramPlacementStrategy, RightToLeftStrategy


class InvalidRegionLengthException(Exception):
    pass


class BoardGenerator:
    board: list[list[str | None]] = None
    rows: int = None
    cols: int = None
    words: list[str] = None
    spangram: str = None
    valid_boards: list = []
    orthogonal_changes = ((0, 1), (0, -1), (1, 0), (-1, 0))
    diagonal_changes = {(1, 1), (1, -1), (-1, 1), (-1, -1)}
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

    @staticmethod
    def generate_region_length_combinations(words):
        # TODO This needs to generate the actual combinations of words
        words = set(words)
        total_length = sum(len(word) for word in words)
        combinations_map = defaultdict(set)

        for num_words in range(1, len(words)):
            for combo in combinations(words, num_words):
                combo_length = sum(len(word) for word in combo)
                complementary_length = total_length - combo_length
                if combo_length > 0 and complementary_length > 0:
                    combo_tuple = tuple(sorted(combo))
                    combo_complement_tuple = tuple(sorted(words - set(combo)))
                    combinations_map[(combo_length, complementary_length)].add((combo_tuple, combo_complement_tuple))
                    combinations_map[(complementary_length, combo_length)].add((combo_complement_tuple, combo_tuple))
        return combinations_map

    def generate_spangram_boards(self):
        starting_positions = self.spangram_placement_strategy.starting_positions()
        for starting_row, starting_col in starting_positions:
            self.generate_spangram_board(
                row=starting_row,
                col=starting_col,
                i=0,
                path=[(starting_row, starting_col)],
                vertices=set(),
                board=self.create_empty_board(self.rows, self.cols)
            )
        return self.valid_boards

    @staticmethod
    def create_empty_board(rows: int, cols: int) -> list[list[str | None]]:
        board = [[None for _ in range(cols)] for _ in range(rows)]
        return board

    @classmethod
    def crossed_diagonally(cls, vertex: list[tuple[int, int]], vertices: set) -> bool:
        complimentary_vertices = cls.get_complimentary_vertices(vertex)
        if not complimentary_vertices:
            return False
        for complimentary_vertex in complimentary_vertices:
            if complimentary_vertex in vertices:
                return True
        return False

    @classmethod
    def get_complimentary_vertices(cls, vertex) -> tuple | None:
        if len(vertex) < 2:
            return
        df = (vertex[0][0] - vertex[1][0], vertex[0][1] - vertex[1][1])
        if df not in cls.diagonal_changes:
            return
        complimentary_vertex = ((vertex[0][0] - df[0], vertex[0][1] + 0), (vertex[0][0] + 0, vertex[0][1] - df[1]))
        complimentary_vertices = (complimentary_vertex, (complimentary_vertex[1], complimentary_vertex[0]))
        return complimentary_vertices

    def generate_spangram_board(self, row: int, col: int, i: int, path: list, vertices: set, board: list) -> bool:
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False
        if board[row][col]:
            return False

        distance_from_end = self.spangram_placement_strategy.distance_form_end(*path[-1])
        letters_to_go = len(self.spangram) - i - 1

        if distance_from_end > letters_to_go:
            return False

        if len(path) > 1:
            vertices.add((path[-2], path[-1]))

        if self.crossed_diagonally(path[-2:], vertices):
            return False

        board[row][col] = self.spangram[i]

        if letters_to_go == 0 and distance_from_end == 0:
            board_tuple = copy.deepcopy(board)
            self.valid_boards.append(board_tuple)
            board[row][col] = None
            return True

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
        for dr, dc in cls.orthogonal_changes:
            cls._create_region(row=row + dr, col=col + dc, board=board, regions=regions)

    def validate_spangram_board(self, board):
        try:
            unfilled_regions = self.get_unfilled_regions(board)
        except InvalidRegionLengthException:
            return False

        return unfilled_regions


if __name__ == '__main__':
    results = []
    for strategy_class in (RightToLeftStrategy,):
        generator = BoardGenerator(2, 2, ['flap', 'test', 'brown'], 'test', strategy_class)
        boards = generator.generate_spangram_boards()
        results.append(boards)
