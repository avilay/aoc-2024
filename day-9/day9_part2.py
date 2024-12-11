from dataclasses import dataclass
from pathlib import Path

test_input = "2333133121414131402"


@dataclass
class Block:
    file_id: int | None
    idx: int
    size: int


def inflate(compressed: str) -> tuple[list[Block], list[Block]]:
    file_blocks = []
    empty_blocks = []
    file_id = 0
    idx = 0
    for i, size in enumerate(compressed):
        size = int(size)
        if i % 2 == 0:
            # this is a file block
            file_blocks.append(Block(file_id=file_id, idx=idx, size=size))
            file_id += 1
        else:
            # this is an empty block
            empty_blocks.append(Block(file_id=None, idx=idx, size=size))
        idx += size

    return file_blocks, empty_blocks


def refragment(file_blocks: list[Block], empty_blocks: list[Block]) -> None:
    for file_block in reversed(file_blocks):
        for empty_block in empty_blocks:
            if empty_block.idx > file_block.idx: break
            if empty_block.size >= file_block.size:
                # Move this file
                file_block.idx = empty_block.idx
                empty_block.idx += file_block.size
                empty_block.size -= file_block.size
                break  # no need to look for empty blocks for this file


def checksum(file_blocks: list[Block]) -> int:
    chksum = 0
    for file_block in file_blocks:
        chksum += file_block.file_id * sum(range(file_block.idx, file_block.idx + file_block.size))
    return chksum


def solve2():
    # input_ = test_input
    input_ = Path("input.txt").read_text().splitlines()[0]
    file_blocks, empty_blocks = inflate(input_)
    refragment(file_blocks, empty_blocks)
    chksum = checksum(file_blocks)
    print(f"Answer to part 2: {chksum}")


if __name__ == "__main__":
    solve2()
