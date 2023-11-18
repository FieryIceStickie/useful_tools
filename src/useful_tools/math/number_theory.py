import math
from bisect import bisect
from functools import lru_cache
from operator import itemgetter
from typing import Iterator, Literal, overload


@overload
def generalized_pentagonal_nums(n: int, *, include_index: Literal[True] = False) -> Iterator[tuple[int, int]]:
    ...


@overload
def generalized_pentagonal_nums(n: int, *, include_index: Literal[False] = False) -> Iterator[int]:
    ...


def generalized_pentagonal_nums(n: int, *, include_index: bool = False) -> Iterator[int | tuple[int, int]]:
    """
    Generates the first n generalized pentagonal numbers, starting from 0
    Also returns the number
    https://en.wikipedia.org/wiki/Pentagonal_number
    :param n: num
    :param include_index: kwarg for including index in return type
    :return: (k, kth generalized pentagonal number) if include_index else kth generalized pentagonal number
    """
    k = 0
    for _ in range(n):
        yield (k, int(k * (3*k - 1) // 2)) if include_index else int(k * (3*k - 1) // 2)
        k = (k <= 0) - k


def count_non_strict_integer_partitions(num: int) -> int:
    """
    https://en.wikipedia.org/wiki/Partition_(number_theory)
    :return: number of partitions less than num
    """
    *penta_nums, = generalized_pentagonal_nums(num + 1, include_index=True)

    @lru_cache(maxsize=num)
    def p(n: int) -> int:
        if n == 0:
            return 1
        return sum(p(n - a) * (1 if k % 2 else -1) for k, a in penta_nums[1:bisect(penta_nums, n, key=itemgetter(1))])
    return p(num)


def egyptian_decomposition(p: int, q: int, /, *,
                           force: bool = False) -> list[int] | list[list[int]]:
    """
    Given a rational number 0 < p/q < 1, find a decomposition of p/q into a sum of distinct unit fractions
    Set force=True if result needs to be the same across versions
    Example:
    (3, 5) -> [2, 10]
    (7, 22) -> []
    :param p: Numerator
    :param q: Denominator
    :param force: If true, skips directly to greedy method
    :return: Sorted list of denominators of unit fractions
    """
    g = math.gcd(p, q)
    p //= g
    q //= g
    if p == 1:
        return [q]

    if not force:
        if not (q+1) % p:
            b = (q+1) // p
            return [b, b*q]

        # Interpolation search factors of q+1 that sum to p

        # Practical number A: 2/p = 1/A + (2A-p)/Ap

        # Check if q is practical

        # 2/q = 1/q + 1/2q + 1/3q + 1/6q factorization for q prime
    denoms = []
    while True:
        c = -(-q//p)  # Ceil div
        denoms.append(c)
        p, q = (-q) % p, q * c
        g = math.gcd(p, q)
        p //= g
        q //= g
        if p == 1:
            return denoms + [q]