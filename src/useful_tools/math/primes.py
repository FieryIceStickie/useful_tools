import math
from bisect import bisect
from collections import Counter
from functools import lru_cache
from itertools import chain, product
from typing import Iterator

from bitarray import bitarray

from src.useful_tools.utils import round_robin


def next_prime(n: int) -> int:
    """
    Given a number, returns the next prime number
    :param n: number
    :return: next prime
    """
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


def sieve_of_eratosthenes(n: int) -> Iterator[int]:
    if n < 9:
        smol_primes = [2, 3, 5, 7]
        yield from smol_primes[:bisect(smol_primes, n)]
        return

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
    yield from (i for i, v in enumerate(sieve[end + 1:], end + 1) if v)


if __name__ == '__main__':
    pass
