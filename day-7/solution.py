from collections.abc import Callable, Sequence
from functools import partial
from itertools import product
from operator import add, mul

test_input = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""
type Op = Callable[[int, int], int]
type Eqn = tuple[int, list[int]]


def cat(v1: int, v2: int) -> int:
    return int(str(v1) + str(v2))


def parse(lines: list[str]) -> list[Eqn]:
    eqns: list[Eqn] = []
    for line in lines:
        line = line.strip()
        if line:
            output, input_ = line.split(":")
            ans = int(output)
            nums = [int(fld) for fld in input_.split()]
            eqns.append((ans, nums))
    return eqns


def apply(all_ops: Sequence[Op], all_args: list[int]) -> int:
    if not all_ops and len(all_args) == 1:
        return all_args[0]

    op, ops = all_ops[0], all_ops[1:]
    arg2, args = all_args[0], all_args[1:]
    arg1 = apply(ops, args)
    return op(arg1, arg2)


def is_valid(possible_ops: Sequence[Op], eqn: Eqn) -> bool:
    len_all_ops = len(eqn[1]) - 1
    candidate_all_ops: list[Sequence[Op]] = [list(reversed(comb)) for comb in product(*[possible_ops] * len_all_ops)]
    all_args = list(reversed(eqn[1]))
    expected_answer = eqn[0]
    return any(
        apply(all_ops, all_args) == expected_answer
        for all_ops in candidate_all_ops
    )


def solve1():
    # lines = test_input.splitlines()
    lines = open("input.txt", "r").readlines()
    eqns = parse(lines)
    is_eqn_valid = partial(is_valid, (add, mul))
    valid_eqns = filter(is_eqn_valid, eqns)
    valid_eqns = list(valid_eqns)
    tot = sum(valid_eqn[0] for valid_eqn in valid_eqns)
    print(f"Answer to part 1: {tot}")


def solve2():
    # lines = test_input.splitlines()
    lines = open("input.txt", "r").readlines()
    eqns = parse(lines)
    is_eqn_valid = partial(is_valid, (add, mul, cat))
    valid_eqns = filter(is_eqn_valid, eqns)
    valid_eqns = list(valid_eqns)
    tot = sum(valid_eqn[0] for valid_eqn in valid_eqns)
    print(f"Answer to part 2: {tot}")


def main():
    solve2()


if __name__ == '__main__':
    main()
