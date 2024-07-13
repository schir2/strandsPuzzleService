import unittest
from unittest.mock import patch

from generator.spangram_placement_strategies import LeftToRightStrategy, RightToLeftStrategy, UpToDownStrategy, \
    DownToUpStrategy



class TestSpangramPlacementStrategies(unittest.TestCase):

    def setUp(self):
        self.rows = 5
        self.cols = 5
        self.spangram = 'SPANGRAM'
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def test_left_to_right_strategy(self):
        strategy = LeftToRightStrategy(self.rows, self.cols, self.spangram, self.board)
        self.assertEqual(strategy.direction, (0, 1))

        self.assertEqual(strategy.distance_form_end(2, 2), 3)

        row, col = strategy.select_starting_position()
        self.assertGreaterEqual(row, 0)
        self.assertLess(row, self.rows)
        self.assertEqual(col, 0)

    def test_right_to_left_strategy(self):
        strategy = RightToLeftStrategy(self.rows, self.cols, self.spangram, self.board)
        self.assertEqual(strategy.direction, (0, -1))

        self.assertEqual(strategy.distance_form_end(2, 2), 2)

        row, col = strategy.select_starting_position()
        self.assertGreaterEqual(row, 0)
        self.assertLess(row, self.rows)
        self.assertEqual(col, self.cols - 1)

    def test_up_to_down_strategy(self):
        strategy = UpToDownStrategy(self.rows, self.cols, self.spangram, self.board)
        self.assertEqual(strategy.direction, (1, 0))

        self.assertEqual(strategy.distance_form_end(2, 2), 3)

        row, col = strategy.select_starting_position()
        self.assertEqual(row, 0)
        self.assertGreaterEqual(col, 0)
        self.assertLess(col, self.cols)

    def test_down_to_up_strategy(self):
        strategy = DownToUpStrategy(self.rows, self.cols, self.spangram, self.board)
        self.assertEqual(strategy.direction, (-1, 0))

        self.assertEqual(strategy.distance_form_end(2, 2), 2)

        row, col = strategy.select_starting_position()
        self.assertEqual(row, self.rows - 1)
        self.assertGreaterEqual(col, 0)
        self.assertLess(col, self.cols)


if __name__ == '__main__':
    unittest.main()
