class CollisionException(Exception):
    """Raised when a collision is detected"""
    pass


class InvalidSpangramException(Exception):
    """Raised when a spangram is invalid"""
    pass


class CannotFindWordException(Exception):
    """Raised when a word cannot be found"""
    pass


class InvalidTotalWordLengthException(Exception):
    """Raised when the sum of all word lengths does not equal the total grid size"""
    pass


class StrandsValidator:
    marked_grid = set()
    word_paths = {}
    sorted_word_paths = {}
    df = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    collision_found = False

    def __init__(self, grid, spangram, correct_words):
        self.grid = grid
        self.spangram = spangram
        self.correct_words = correct_words
        self.rows = len(grid)
        self.cols = len(grid[0])

    def find_word(self, word: str):
        word_found = False
        for row in range(self.rows):
            for col in range(self.cols):
                if word[0] == self.grid[row][col]:
                    if self.dfs(row, col, word, []):
                        word_found = True
        if word_found:
            for coords in self.word_paths[word]:
                self.marked_grid.add(coords)
                return True
        raise CannotFindWordException

    def dfs(self, row, col, target_word, path, builder=""):
        if target_word == "":
            if builder in self.sorted_word_paths:
                path.sort()
                if path not in self.sorted_word_paths[builder]:
                    raise CollisionException(path)
            self.word_paths[builder] = path
            path.sort()
            self.sorted_word_paths[builder] = path
            return True

        if (row, col) in self.marked_grid:
            return False
        if (not ((0 <= row < self.rows) and (0 <= col < self.cols)) or
                (row, col) in path or
                self.grid[row][col] != target_word[0]):
            return False

        result = False
        for drow, dcol in self.df:
            result = result or self.dfs(row + drow, col + dcol, target_word[1:], path + [(row, col)],
                                        builder + self.grid[row][col])
        return result

    def validate_total_word_length(self):
        total_length = len(''.join(self.correct_words)) + len(self.spangram)
        grid_length = self.rows * self.cols
        if not total_length == grid_length:
            raise InvalidTotalWordLengthException

    def validate_puzzle(self):
        self.validate_total_word_length()
        self.validate_sangram()

        for word in self.correct_words:
            self.find_word(word)

    def validate_sangram(self):

        if not self.find_word(self.spangram):
            raise InvalidSpangramException("Spangram word was not found")
        if not self.word_touches_different_edges(self.spangram):
            raise InvalidSpangramException("Spangram word does not touch different edges")
        return True

    def word_touches_different_edges(self, word):
        grid_edges = [(i, 0) for i in range(self.rows)] + \
                     [(i, self.cols - 1) for i in range(self.rows)] + \
                     [(0, j) for j in range(self.cols)] + \
                     [(self.rows - 1, j) for j in range(self.cols)]

        edge_touched = set()
        for coord in [self.word_paths[word][0], self.word_paths[word][-1]]:
            if coord in grid_edges:
                edge_touched.add(coord)
        return len(edge_touched) == 2


if __name__ == "__main__":
    grid = [["t", "g", "r", "a", "l", "p"],
            ["a", "e", "e", "e", "k", "h"],
            ["b", "a", "m", "m", "l", "a"],
            ["d", "g", "a", "e", "k", "a"],
            ["e", "l", "a", "t", "p", "p"],
            ["s", "t", "e", "t", "a", "l"],
            ["i", "g", "r", "n", "o", "i"],
            ["a", "m", "s", "e", "p", "s"]]

    spangram = 'greekletters'
    correct_words = ["beta", "sigma", "gamma", "delta", "alpha", "kappa", "epsilon"]

    puzzle_validator = StrandsValidator(grid=grid, spangram=spangram, correct_words=correct_words)
    try:
        puzzle_validator.validate_puzzle()
    except Exception as e:
        raise e
