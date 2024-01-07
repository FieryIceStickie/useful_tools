from typing import Protocol, Self, ClassVar, Any
from collections.abc import Iterable

from useful_types import SupportsRichComparisonT

__all__ = ['get_least_bounding_num_type', 'CRingType', 'Integer']


def get_least_bounding_num_type[T](args: Iterable[T]) -> type[T]:
    if not args:
        raise ValueError(f'get_least_bounding_num_type() passed no types')
    types = set(args)
    if len(types) == 1:
        return next(iter(types))
    return NotImplemented


class CRingType(Protocol):
    """Commutative Ring Type"""
    add_id: ClassVar[Self]
    mul_id: ClassVar[Self]

    def __add__(self, other: Self) -> Self: ...

    def __radd__(self, other: Self) -> Self: ...

    def __mul__(self, other: int | Self) -> Self: ...

    def __rmul__(self, other: int | Self) -> Self: ...

    def __pow__(self, power: int, modulo: Self = None) -> ...: ...


class Integer(int):
    add_id = 0
    mul_id = 1


