import math
from collections import Counter
from functools import lru_cache
from itertools import chain, product
from typing import Iterator

from bitarray import bitarray


from src.useful_tools.utils import round_robin


def next_prime(n: int) -> int:
    return 3 if n == 2 else next(p for p in range(n + 2, n * 2, 2) if is_prime(p))


@lru_cache(maxsize=100)
def is_prime(n: int) -> bool:
    """
    Checks if a number is prime
    :param n: number
    :return: bool(n is prime)
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    # TODO: Bigger wheel
    # TODO: probabilistic methods/better methods than trial div
    return all(n % p for p in chain((2, 3), round_robin(
        range(5, math.isqrt(n) + 1, 6),
        range(7, math.isqrt(n) + 1, 6)
    )))


def check_prime(n: int) -> int:
    """
    is_prime(), but returns an integer that divides the number if it is composite
    :param n: num
    :return: 0 if n is prime else a divisor of n
    """
    if n < 2:
        raise ValueError(f'primality of {n} is undefined')
    if n in (2, 3):
        return 0
    for p in chain(
            (2, 3),
            round_robin(range(5, int(math.sqrt(n)) + 1, 6),
                        range(7, int(math.sqrt(n)) + 1, 6))
    ):
        if not n % p:
            return p
    return 0


def prime_factorization(n: int) -> Counter[int]:
    """
    Determines the prime factorization of n
    :param n: number
    :return: Counter[prime, power] (Returns {1: 1} for n=1,
    but this is an implementation detail and should not be relied upon)
    """
    if n == 1:
        return Counter({1: 1})
    factorization = Counter()
    while p := check_prime(n):
        # TODO: Make it a progressive alg so it avoids relooping
        # Probably will require getting rid of check_prime
        factorization[p] += 1
        n //= p
    factorization[n] += 1
    return factorization


def factors(n: int) -> list[int]:
    prime_powers = [tuple(prime ** i for i in range(power + 1)) for prime, power in prime_factorization(n).items()]
    prime_products = product(*prime_powers)
    return sorted(math.prod(i) for i in prime_products)


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


def sieve_of_eratosthenes(n: int) -> Iterator[int]:
    if n < 2:
        return
    elif n == 2:
        yield 2
        return
    p = 4  # For n=3 case

    sieve = bitarray(n + 1)
    sieve.setall(1)

    sieve[4::2] = 0
    sieve[6::3] = 0
    yield from (2, 3)

    end = math.isqrt(n)
    for p in round_robin(
        range(5, end+1, 6),
        range(7, end+1, 6)
    ):
        if sieve[p]:
            yield p
            sieve[p * p::p] = False
    yield from (i for i, v in enumerate(sieve[p:], p) if v)


if __name__ == '__main__':
    print(*sieve_of_eratosthenes(1000))

