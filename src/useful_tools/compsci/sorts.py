from typing import MutableSequence, Sequence, TypeVar

M = TypeVar('M', bound=Sequence)
S = TypeVar('S', bound=MutableSequence)


def bubble_sort(arr: M) -> M:
    pass


def optimized_bubble_sort(arr: M) -> M:
    pass


def merge_sort(arr: S) -> S:
    pass


def heap_sort(arr: S) -> S:
    pass


def quick_sort(arr: M) -> M:
    pass


def radix_sort(arr: S) -> S:
    pass


if __name__ == '__main__':
    bubble_sort([1, 2, 3, 4, 5])
