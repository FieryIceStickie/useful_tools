from collections.abc import Callable, Iterator
from functools import cache
from functools import reduce
from itertools import chain, count, islice, product, repeat
from math import factorial, prod
from operator import add, mul
from typing import Any, Self

from attrs import field, frozen
from frozendict import frozendict
from rich.pretty import pprint


class Term[T](frozendict[T, int]):
    def __add__(self, other: Self) -> Self:
        rtn: dict[T, int] = {**self}
        for t, r in other.items():
            rtn[t] = rtn.get(t, 0) + r
        return Term(rtn)

    def __neg__(self) -> Self:
        return Term({t: -r for t, r in self.items()})

    def __sub__(self, other: Self) -> Self:
        return self + (-other)

    def __mul__(self, other: Self | int) -> Self:
        match other:
            case int(c):
                return Term({t: r * c for t, r in self.items()})
        rtn: dict[T, int] = {}
        for t1, r1 in self.items():
            for t2, r2 in other.items():
                t = t1 + t2
                rtn[t] = rtn.get(t, 0) + r1 * r2
        return Term(rtn)

    def __rmul__(self, c: int) -> Self:
        return Term({t: r * c for t, r in self.items()})


@frozen
class Zeta:
    n: int

    def __str__(self) -> str:
        return f'ζ({self.n})'


type ZetaTerm = Term[Zeta]
type ZetaExpr = Term[ZetaTerm]


@frozen
class SeriesTerm[T]:
    coef: T
    power: int


@frozen
class Series[T: Term[Any]]:
    low: int
    term: Callable[[int], T] = field(converter=cache)

    def __getitem__(self, item: int) -> T:
        return Term() if item < self.low else self.term(item)

    def __add__(self, other: 'Series[T]') -> 'Series[T]':
        return Series(
            min(self.low, other.low),
            lambda n: self[n] + other[n],
        )

    def __mul__(self, other: 'Series[T]') -> 'Series[T]':
        low = self.low + other.low
        return Series(
            low,
            lambda n: sum(
                (
                    self[self.low + k] * other[n - self.low - k]  #
                    for k in range(n - low + 1)
                ),
                Term(),
            ),
        )

    def __rmul__(self, other: int) -> 'Series[T]':
        return Series(self.low, lambda n: other * self.term(n))

    def __iter__(self) -> Iterator[T]:
        return map(self.term, count(self.low))


@frozen
class X:
    n: int

    def diff(self, is_x: bool) -> 'Func':
        return X(self.n + 1) if is_x else P(self.n + 1)

    def series(self) -> Series[ZetaExpr]:
        num = (-1) ** self.n * factorial(self.n)
        return Series(-self.n - 1, lambda n: Term({Term[Zeta](): num}) if n == -self.n - 1 else Term())

    def __str__(self) -> str:
        return f'X{self.n or ""}'


@frozen
class Y:
    n: int

    def diff(self, is_x: bool) -> 'Func':
        return P(self.n + 1) if is_x else Y(self.n + 1)

    def series(self) -> Series[ZetaExpr]:
        m = self.n
        return Series(
            1,
            lambda n: Term(
                {
                    Term[Zeta]({Zeta(n + m + 1): 1}):  #
                    (-1) ** (n + m + 1) * prod(range(m + n, n, -1))
                }
            ),
        )

    def __str__(self) -> str:
        return f'Y{self.n or ""}'


@frozen
class P:
    n: int

    def diff(self, is_x: bool) -> 'Func':
        return P(self.n + 1)

    def series(self) -> Series[ZetaExpr]:
        m = self.n
        return Series(
            0,
            lambda n: Term(
                {
                    Term[Zeta]({Zeta(n + m + 1): 1}):  #
                    (-1) ** (n + m + 1) * prod(range(m + n, n, -1))
                }
            ),
        )

    def __str__(self) -> str:
        return f'P{self.n or ""}'


type Func = X | Y | P
type FuncTerm = Term[Func]
type FuncExpr = Term[FuncTerm]


def diff_term(term: FuncTerm, is_x: bool) -> FuncExpr:
    return Term({term + Term({t: -1, t.diff(is_x): 1}): r for t, r in term.items() if r})


def diff_expr(expr: FuncExpr, is_x: bool) -> FuncExpr:
    return sum((coef * diff_term(term, is_x) for term, coef in expr.items()), start=Term[FuncTerm]())


def get_expr(n: int, m: int) -> FuncExpr:
    expr: FuncExpr = Term({Term[Func](): 1})
    for _ in range(n):
        left: FuncExpr = Term({term + Term({X(0): 1}): coef for term, coef in expr.items()})
        right = diff_expr(expr, True)
        expr = left - right
    for _ in range(m):
        left = Term({term + Term({Y(0): 1}): coef for term, coef in expr.items()})
        right = diff_expr(expr, False)
        expr = left - right
    return -expr if (n + m) % 2 else expr


def expr_str[T](expr: Term[Term[T]]) -> str:
    return ' + '.join(f'{coef}{term_str(term)}' for term, coef in expr.items())


def term_str[T](term: Term[T]) -> str:
    return ''.join(f'{t}{f"^{{{r}}}" if r > 1 else ""}' for t, r in term.items() if r)


def eval_term(term: FuncTerm) -> Series[ZetaExpr]:
    return reduce(mul, (z.series() for z in chain.from_iterable(repeat(t, r) for t, r in term.items())))


def eval_expr(expr: FuncExpr) -> Series[ZetaExpr]:
    return reduce(
        add,
        (coef * eval_term(term) for term, coef in expr.items()),
    )


def main():
    expr = get_expr(3, 4)
    for term, coef in expr.items():
        series = eval_term(term)
        # thing = '     '.join(f'{expr_str(m)}z^{i}' for i, m in enumerate(islice(series, 3), series.low))
        print(f'{term_str(term): <15}, {coef: <3}: {expr_str(series[1])}')

    series = eval_expr(expr)
    print(expr_str(series.term(1)))

    print(expr_str(eval_expr(get_expr(1, 2)).term(1)))
    print(expr_str(eval_expr(get_expr(2, 1)).term(1)))

    # for n, m in product(range(5), range(1, 5)):
    #     expr = get_expr(n, m)
    #     series = eval_expr(expr)
    #     print(f'{n}, {m}: {expr_str(series.term(1))}')

    # import sys
    # sys.setrecursionlimit(10000000)

    # expr = get_expr(3, 4)
    # series = eval_expr(expr)
    # print(expr_str(series.term(1)))
    


if __name__ == '__main__':
    main()
