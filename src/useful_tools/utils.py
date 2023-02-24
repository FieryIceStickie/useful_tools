from pathlib import Path
from os import PathLike
from collections import deque
from itertools import zip_longest
from typing import TypeVar
from collections.abc import Iterable, Iterator


T = TypeVar('T')


def src_path() -> PathLike:
    return Path(__file__).parent.parent


def round_robin(*iterables: Iterable[T]) -> Iterator[T]:
    """Taken from python docs for collections.deque"""
    iterators = deque(iter(i) for i in iterables)
    while iterators:
        try:
            while True:
                yield next(iterators[0])
                iterators.rotate(-1)
        except StopIteration:
            iterators.popleft()


def zip_string(*strings: str, fillvalue: str = ' ') -> str:
    return ''.join(map(''.join, zip_longest(*strings, fillvalue=fillvalue)))
