import pytest

from src.useful_tools.compsci.bit_ops import full_adder


@pytest.mark.parametrize('a, b, c, high, low', [
    (0, 0, 0, 0, 0),
    (0, 0, 1, 0, 1),
    (0, 1, 0, 0, 1),
    (0, 1, 1, 1, 0),
    (1, 0, 0, 0, 1),
    (1, 0, 1, 1, 0),
    (1, 1, 0, 1, 0),
    (1, 1, 1, 1, 1)
])
def test_full_adder(a: int, b: int, c: int, high: int, low: int):
    assert full_adder(a, b, c) == (high, low)
