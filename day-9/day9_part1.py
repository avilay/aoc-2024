from copy import copy
from pathlib import Path

test_input_1 = "12345"
test_input_2 = "2333133121414131402"


def inflate(compressed):
    inflated = []
    file_id = 0
    for i, n in enumerate(compressed):
        if i % 2 == 0:
            inflated += [file_id] * int(n)
            file_id += 1
        else:
            inflated += [-1] * int(n)
    return inflated


def defragment(blocks):
    blocks = copy(blocks)
    i, j = 0, len(blocks) - 1
    while i < j:
        # Move forward until there is an empty space
        # Move backward until there is a file block
        if blocks[i] != -1:
            i += 1
            continue
        if blocks[j] == -1:
            j -= 1
            continue

        # Now there is an empty space in front and file block at the end
        blocks[i] = blocks[j]
        blocks[j] = -1
        i += 1
        j -= 1
    return blocks


def checksum(blocks):
    return sum(n * i for i, n in enumerate(blocks) if n != -1)


def solve1():
    # inflated = inflate(test_input_1)
    # inflated = inflate(test_input_2)
    input_ = Path("input.txt").read_text().splitlines()[0]
    inflated = inflate(input_)
    blocks = defragment(inflated)
    chksum = checksum(blocks)
    print(f"Anser to part 1: {chksum}")


if __name__ == "__main__":
    solve1()
