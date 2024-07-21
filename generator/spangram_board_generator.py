import random
from typing import List

from generator.spangram_placement_strategies import SpangramPlacementStrategy, RightToLeftStrategy, TopToBottomStrategy, \
    LeftToRightStrategy, BottomToTopStrategy
from generator.utils import create_empty_board, crossed_diagonally


class SpangramBoardGenerator:
    strategy_classes = [LeftToRightStrategy, RightToLeftStrategy, TopToBottomStrategy, BottomToTopStrategy]

    def __init__(self, rows: int, cols: int, spangram: str,
                 strategy_classes: List[SpangramPlacementStrategy] | SpangramPlacementStrategy | None = None):
        self.rows = rows
        self.cols = cols
        self.spangram = spangram
        if strategy_classes and not isinstance(strategy_classes, list):
            strategy_classes = [strategy_classes]
        self.strategy_classes = strategy_classes or self.strategy_classes
        self.spangram_placement_strategies = [strategy_class(rows, cols) for strategy_class in self.strategy_classes]

    def generate_random_spangram_board(self, ) -> list[list[str | None]] | None:

        for spangram_placement_strategy in self.spangram_placement_strategies:
            starting_positions = spangram_placement_strategy.starting_positions()
            random.shuffle(starting_positions)
            random.shuffle(starting_positions)
            for starting_row, starting_col in starting_positions:
                result = self._generate_random_spangram_board(
                    row=starting_row,
                    col=starting_col,
                    i=0,
                    path=[(starting_row, starting_col)],
                    vertices=set(),
                    board=create_empty_board(self.rows, self.cols),
                    end_reached=False,
                    spangram_placement_strategy=spangram_placement_strategy
                )
                if result:
                    return result

    def _generate_random_spangram_board(self, row: int, col: int, i: int, path: list, vertices: set,
                                        board: list, end_reached: bool,
                                        spangram_placement_strategy: SpangramPlacementStrategy) -> list[list[
        str | None]] | None:
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
        if board[row][col]:
            return

        distance_from_end = spangram_placement_strategy.distance_form_end(*path[-1])

        end_reached |= end_reached or (distance_from_end == 0)

        letters_to_go = len(self.spangram) - i - 1

        if distance_from_end > letters_to_go and not end_reached:
            return

        if len(path) > 1:
            vertices.add((path[-2], path[-1]))

        if crossed_diagonally(path[-2:], vertices):
            return

        board[row][col] = self.spangram[i]

        if letters_to_go == 0 and end_reached:
            return board

        directions = []

        if end_reached or letters_to_go - distance_from_end >= 2:
            for dr, dc in spangram_placement_strategy.negative_direction_transforms:
                directions.append((row + dr, col + dc))
        if end_reached or letters_to_go - distance_from_end >= 1:
            for dr, dc in spangram_placement_strategy.neutral_direction_transforms:
                directions.append((row + dr, col + dc))
        for dr, dc in spangram_placement_strategy.positive_direction_transforms:
            directions.append((row + dr, col + dc))

        random.shuffle(directions)

        for next_row, next_col in directions:
            next_row_col_tuple = (next_row, next_col)
            result = self._generate_random_spangram_board(
                row=next_row,
                col=next_col,
                i=i + 1,
                path=path + [next_row_col_tuple],
                vertices=vertices | {next_row_col_tuple},
                board=board,
                end_reached=end_reached,
                spangram_placement_strategy=spangram_placement_strategy
            )
            if result:
                return result

        board[row][col] = None


if __name__ == '__main__':
    generator = SpangramBoardGenerator(5, 5, spangram='verylongword')
    board = generator.generate_random_spangram_board()
    if board:
        for row in board:
            print(row)
        print()
