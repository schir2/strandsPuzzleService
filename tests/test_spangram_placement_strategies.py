import unittest

from generator.spangram_placement_strategies import LeftToRightStrategy, RightToLeftStrategy, TopToBottomStrategy, \
    BottomToTopStrategy


class TestSpangramPlacementStrategies(unittest.TestCase):

    def setUp(self):
        self.rows = 5
        self.cols = 5
        self.spangram = 'SPANGRAM'
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def test_left_to_right_strategy(self):
        strategy = LeftToRightStrategy(self.rows, self.cols, self.spangram)
        self.assertEqual(strategy.direction, (0, 1))

        self.assertEqual(strategy.distance_form_end(2, 2), 3)

        starting_positions = strategy.starting_positions()
        self.assertEqual(starting_positions, [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)])

    def test_right_to_left_strategy(self):
        strategy = RightToLeftStrategy(self.rows, self.cols, self.spangram)
        self.assertEqual(strategy.direction, (0, -1))

        self.assertEqual(strategy.distance_form_end(2, 2), 2)

        starting_positions = strategy.starting_positions()
        self.assertEqual(starting_positions, [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)])

    def test_up_to_down_strategy(self):
        strategy = TopToBottomStrategy(self.rows, self.cols, self.spangram)
        self.assertEqual(strategy.direction, (1, 0))

        self.assertEqual(strategy.distance_form_end(2, 2), 3)

        starting_positions = strategy.starting_positions()
        self.assertEqual(starting_positions, [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)])

    def test_down_to_up_strategy(self):
        strategy = BottomToTopStrategy(self.rows, self.cols, self.spangram)
        self.assertEqual(strategy.direction, (-1, 0))

        self.assertEqual(strategy.distance_form_end(2, 2), 2)

        starting_positions = strategy.starting_positions()
        self.assertEqual(starting_positions, [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)])