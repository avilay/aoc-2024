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


def _apply(all_ops: Sequence[Op], all_args: list[int]) -> int:
    # exit condition
    if not all_ops and len(all_args) == 1:
        return all_args[0]

    # Now just some simple recursive process
    op, ops = all_ops[0], all_ops[1:]
    arg, args = all_args[0], all_args[1:]
    return op(
        _apply(ops, args),
        arg
    )


def apply(all_ops: Sequence[Op], all_args: list[int]) -> int:
    """
    all_args = [x, y, z]
    all_ops = [A, B]
    This function gives the result of x A y B z where A and B are two different ops and x, y, and z are args.
    It'll first need to evaluate A(x, y) then pass this result to B which will evaluate B( A(x, y), z). All the ops in
    the given problem happen to be commutative so the order of args does not matter, but I keep the original order this
    function will work for even non-commutative ops.
    For this to work I'll need to reverse the order of both ops and args and then recursively apply them.
    """
    all_ops = list(reversed(all_ops))
    all_args = list(reversed(all_args))
    return _apply(all_ops, all_args)


def is_valid(possible_ops: Sequence[Op], eqn: Eqn) -> bool:
    # The number of ops needed is 1 less than the number of args
    len_all_ops = len(eqn[1]) - 1

    # For each empty position between two args, I can choose one of the ops
    # There are M^N possible candidates where M is the number of possible ops
    # and N are the number of ops needed.
    candidate_all_ops = list(product(possible_ops, repeat=len_all_ops))
    
    all_args = eqn[1]
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
    solve1()
    solve2()


if __name__ == '__main__':
    main()
