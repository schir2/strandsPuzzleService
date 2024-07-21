from unittest import TestCase

from generator.board_generator import BoardGenerator


class TestBoardGenerator(TestCase):

    def setUp(self):
        self.spangram_board_with_two_regions = [
            ['s', None, None, None, None, None, ],
            [None, 'p', None, None, None, None, ],
            [None, None, 'a', None, None, None, ],
            [None, None, None, 'n', None, None, ],
            [None, None, None, None, 'g', None, ],
            [None, None, None, None, 'r', None, ],
            [None, None, None, None, 'a', None, ],
            [None, None, None, None, None, 'm', ],
        ]

        self.converted_board_to_regions = [
            {(0, 1), (2, 4), (1, 2), (0, 4), (3, 4), (5, 5), (1, 5), (6, 5), (0, 3), (1, 4), (2, 3), (0, 2), (4, 5),
             (0, 5), (2, 5), (1, 3), (3, 5)},
            {(4, 0), (4, 3), (3, 1), (5, 1), (1, 0), (7, 4), (6, 2), (7, 1), (4, 2), (3, 0), (5, 0), (5, 3), (2, 1),
             (6, 1), (7, 0), (7, 3), (3, 2), (4, 1), (5, 2), (2, 0), (7, 2), (6, 0), (6, 3)}]

        self.regions_with_two_regions = {
            (0, 1), (2, 4), (1, 2), (0, 4), (3, 4), (5, 5), (1, 5), (6, 5), (0, 3), (1, 4), (2, 3), (0, 2), (4, 5),
            (0, 5), (2, 5), (1, 3), (3, 5), (4, 0), (4, 3), (3, 1), (5, 1), (1, 0), (7, 4), (6, 2), (7, 1), (4, 2),
            (3, 0), (5, 0), (5, 3), (2, 1), (6, 1), (7, 0), (7, 3), (3, 2), (4, 1), (5, 2), (2, 0), (7, 2), (6, 0),
            (6, 3)
        }


    def test_crossed_diagonally_exists(self):
        vertices = {((0, 1), (1, 2)), }
        result = BoardGenerator.crossed_diagonally([(1, 1), (0, 2)], vertices)
        self.assertTrue(result)


    def test_crossed_diagonally_flipped_exists(self):
        vertices = {((1, 2), (0, 1))}
        result = BoardGenerator.crossed_diagonally([(1, 1), (0, 2)], vertices)
        self.assertTrue(result)


    def test_crossed_diagonally_does_not_exist(self):
        vertices = set()
        result = BoardGenerator.crossed_diagonally([(1, 1), (0, 2)], vertices)
        self.assertFalse(result)


    def test_get_complimentary_vertices_diagonal(self):
        complimentary_vertices = BoardGenerator.get_complimentary_vertices(((1, 1), (0, 2)))
        vertices = {((0, 1), (1, 2)), ((1, 2), (0, 1))}
        for complimentary_vertex in complimentary_vertices:
            self.assertIn(complimentary_vertex, vertices)


    def test_get_complimentary_vertices_vertical(self):
        complimentary_vertices = BoardGenerator.get_complimentary_vertices(((1, 1), (2, 1)))
        self.assertIsNone(complimentary_vertices)


    def test_get_complimentary_vertices_horizontal(self):
        complimentary_vertices = BoardGenerator.get_complimentary_vertices(((1, 1), (1, 2)))
        self.assertIsNone(complimentary_vertices)


    def test_generate_region_length_combinations(self):
        words = ['apple', 'door', 'house']
        print(BoardGenerator.generate_region_length_combinations(words))


    def test_disjoint_region_generator(self):
        disjoint_regions = BoardGenerator.disjoint_region_generator(self.regions_with_two_regions)
        self.assertTrue(disjoint_regions, self.spangram_board_with_two_regions)


    def test_convert_board_to_regions(self):
        converted_board = BoardGenerator.convert_board_to_regions(self.spangram_board_with_two_regions)
        self.assertEqual(converted_board, self.converted_board_to_regions)
