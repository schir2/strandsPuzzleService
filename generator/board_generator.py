from collections import defaultdict
from itertools import combinations

from generator.utils import convert_board_to_regions


class InvalidRegionLengthException(Exception):
    pass


class BoardGenerator:
    board: list[list[str | None]] = None
    rows: int = None
    cols: int = None
    words: list[str] = None
    spangram: str = None
    valid_boards: list = []

    def __init__(self, rows: int, cols: int, words: list[str], spangram: str,
                 spangram_placement_strategy_class):
        self.board = [[None] * cols for _ in range(rows)]
        self.rows = rows
        self.cols = cols
        self.words = words
        self.spangram = spangram
        self.spangram_placement_strategy = spangram_placement_strategy_class(rows=rows, cols=cols)
        self.region_length_combinations = self.generate_region_length_combinations(words)

    def fill_region_with_words(self, words, region):
        for i, word in enumerate(words):
            regions = self.fill_word_into_region(word, region)

    def fill_word_into_region(self, word, region):
        ...

    @staticmethod
    def generate_region_length_combinations(words):
        words = set(words)
        total_length = sum(len(word) for word in words)
        combinations_map = defaultdict(set)

        for num_words in range(1, len(words)):
            for combo in combinations(words, num_words):
                combo_length = sum(len(word) for word in combo)
                complementary_length = total_length - combo_length
                combo_tuple = tuple(sorted(combo))
                combo_complement_tuple = tuple(sorted(words - set(combo)))
                combinations_map[(combo_length, complementary_length)].add((combo_tuple, combo_complement_tuple))
                combinations_map[(complementary_length, combo_length)].add((combo_complement_tuple, combo_tuple))
        return combinations_map

    def validate_spangram_board(self, board):
        unfilled_regions = convert_board_to_regions(board)
        if len(unfilled_regions) != 2:
            raise InvalidRegionLengthException

        return unfilled_regions
