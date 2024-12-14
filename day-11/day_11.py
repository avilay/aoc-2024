from functools import lru_cache


def update(stone: int) -> tuple[int | None, int | None]:
    if stone == 0:
        return 1, None

    string_stone = str(stone)
    if len(string_stone) % 2 == 0:
        mid = len(string_stone) // 2
        left = int(string_stone[:mid])
        right = int(string_stone[mid:])
        return left, right

    return stone * 2024, None


@lru_cache
def blink(n_blinks: int, stone: int | None) -> int:
    if stone is None: return 0

    new_stones = update(stone)
    if n_blinks == 1:
        return 1 if new_stones[1] is None else 2

    num_stones = blink(n_blinks-1, new_stones[0])
    if new_stones[1] is not None:
        num_stones += blink(n_blinks-1, new_stones[1])

    return num_stones


def main():
    # test_input = [125, 17]
    input_ = [4022724, 951333, 0, 21633, 5857, 97, 702, 6]
    n_blinks = 75
    num_stones = sum(blink(n_blinks, stone) for stone in input_)
    print(num_stones)


if __name__ == "__main__":
    main()
