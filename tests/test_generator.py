from unittest import TestCase

from generator.board_generator import BoardGenerator


class TestBoardGenerator(TestCase):
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


class TestBoardGenerator(TestCase):
    def test_generate_region_length_combinations(self):
        words = ['apple', 'door', 'house']
        print(BoardGenerator.generate_region_length_combinations(words))
