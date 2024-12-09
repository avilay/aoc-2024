from functools import partial

import day8_part1 as p1


def symbol_antinodes(max_rows, max_cols, vecs):
    is_within_bounds = partial(p1.within_bounds, max_rows, max_cols)
    anodes = set()
    for i, v1 in enumerate(vecs):
        anodes.add(v1.to_tuple())
        for v2 in vecs[i + 1:]:
            anodes.add(v2.to_tuple())
            d = v1 - v2

            # Get all nodes above v1
            a = v1 - d
            while is_within_bounds(a):
                anodes.add(a.to_tuple())
                a = a - d

            # Get all nodes below v1
            b = v1 + d
            while is_within_bounds(b):
                anodes.add(b.to_tuple())
                b = b + d

    return anodes


def solve2():
    # lines = p1.test_input.splitlines()[1:]
    lines = open("input.txt").read().splitlines()
    max_rows = len(lines)
    max_cols = len(lines[0])
    sparse_grid = p1.build_grid(lines)
    get_symbol_antinodes = partial(symbol_antinodes, max_rows, max_cols)
    antinodes = p1.grid_antinodes(sparse_grid, get_symbol_antinodes)
    print(f"Answer to part two: {len(antinodes)}")


if __name__ == "__main__":
    solve2()
