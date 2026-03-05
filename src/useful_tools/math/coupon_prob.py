from functools import cache
from itertools import accumulate, count, repeat
from math import factorial
import random


@cache
def stirling2(n: int, k: int) -> int:
    if n == k:
        return 1
    elif not k or not n:
        return 0
    return k * stirling2(n - 1, k) + stirling2(n - 1, k - 1)


def prob_after_x_rolls(n: int, x: int) -> int:
    return factorial(n - 1) / n ** (x - 1) * stirling2(x - 1, n - 1)


def main():
    # n = 26
    # for i, p in enumerate(accumulate(map(prob_after_x_rolls, repeat(n), count(1))), start=1):
    #     print(i, p)
    #     if p > 0.95:
    #         break

    N = 26
    n = 26


if __name__ == '__main__':
    main()
