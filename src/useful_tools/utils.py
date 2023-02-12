from collections import deque
from os import PathLike
from pathlib import Path


def src_path() -> PathLike:
    return Path(__file__).parent.parent


def round_robin(*iterables):
    """Taken from python docs for collections.deque"""
    iterators = deque(map(iter, iterables))
    while iterators:
        try:
            while True:
                yield next(iterators[0])
                iterators.rotate(-1)
        except StopIteration:
            iterators.popleft()
