from collections import defaultdict
from functools import cache, reduce
from math import log
import re
from typing import Iterable, Iterator, Optional, Self, Sequence, TypeVar

from attrs import define, field

T = TypeVar('T')


@define
class Trie:
    count: int = 0
    letters: defaultdict[T, Self] = field(factory=defaultdict)

    def __attrs_post_init__(self):
        self.letters.default_factory = Trie

    def __iadd__(self, other: Iterable[T]):
        self.count += 1
        curr = self
        for c in other:
            curr = curr.letters[c]
            curr.count += 1
        return self

    def __getitem__(self, item: Iterable[T]):
        return reduce(lambda s, c: s.letters[c], item, self)


def recursive_permutations(iterable: Sequence[T], r: Optional[int] = None,
                           current: tuple[int, ...] = (), c: int = 0) -> Iterator[tuple[T, ...]]:
    if r is None:
        r = len(iterable)
    if c == r:
        yield tuple(iterable[i] for i in current)
    for i, v in enumerate(iterable):
        if i not in current:
            yield from recursive_permutations(iterable, r, (*current, i), c + 1)


def recursive_combinations(iterable: Sequence[T], r: Optional[int] = None,
                           current: tuple[int, ...] = (), c: int = 0) -> Iterator[tuple[T, ...]]:
    if r is None:
        r = len(iterable)
    if c == r:
        yield tuple(iterable[i] for i in current)
    for i, v in enumerate(iterable):
        if not current or i > current[-1]:
            yield from recursive_combinations(iterable, r, (*current, i), c + 1)


def iter_bits(num: int, bits=1) -> Iterator[int]:
    mask_num = 2**bits-1
    while num > 0:
        yield num & mask_num
        num >>= bits


def sum_of_restricted_digit_sum_less_than_n(n: int, target_digit_sum: int, *, base: int = 10) -> tuple[int, int]:
    if base < 2:
        raise ValueError('Base cannot be less than 2.')

    length = int(log(n, base)+1)

    if base == 10:
        digits = {i: int(v) for i, v in enumerate(str(n))}
    elif base & (base - 1) == 0:
        digits = {length - i - 1: v for i, v in enumerate(iter_bits(n, int(log(base, 2))))}
    else:
        digits = {}
        num = n
        for i in range(length):
            digits[length - i - 1] = num % base
            num //= base

    @cache
    def solve(i: int, tight: bool, digit_sum: int):
        if digit_sum > target_digit_sum:
            return 0, 0
        if i == length:
            return 0, digit_sum == target_digit_sum
        new_total, new_count = 0, 0
        current_digit = digits[i]
        for digit in range(current_digit+1 if tight else base):
            mid_total, mid_count = solve(i+1, tight and digit == current_digit, digit_sum+digit)
            new_count += mid_count
            new_total += mid_total + digit*base**(length-i-1)*mid_count
        return new_total, new_count
    return solve(0, True, 0)


def obsidian_to_quora(text: str) -> str:
    return re.sub(
        r'\$([^$]+)\$',
        r'[math]\1[/math]',
        re.sub(
            r'\$\$([^$]+)\$\$',
            lambda g: f'[math]{g.group(1).replace('\n', '')}[/math]',
            text
        )
    )


if __name__ == '__main__':
    print(obsidian_to_quora(r"""We want to evaluate the integral
$$
\begin{align*}
\int_{0}^{2\pi} \sin^{6}x\cos^{6}x\,\mathrm{d}x
\tag*{}\end{align*}
$$
via contour integration.
We start off with the substitution $z=e^{ix}$, which converts the integral into a contour integral over the unit circle in the clockwise direction:
$$
\begin{align*}
\int_{0}^{2\pi} \sin^{6}x\cos^{6}x\,\mathrm{d}x&=\oint_{|z|=1}\left( \frac{z-z^{-1}}{2i} \right)^{6}\left( \frac{z+z^{-1}}{2} \right)^{6} \frac{\mathrm{d}z}{iz}.\\
&=\frac{i}{2^{12}}\oint_{|z|=1}(z-z^{-1})^{6}(z+z^{-1})^{6} \frac{\mathrm{d}z}{z}.
\tag*{}\end{align*}
$$
Now we use the residue theorem. By multiplying through, we can see that the only pole of the integrand is the order-$13$ one at $z=0$. The residue is the coefficient of $z^{-1}$ in the Laurent series of the integrand, so we just need to find the constant coefficient of $(z-z^{-1})^{6}(z+z^{-1})^{6}$:
$$
\begin{align*}
(z-z^{-1})^{6}(z+z^{-1})^{6}&=(z^{2}-z^{-2})^{6}\\
&=\sum_{k=0}^{6} \binom{6}{k} z^{2(6-k)}(-1)^{k}z^{-2k}\\
&=\sum_{k=0}^{6} \binom{6}{k} (-1)^{k}z^{12-4k}.
\tag*{}\end{align*}
$$
Thus, the residue is $\displaystyle-\binom{6}{3}$, and so by the residue theorem we have that
$$
\begin{align*}
\oint_{|z|=1}(z-z^{-1})^{6}(z+z^{-1})^{6} \frac{\mathrm{d}z}{z}&=-2\pi i \binom{6}{3}.
\tag*{}\end{align*}
$$
Finally, we get that
$$
\begin{align*}
\int_{0}^{2\pi} \sin^{6}x\cos^{6}x\,\mathrm{d}x&=\frac{\pi}{2^{11}} \binom{6}{3}\\
&=\frac{5\pi}{512}.
\tag*{}\end{align*}
$$

"""))
