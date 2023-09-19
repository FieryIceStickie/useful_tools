from cmath import exp, pi
from collections import Counter, defaultdict
from functools import cache
from itertools import chain, repeat, starmap
from math import isclose, prod
from operator import itemgetter

import numpy.polynomial.polynomial as npoly
from attrs import define, field

from src.useful_tools.math.polynomial import polyify

SUPERSCRIPT = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
SUBSCRIPT = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')


@define(frozen=True, slots=True)
class Unity:
    order: int = field(converter=lambda n: n % UNITY_ROOT)

    def __mul__(self, other):
        if not isinstance(other, Unity):
            if isinstance(other, int):
                return Summation(Counter({self: other}))
            return NotImplemented
        return Unity(self.order + other.order)

    def __rmul__(self, other):
        return self * other

    def __pow__(self, power, modulo=None):
        return Unity(self.order * power)

    def __add__(self, other):
        if not isinstance(other, Unity | int):
            return NotImplemented
        s = Summation()
        s += self
        s += other
        return s

    def __radd__(self, other):
        return self + other

    def __repr__(self):
        return f'ω{str(self.order).translate(SUBSCRIPT)}' if self.order else '1'

    def __lt__(self, other):
        return self.order < other.order


@define(frozen=True)
class Summation:
    args: Counter = field(factory=Counter)

    def __iadd__(self, other):
        if isinstance(other, Unity | int) and other:
            self.args[other] += 1
        return self

    def __add__(self, other):
        if isinstance(other, Unity | int) and other:
            return Summation(self.args + Counter({other: 1}))
        elif isinstance(other, Summation):
            return Summation(self.args + other.args)

    def __str__(self):
        return '+'.join(f'{"" if v == 1 else str(v)}{k}' for k, v in sorted(self.args.items()) if v and k)


def coin_change(m, coins):
    print(f'{coins = }')
    def solve(n, lim):
        if not n:
            yield ()
            return
        if lim is None:
            lim = n
        for k in range(1, min(n, lim) + 1):
            if coins[k]:
                yield from ((k, *i) for i in solve(n-k, k))
    return solve(m, min(m, len(coins)-1))


def newton_method(poly: list[int], k: int) -> int:
    n = len(poly)
    poly = defaultdict(int, {*enumerate(poly)})
    @cache
    def solve(k: int):
        if not k:
            return n-1
        return -k*poly[k] - sum(poly[k-i]*solve(i) for i in range(1, k))
    return solve(k)

def numpy_method(poly, k):
    return round(sum(r**k for r in npoly.Polynomial(poly[::-1]).roots()).real)


def multiset_perms(c: Counter, prev=None):
    if not +c:
        yield ()
        return
    for k, v in c.items():
        if k != prev:
            for n in range(1, v+1):
                c[k] -= 1
                yield from ((k,)*n + i for i in multiset_perms(c, k))
            c[k] += v


def my_method(poly, n):
    m = len(poly) - 1
    res = 0
    w = exp(2j*pi/n)
    print(polyify(poly[::-1]), n)
    # counts = defaultdict(set)
    contribs = Counter()
    for p in coin_change(n, poly):
        padded = Counter(p) + Counter({0: n - len(p)})
        print(f'\nCombo: {", ".join(map(str, chain.from_iterable(starmap(repeat, padded.items()))))}')
        coef = prod(itemgetter(*p)(poly)) if len(p) > 1 else poly[p[0]]
        orders = Counter(sum(k*(m-a[k]) for k in range(n)) % n for a in multiset_perms(padded))
        # counts[tuple(sorted(padded.values()))].add(tuple(orders[k] for k in range(n)))
        # print(f'Orders:')
        # for k in range(n):
        #     prefix = ''
        #     if k in (0, n/2):
        #         prefix = '\033[1;33m'
        #     print(f'{prefix}{k}: {orders[k]}\033[0m')
        contrib = sum(v*w**k for k, v in orders.items())
        assert not round(contrib.imag) and isclose(contrib.real, round(contrib.real))
        contrib = round(contrib.real)
        if contrib % n:
            print(f'Special case: {contrib}')
        else:
            print(f'Scaled: {contrib // n}')
            contribs[contrib // n] += 1
        print(f'Contrib: {round(contrib.real)} * {coef} = {round(contrib.real) * coef}')
        res += coef * contrib
    if not m & 1 or n & 1:
        print('swap sign')
        res = -res
    assert not round(res.imag)
    # for k, v in counts.items():
    #     print(f'Combo: {k}')
    #     print('\n'.join(f'{i} - {j} = {i-j}' for i, j, *_ in v), end='\n\n')
    for k, v in sorted(contribs.items()):
        print(k, v)
    return round(res.real)


def main():
    global UNITY_ROOT
    pt = (1, 1, 1, 1, 1, 1)
    for k in [13]:
        UNITY_ROOT = k
        print(f'Power: {k}')
        a, b, c = newton_method(pt, k), numpy_method(pt, k), my_method(pt, k)
        print(f'\033[0;32mNewton: {a}')
        print(f'Numpy: {b}')
        print(f'Mine: {c}\033[0m')
        assert a == b == c
        print('\n')


if __name__ == '__main__':
    main()
