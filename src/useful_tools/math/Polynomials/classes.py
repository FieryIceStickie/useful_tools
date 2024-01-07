from typing import Self
from collections.abc import Iterable, Mapping
from operator import pos, neg, add, sub, mul
from io import StringIO

from frozendict import frozendict

from specs import active_print_spec, LocalPrintContext
from number_types import get_least_bounding_num_type, CRingType
from utils import ordered_dict_zip, filled_ordered_dict_zip, SUPERSCRIPT


def _svlp_operator_fallbacks(monomorphic_op, fallback_op):
    def forward(self, other):
        if isinstance(other, SingleVariableLaurentPolynomial):
            return monomorphic_op(
                self.coef_dict, other.coef_dict,
                get_least_bounding_num_type((self.coef_type, other.coef_type))
            )
        elif issubclass(self.coef_type, type(other)):
            return monomorphic_op(
                self, {0: self.coef_type(other)},
                self.coef_type
            )
        else:
            return NotImplemented

    forward.__name__ = f'__{fallback_op.__name__}__'
    forward.__doc__ = monomorphic_op.__doc__

    def reverse(self, other):
        if isinstance(other, SingleVariableLaurentPolynomial):
            return monomorphic_op(
                other.coef_dict, self.coef_dict,
                get_least_bounding_num_type((self.coef_type, other.coef_type))
            )
        elif issubclass(self.coef_type, type(other)):
            return monomorphic_op(
                {0: self.coef_type(other)}, self.coef_dict,
                self.coef_type,
            )
        else:
            return NotImplemented

    reverse.__name__ = f'__{fallback_op.__name__}__'
    reverse.__doc__ = monomorphic_op.__doc__
    return forward, reverse


