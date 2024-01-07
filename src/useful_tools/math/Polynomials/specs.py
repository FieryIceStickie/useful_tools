from typing import Literal, TypedDict, Any, Annotated
from collections.abc import Mapping, Callable

from attrs import define, field, validators, Attribute

from useful_types import SupportsRichComparisonT

__all__ = ['LocalPrintContext', 'active_print_spec']


class PolyPrintSpecKwargs(TypedDict):
    order: Literal['asc', 'desc'] | Callable[[int, int], SupportsRichComparisonT]
    variable: str | Mapping[str, str]
    mode: Literal['visual', 'latex', 'latexfrac', 'spaced', 'repr']


class LocalPrintContext:
    __slots__ = ('saved_print_spec',)

    def __init__(self, **kwargs: PolyPrintSpecKwargs):
        self.saved_print_spec = PolyPrintSpec(**kwargs)

    def __enter__(self):
        global active_print_spec
        active_print_spec, self.saved_print_spec = self.saved_print_spec, active_print_spec

    def __exit__(self, exc_type, exc_val, exc_tb):
        global active_print_spec
        active_print_spec, self.saved_print_spec = self.saved_print_spec, active_print_spec


@define(repr=False)
class PolyPrintSpec:
    # TODO: context manager for setting modes
    order: Annotated[
        Attribute,
        Literal['asc', 'desc'] | Callable[[int, int], SupportsRichComparisonT]
    ] = field(default='desc')
    mode: Literal[
        'visual', 'latex', 'latexfrac',
        'spaced', 'repr', 'spacedrepr'
    ] = field(
        default='visual',
        validator=validators.in_(
            ('visual', 'latex', 'latexfrac', 'spaced', 'repr', 'spacedrepr')
        ))
    _variable: dict[str, str] = field(factory=lambda: {'laurent': 'z', 'regular': 'x'})

    @property
    def variable(self):
        return self._variable

    @variable.setter
    def variable(self, value):
        if isinstance(value, str):
            self._variable['laurent'] = self._variable['regular'] = value
        elif isinstance(value, Mapping):
            for k, v in value.items():
                if k not in ('laurent', 'regular'):
                    raise ValueError(f'{k} is an invalid option for PolyPrintSpec.variable')
                elif not isinstance(v, str):
                    raise ValueError(f'{v!r} is not a valid variable str')
                self._variable[k] = v
        else:
            raise ValueError(f'{value!r} is not a valid variable str')

    @order.validator
    def order_check(self, attribute: Attribute, value: Any):
        if isinstance(value, str) and value not in ('asc', 'desc') and not callable(value):
            raise ValueError(f'{value} is an invalid option for attribute {attribute.name} on PolynomialPrintSpec()')

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'order={self.order!r}, '
            f'variable={self._variable!r}, '
            f'mode={self.mode!r}'
            f')'
        )


active_print_spec = PolyPrintSpec()
