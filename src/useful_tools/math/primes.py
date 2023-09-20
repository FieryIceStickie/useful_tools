import math
from bisect import bisect
from collections import Counter, deque
from functools import lru_cache
from itertools import accumulate, chain, cycle, product
from typing import Iterator

from bitarray import bitarray

from src.useful_tools.utils import round_robin

__all__ = ['next_prime', 'is_prime', 'check_prime',
           'prime_factorization', 'factors',
           'gen_primes_below_n', 'sieve_of_eratosthenes', 'infinisieve']


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
    end = math.isqrt(n) + 1
    return all(n % p for p in chain((2, 3), round_robin(
        range(5, end, 6),
        range(7, end, 6)
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
    end = int(math.sqrt(n)) + 1
    for p in chain(
            (2, 3),
            round_robin(range(5, end, 6),
                        range(7, end, 6))
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
        # TODO: Use faster methods
        factorization[p] += 1
        n //= p
    factorization[n] += 1
    return factorization


def factors(n: int) -> list[int]:
    prime_powers = (tuple(prime ** i for i in range(power + 1))
                    for prime, power in prime_factorization(n).items())
    prime_products = product(*prime_powers)
    return sorted(math.prod(i) for i in prime_products)


def gen_primes_below_n(n: int) -> Iterator[int]:
    """
    Generates primes less than or equal to n
    Uses sieve of eratosthenes with (2, 3, 5) wheel
    :param n: Max limit
    :return: Primes
    """
    if n < 31:
        smol_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        yield from smol_primes[:bisect(smol_primes, n)]
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
            sieve[p * p::p] = False
        p += next(diffs)
    yield from (i for i, v in enumerate(sieve[end + 1:], end + 1) if v)


def sieve_of_eratosthenes(n: int) -> bitarray:
    """
    Sieve of eratosthenes
    :param n: Sieve size
    :return: Sieve
    """
    if n < 31:
        return bitarray('0011010100010100010100010000010')[:n+1]

    sieve = bitarray(n + 1)
    sieve.setall(1)

    sieve[:2] = 0
    sieve[4::2] = 0
    sieve[6::3] = 0
    sieve[10::5] = 0

    end = math.isqrt(n)
    diffs = cycle((4, 2, 4, 2, 4, 6, 2, 6))
    p = 7
    while p <= end:
        if sieve[p]:
            sieve[p * p::p] = False
        p += next(diffs)
    return sieve


def infinisieve() -> Iterator[int]:
    """
    Uses an incremental sieve that postpones adding numbers to the net until the sieve exceeds the number's square
    Modified from https://stackoverflow.com/questions/2211990
    """
    # All primes below 49, which is 7**2 as 7 is the first prime after the wheel
    yield from (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)

    # net of {numbers: (step_idx, step_mul)}
    # keeps an incremental sieve for infinite sieving
    nets = {}
    sieve = infinisieve()

    # 2 3 5 wheel sieve
    wheel = [4, 2, 4, 2, 4, 6, 2, 6]
    # Setup cumulative wheel for later step adjustments
    step_idx_dict = {v % 30: i for i, v in enumerate(accumulate(wheel[:-1], initial=7))}
    wheel = deque(wheel)

    # p should start at 7
    [next(sieve) for _ in range(3)]
    p = next(sieve)
    q = p * p

    for i in accumulate(chain([49], cycle((4, 6, 2, 6, 4, 2, 4, 2)))):
        if i in nets:  # If number has been marked -> composite
            step_idx, step_mul = nets.pop(i)  # Prepare step for incrementing net
        elif i < q:  # Number less than p*p which is unmarked -> prime
            yield i
            continue
        else:  # i=p*p since p coprime to 30 => p*p coprime to 30
            # Prepare step for incrementing net since
            # p*p is now another composite to mark off
            step_idx = step_idx_dict[p % 30]
            step_mul = p
            p = next(sieve)
            q = p * p
        wheel_shift = step_idx
        wheel.rotate(-wheel_shift)
        # This works as in (Z/nZ)*, f(n)=p*n is a bijection
        # Hence, if p*p+n*p = p(n+p) is in (Z/nZ)*, then
        # n+p must also be in (Z/nZ)*, and so we can roll the
        # wheel with p's residue, starting from p*p and multiplying
        # by p to ensure we hit only relevant composites
        for m in cycle(wheel):
            i += step_mul * m
            step_idx = (step_idx + 1) % 8
            if i not in nets:
                break
        wheel.rotate(wheel_shift)
        nets[i] = step_idx, step_mul


if __name__ == '__main__':
    pass
