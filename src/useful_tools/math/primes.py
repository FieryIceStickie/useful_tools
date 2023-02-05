import math
from collections import Counter
from functools import lru_cache
from itertools import product
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
    if n < 1:
        return False
    if n in (2, 3):
        return True
    return all(n % p for p in round_robin(
        (2, 3),
        range(5, int(math.sqrt(n)) + 1, 6),
        range(7, int(math.sqrt(n)) + 1, 6)
    ))


def check_prime(n: int) -> int:
    """
    is_prime(), but returns an integer that divides the number if it is composite
    :param n: num
    :return: 0 if n is prime else a divisor of n (returns -1 for 1)
    """
    for p in range(2, int(math.sqrt(n)) + 1):
        if not n % p:
            return p
    else:
        return 0


def prime_factorization(n: int) -> Counter[int]:
    """
    Determines the prime factorization of n
    :param n: number
    :return: Counter[prime, power] (Returns {1: 1} for n=1, but not recommended to use this behaviour)
    """
    if n == 1:
        return Counter({1: 1})
    factorization = Counter()
    while p := check_prime(n):
        factorization[p] += 1
        n //= p
    factorization[n] += 1
    return factorization


def factors(n: int) -> list[int]:
    prime_powers = [tuple(prime ** i for i in range(power + 1)) for prime, power in prime_factorization(n).items()]
    prime_products = product(*prime_powers)
    return sorted(math.prod(i) for i in prime_products)


def egyptian_decomposition(p: int, q: int) -> list[int]:
    """
    Given a rational number 0 < p/q < 1, find a decomposition of p/q into a sum of distinct unit fractions
    Note: not unique, just finds one expansion
    Example:
    (3, 5) -> [2, 10]
    (7, 22) ->
    :param p: Numerator
    :param q: Denomiator
    :return: Sorted list of denominators of unit fractions
    """
    pass


if __name__ == '__main__':
    pass