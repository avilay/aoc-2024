from enum import Enum

import numpy as np

test_input = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""


class Heading(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    def __str__(self):
        if self.value == 1:
            return "^"
        elif self.value == 2:
            return "v"
        elif self.value == 3:
            return "<"
        elif self.value == 4:
            return ">"


def init_grid(lines):
    arrs = []
    for line in lines:
        line = line.strip()
        if line:
            arrs.append(np.array(list(line)))
    grid = np.array(arrs)
    return grid


def get_starting_position(grid):
    headings = [Heading.UP, Heading.DOWN, Heading.LEFT, Heading.RIGHT]
    icons = [str(heading) for heading in list(Heading)]
    for icon, heading in zip(icons, headings):
        start_pos = np.argwhere(grid == icon)
        if start_pos.size != 0:
            return tuple(start_pos.flatten().tolist()), heading


def get_next_position(grid, curr_pos, curr_heading):
    num_rows, num_cols = grid.shape
    curr_row, curr_col = curr_pos
    open_icons = [".", "X"]
    if curr_heading == Heading.UP:
        # 1 step up
        row = curr_row - 1
        # noinspection DuplicatedCode
        col = curr_col
        if row < 0 or row >= num_rows:
            # exit the room
            return None, None
        if grid[row, col] in open_icons:
            # take a step forward
            return (row, col), curr_heading
        if grid[row, col] == "#":
            # turn right in place
            return (curr_row, curr_col), Heading.RIGHT

    if curr_heading == Heading.DOWN:
        # one step down
        row = curr_row + 1
        # noinspection DuplicatedCode
        col = curr_col
        if row < 0 or row >= num_rows:
            # exit the room
            return None, None
        if grid[row, col] in open_icons:
            # take a step down (world coords)
            return (row, col), curr_heading
        if grid[row, col] == "#":
            # turn left (world coords) in place
            return (curr_row, curr_col), Heading.LEFT

    if curr_heading == Heading.LEFT:
        # one step left
        row = curr_row
        col = curr_col - 1
        # noinspection DuplicatedCode
        if col < 0 or col >= num_cols:
            # exit the room
            return None, None
        if grid[row, col] in open_icons:
            # step one step left
            return (row, col), curr_heading
        if grid[row, col] == "#":
            # turn up in place
            return (curr_row, curr_col), Heading.UP

    if curr_heading == Heading.RIGHT:
        # one step right
        row = curr_row
        col = curr_col + 1
        # noinspection DuplicatedCode
        if col < 0 or col >= num_cols:
            # exit the room
            return None, None
        if grid[row, col] in open_icons:
            # take one step to the right
            return (row, col), curr_heading
        if grid[row, col] == "#":
            # turn down in place
            return (curr_row, curr_col), Heading.DOWN

    raise RuntimeError(f"This should not happen! grid[{row},{col}] = {grid[row, col]}")


def find_obstructions(orig_grid):
    grid = orig_grid.copy()
    start_pos, start_heading = get_starting_position(grid)
    path = guard_path(grid)
    obstructions = set()

    for idx in range(len(path) - 1, 0, -1):
        step, _ = path[idx]
        if step in obstructions or step == start_pos:
            continue
        grid = orig_grid.copy()
        grid[start_pos] = "X"
        grid[step] = "#"
        new_path = set()
        pos, heading = start_pos, start_heading
        while pos is not None:
            if (pos, heading) in new_path:
                obstructions.add(step)
                break
            grid[pos] = "X"
            new_path.add((pos, heading))
            pos, heading = get_next_position(grid, pos, heading)

    return obstructions


def guard_path(grid):
    path = []
    pos, heading = get_starting_position(grid)
    while pos is not None:
        grid[pos] = "X"
        path.append((pos, heading))
        pos, heading = get_next_position(grid, pos, heading)
    return path


def part2():
    with open("input.txt") as f:
        lines = f.readlines()
    # lines = test_input.splitlines()
    grid = init_grid(lines)
    obstructions = find_obstructions(grid)
    count = len(obstructions)
    print(f"Part 2: {count}")


def part1():
    with open("input.txt") as f:
        lines = f.readlines()
    # lines = test_input.splitlines()
    grid = init_grid(lines)
    guard_path(grid)
    count = len(np.argwhere(grid == "X"))
    print(f"Part 1: {count}")  # Part 1: 4647


def main():
    # part1()
    part2()


if __name__ == "__main__":
    main()
