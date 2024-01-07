from collections.abc import Iterator, Mapping, Callable
import heapq
from itertools import groupby
from operator import itemgetter
from useful_types import SupportsRichComparisonT


__all__ = ['SUPERSCRIPT', 'SUBSCRIPT', 'identity', 'ordered_dict_zip', 'filled_ordered_dict_zip']


SUPERSCRIPT = str.maketrans('0123456789+-=()', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾')
SUBSCRIPT = str.maketrans('0123456789+-=()', '₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎')


def _ordered_dict_zip_sort_key[K, V](
        idx: int,
        d: dict[K, V],
        key: Callable[[K], SupportsRichComparisonT],
) -> Iterator[tuple[K, int, V]]:
    yield from ((key(k), idx, v) for k, v in d.items())


def identity[T](elem: T) -> T:
    return elem


def ordered_dict_zip[K, V](
        *dicts: Mapping[K, V],
        key: Callable[[K], SupportsRichComparisonT] | None = None,
) -> Iterator[tuple[K, dict[int, V]]]:
    """
    dict_zip, but keys are outputted in sorted order
    Note: If a dict contains two distinct keys k1, k2 s.t. key(k1)=key(k2), one of them will be discarded
    :param dicts: Dictionaries that have keys in sorted order
    :param key: Key function for sorting the keys
    :returns: Iterator of (key(k), {idx: value})
    """
    if key is None:
        key = identity
    yield from (
        (k, {idx: v for _, idx, v in g})
        for k, g in groupby(
            heapq.merge(*(
                    _ordered_dict_zip_sort_key(idx, d, key)
                    for idx, d in enumerate(dicts)
                )),
            key=itemgetter(0),
        )
    )


def filled_ordered_dict_zip[K, V, Fv](
        *dicts: Mapping[K, V],
        key: Callable[[K], SupportsRichComparisonT] | None = None,
        fillvalue: Fv = None,
) -> Iterator[tuple[K, tuple[V | Fv, ...]]]:
    """
    ordered_dict_zip, but outputs tuples with a fillvalue
    :param dicts: Dictionaries that have keys in sorted order
    :param key: Key function for sorting the keys
    :param fillvalue: Default value to be put into return tuples
    :return: Iterator of (key(k), (idx 0 value/fillvalue, idx 1 value/fillvalue, ...))
    """
    yield from (
        (k, tuple(d.get(idx, fillvalue) for idx in range(len(dicts))))
        for k, d in ordered_dict_zip(*dicts, key=key)
    )
