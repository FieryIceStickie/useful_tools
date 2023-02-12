import pytest

from src.useful_tools.math.primes import check_prime, is_prime


@pytest.mark.parametrize('prime,primality', [
    (0, False),
    (1, False),
    (2, True),
    (3, True),
    (4, False),
    (5, True),
    (7, True),
    (9, False),
    (17, True),
    (74017, True),
    (90703, True),
    (59999, True),
    (561, False),  # Carmichael_1
    (41041, False),  # Carmichael_2
    (825265, False),  # Carmichael_3
    (2147483647, True),  # Mersenne_31
    (137438953471, False),  # Mersenne_37
    (65537, True),  # Fermat_4
    (4294967297, False)  # Fermat_5
])
def test_is_prime(prime: int, primality: bool):
    assert is_prime(prime) == primality


@pytest.mark.parametrize('prime,result', [
    (2, 0),
    (3, 0),
    (4, 2),
    (5, 0),
    (7, 0),
    (9, 3),
    (17, 0),
    (74017, 0),
    (90703, 0),
    (59999, 0),
    (561, 3),  # Carmichael_1
    (41041, 7),  # Carmichael_2
    (825265, 5),  # Carmichael_3
    (2147483647, 0),  # Mersenne_31
    (137438953471, 223),  # Mersenne_37
    (65537, 0),  # Fermat_4
    (4294967297, 641)  # Fermat_5
])
def test_check_prime(prime: int, result: int):
    assert check_prime(prime) == result


@pytest.mark.parametrize('n', [-2, -1, 0, 1])
def test_check_prime_domain(n: int):
    with pytest.raises(ValueError):
        check_prime(n)
