import math
from bisect import bisect
from itertools import cycle, islice
from typing import Iterator

from bitarray import bitarray


def gen_primes_below_n(n: int) -> Iterator[int]:
    """
    Generates primes less than or equal to n
    Uses sieve of eratosthenes with (2, 3, 5) wheel
    :param n: Max limit
    :return: Primes
    """
    if n < 31:
        smol_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        yield from smol_primes[: bisect(smol_primes, n)]
        return

    sieve = bitarray(n + 1)
    sieve.setall(1)

    sieve[4::2] = 0
    sieve[6::3] = 0
    sieve[10::5] = 0
    yield from (2, 3, 5)

    end = math.isqrt(n)
    diffs = cycle((4, 2, 4, 2, 4, 6, 2, 6))
    p = 7
    while p <= end:
        if sieve[p]:
            yield p
            sieve[p * p :: p] = False
        p += next(diffs)
    yield from (i for i, v in enumerate(sieve[end + 1 :], end + 1) if v)


*primes, = gen_primes_below_n(10000)
nums = []
for p in islice(primes, 1, None):
    n = 1
    for order in range(p):
        n = (2 * n) % p
        if n == 1:
            break
    order += 1
    nums.append((order, p))
nums.sort()
print(nums[:20])


