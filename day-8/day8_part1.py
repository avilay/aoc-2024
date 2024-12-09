from multiprocessing import Pool

test_input = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

from collections import defaultdict
from functools import partial


class Vec:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __add__(self, other):
        return Vec(self.row + other.row, self.col + other.col)

    def __sub__(self, other):
        return Vec(self.row - other.row, self.col - other.col)

    def to_tuple(self):
        return self.row, self.col


def build_grid(lines):
    sparse_grid = defaultdict(list)
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == ".":
                continue
            else:
                sparse_grid[char].append(Vec(i, j))
    return sparse_grid


def within_bounds(max_rows, max_cols, u):
    return 0 <= u.row < max_rows and 0 <= u.col < max_cols


def symbol_antinodes(max_rows, max_cols, vecs):
    is_within_bounds = partial(within_bounds, max_rows, max_cols)
    anodes = set()
    for i, v1 in enumerate(vecs):
        for v2 in vecs[i + 1:]:
            d = v1 - v2
            a1 = d + v1
            a2 = v2 - d
            if is_within_bounds(a1):
                anodes.add(a1.to_tuple())
            if is_within_bounds(a2):
                anodes.add(a2.to_tuple())
    return anodes


def grid_antinodes(sparse_grid, get_symbol_antinodes):
    antinodes = set()
    with Pool() as pool:
        symb_anodes = pool.map(get_symbol_antinodes, sparse_grid.values())

    for anodes in symb_anodes:
        antinodes.update(anodes)
    return antinodes


def solve1():
    # lines = test_input.splitlines()[1:]
    lines = open("input.txt").read().splitlines()
    max_rows = len(lines)
    max_cols = len(lines[0])
    sparse_grid = build_grid(lines)
    get_symbol_antinodes = partial(symbol_antinodes, max_rows, max_cols)
    antinodes = grid_antinodes(sparse_grid, get_symbol_antinodes)
    print(f"Answer to part one: {len(antinodes)}")


if __name__ == "__main__":
    solve1()
