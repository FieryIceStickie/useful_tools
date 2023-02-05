from einspect import impl
from itertools import product
import pytest


@impl(int)
def __matmul__(self, other):
    return int(not(self&other))


def full_adder(a: int, b: int, c: int):
    return a@b@(a@b@a@(a@b@b)@c),a@b@a@(a@b@b)@c@(a@b@a@(a@b@b))@(a@b@a@(a@b@b)@c@c)


def add(a, b):
    c, *n = 0,
    while a|b:
        c, i = full_adder(a & 1, b & 1, c)
        n += [i]
        a >>= 1
        b >>= 1
    return [c, *n[::-1]]


if __name__ == '__main__':
    pass