class SingleVariableLaurentPolynomial[CT: CRingType]:
    """
    A laurent polynomial with coefficients in CT
    """
    __slots__ = ('_coef_type', '_coef_dict')

    def __init__(self,
                 coefs: Iterable[tuple[int, CT]] | Mapping[int, CT] = None,
                 inp_coef_type: type[CT] | None = None):
        # TODO: Add type checking
        self._coef_dict = frozendict(
            (power, coef)
            for power, coef in (coefs.items() if isinstance(coefs, Mapping) else coefs)
            if coef
        )
        self._coef_type = inp_coef_type or get_least_bounding_num_type(self._coef_dict.values())

    @property
    def coef_dict(self):
        return self._coef_dict

    @property
    def coef_type(self):
        return self._coef_type

    def __pos__(self) -> Self:
        return SingleVariableLaurentPolynomial(
            [(k, pos(v)) for k, v in self.coef_dict.items()],
            self.coef_type,
        )

    def __neg__(self) -> Self:
        return SingleVariableLaurentPolynomial(
            [(k, neg(v)) for k, v in self.coef_dict.items()],
            self.coef_type,
        )

    def get_coef_parts(self, num: CT, *, is_first: bool, is_constant: bool):
        """
        Returns '+num' or 'num' or '-num' depending on the polynomial term
        Also removes 1 if needed
        :param num: The term coefficient
        :param is_first: Whether the term is the first term
        :param is_constant: Whether the term is the constant term
        :return: The operator string
        """
        num_str = str(num)
        if num_str[0] == '-':
            sgn = '-'
            abs_num_str = num_str[1:]
        else:
            sgn = '' if is_first else '+'
            abs_num_str = num_str
        if not is_constant and (num == self.coef_type.mul_id
                                or -num == self.coef_type.mul_id and sgn == '-'):
            return sgn, ''
        else:
            return sgn, abs_num_str

    def get_display(self, x: str) -> str:
        if not self.coef_dict:
            return str(self.coef_type.add_id)
        rtn_str = StringIO()
        is_first = True
        match active_print_spec.order:
            case 'asc':
                coef_it = self.coef_dict.items()
            case 'desc':
                coef_it = reversed(self.coef_dict.items())
            case key_func:
                coef_it = sorted(self.coef_dict.items(), key=key_func)

        space = ' ' if active_print_spec.mode in ('spaced', 'spacedrepr') else ''

        for power, coef in coef_it:
            sgn, coef_str = self.get_coef_parts(coef, is_first=is_first, is_constant=power == 0)
            if power == 0:
                term_str = f'{sgn}{space if sgn and not is_first else ''}{coef_str}'
            elif power == 1:
                term_str = (f'{sgn}{space if sgn and not is_first else ''}'
                            f'{coef_str}{'*' if active_print_spec.mode == 'repr' else ''}{x}')
            else:
                if power < 0 and active_print_spec.mode == 'latexfrac':
                    if power == -1:
                        term_str = fr'{sgn}\frac{{{coef_str or self._coef_type.mul_id}}}{{{x}}}'
                    else:
                        term_str = fr'{sgn}\frac{{{coef_str or self._coef_type.mul_id}}}{{{x}^{{{-power}}}}}'
                elif active_print_spec.mode in ('latex', 'latexfrac'):
                    term_str = f'{sgn}{coef_str}{x}^{{{power}}}'
                elif active_print_spec.mode in ('visual', 'spaced'):
                    term_str = (f'{sgn}{space if sgn and not is_first else ''}{coef_str}'
                                f'{x}{str(power).translate(SUPERSCRIPT)}')
                elif active_print_spec.mode in ('repr', 'spacedrepr'):
                    term_str = (f'{sgn}{space if sgn and not is_first else ''}{coef_str}'
                                f'{'*' if coef_str else ''}{x}**{power}')
                else:
                    raise ValueError('Unknown coef branch\n'
                                     f'{power = }\n{coef = }\n{active_print_spec = }')
            rtn_str.write(term_str + space)
            is_first = False
        return rtn_str.getvalue().rstrip()

    def __str__(self):
        return self.get_display(active_print_spec.variable['laurent'])

    def __repr__(self):
        with LocalPrintContext(mode='repr'):
            return self.get_display(active_print_spec.variable['laurent'])

    @staticmethod
    def _add(self: Mapping[int, CT], other: Mapping[int, CT], inp_coef_type: type[CT]) -> Self:
        return SingleVariableLaurentPolynomial(
            [(power, a + b)
             for power, (a, b) in filled_ordered_dict_zip(
                self, other,
                fillvalue=inp_coef_type.add_id,
            )],
            inp_coef_type,
        )

    __add__, __radd__ = _svlp_operator_fallbacks(_add, add)

    @classmethod
    def sum(cls, *polys: Self, weights: Iterable[CT] | None = None) -> Self:
        resultant_type = get_least_bounding_num_type(poly.coef_type for poly in polys)
        *weights, = weights or []
        return cls([
            (
                power,
                sum(
                    (weights[idx] if idx < len(weights) else resultant_type.mul_id) * v
                    for idx, v in coefs.items()
                ),
            )
            for power, coefs in ordered_dict_zip(
                *[poly.coef_dict for poly in polys]
            )],
            resultant_type,
        )

    @staticmethod
    def _sub(self: Mapping[int, CT], other: Mapping[int, CT], inp_coef_type: type[CT]) -> Self:
        return SingleVariableLaurentPolynomial(
            [(power, a - b)
             for power, (a, b) in filled_ordered_dict_zip(
                self, other,
                fillvalue=inp_coef_type.add_id,
            )],
            inp_coef_type,
        )

    __sub__, __rsub__ = _svlp_operator_fallbacks(_sub, sub)

    @staticmethod
    def _mul(self: Mapping[int, CT], other: Mapping[int, CT], inp_coef_type: type[CT]) -> Self:
        return SingleVariableLaurentPolynomial(
            [(power, sum(coefs.values()))
             for power, coefs in ordered_dict_zip(
                *[{k1 + k2: v1 * v2 for k2, v2 in other.items()} for k1, v1 in self.items()]
            )],
            inp_coef_type,
        )

    __mul__, __rmul__ = _svlp_operator_fallbacks(_mul, mul)

    @classmethod
    def prod(cls, *polys: Self) -> Self:
        return NotImplemented

    def diff(self) -> Self:
        # TODO: Learn how differential operators work with polynomials over other fields
        return SingleVariableLaurentPolynomial(
            [(power - 1, power * coef) for power, coef in self.coef_dict.items() if power],
            self.coef_type
        )


if __name__ == '__main__':
    def main():
        from number_types import Integer
        active_print_spec.mode = 'spaced'
        active_print_spec.order = 'desc'
        active_print_spec.variable['laurent'] = 'x'
        # polys = [SingleVariableLaurentPolynomial(k, Integer) for k in (
        #     {-1: 3, 3: -7, 5: 2},
        #     {-3: -2, -2: -1, 0: -1, 1: 2, 2: -2, 5: 5, 6: -2, 9: -1},
        #     {-5: 1, 0: -1, 2: 7, 7: -7},
        #     {-5: -1, -4: 3, -2: -1, 0: -1},
        # )]
        # print(*polys, sep='\n')
        # print(SingleVariableLaurentPolynomial.sum(*polys))
        h = SingleVariableLaurentPolynomial({0: 1}, Integer)
        print(0, h)
        a = SingleVariableLaurentPolynomial({1: 2}, Integer)
        for n in range(1, 11):
            h = a*h - h.diff()
            print(n, h)

    main()
