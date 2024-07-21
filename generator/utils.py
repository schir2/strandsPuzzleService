from generator.constants import DIAGONAL_CHANGES_SET, ORTHOGONAL_CHANGES


def get_complimentary_vertices(vertex) -> tuple | None:
    if len(vertex) < 2:
        return
    df = (vertex[0][0] - vertex[1][0], vertex[0][1] - vertex[1][1])
    if df not in DIAGONAL_CHANGES_SET:
        return
    complimentary_vertex = ((vertex[0][0] - df[0], vertex[0][1] + 0), (vertex[0][0] + 0, vertex[0][1] - df[1]))
    complimentary_vertices = (complimentary_vertex, (complimentary_vertex[1], complimentary_vertex[0]))
    return complimentary_vertices


def crossed_diagonally(vertex: list[tuple[int, int]], vertices: set) -> bool:
    complimentary_vertices = get_complimentary_vertices(vertex)
    if not complimentary_vertices:
        return False
    for complimentary_vertex in complimentary_vertices:
        if complimentary_vertex in vertices:
            return True
    return False


def create_empty_board(rows: int, cols: int) -> list[list[str | None]]:
    board = [[None for _ in range(cols)] for _ in range(rows)]
    return board


def convert_board_to_regions(board) -> list:
    regions = []
    for row in range(len(board)):
        for col, cell in enumerate(board[row]):
            if cell is None:
                regions.append(set())
                _create_region(row=row, col=col, board=board, region=regions[-1])
    return regions


def _create_region(row: int, col: int, board, region):
    if not (0 <= row < len(board) and 0 <= col < len(board[0])) or board[row][col] is not None:
        return
    board[row][col] = ''
    region.add((row, col))
    for dr, dc in ORTHOGONAL_CHANGES:
        _create_region(row=row + dr, col=col + dc, board=board, region=region)


def disjoint_region_generator(base_region: set) -> list:
    regions = []
    traversed = set()
    for cell in base_region:
        if cell not in traversed:
            regions.append(set())
            _traverse_region(cell=cell, base_region=base_region, regions=regions, traversed=traversed)
    return regions


def _traverse_region(cell, base_region, regions, traversed):
    if not (cell in base_region) or (cell in traversed):
        return
    traversed.add(cell)
    regions[-1].add(cell)
    for dr, dc in ORTHOGONAL_CHANGES:
        _traverse_region((cell[0] + dr, cell[1] + dc), base_region, regions, traversed, )
