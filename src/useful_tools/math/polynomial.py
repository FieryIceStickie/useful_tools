import copy
import re
from collections import defaultdict
from decimal import Decimal
from itertools import chain, product
from math import prod
from typing import Sequence

from Math.complexdecimal import ComplexDecimal


class CoefDict:
    """
    Defaultdict wrapper for coefficients of a polynomial
    """

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], dict | defaultdict | type(self)):
            self.dict = defaultdict(Decimal, {int(k): Decimal(v) for k, v in args[0].items()})
        else:
            self.dict = defaultdict(Decimal, [(int(k), Decimal(v)) for k, v in chain(*args)])

    def sanitize(self):
        """
        Removes zero values from dict
        :return: self
        """
        self.dict = defaultdict(Decimal, {i: v for i, v in self.items() if not v.is_zero()})
        return self

    def __neg__(self):
        return CoefDict({i: -v for i, v in self.items()})

    def __eq__(self, other):
        self.sanitize()
        other.sanitize()
        return self.dict == other.dict

    def __bool__(self):
        self.sanitize()
        return bool(self.dict)

    def __repr__(self):
        dict_str = re.search(r'defaultdict\(<class \'.+\'>, (.+)\)', str(self.dict)).group(1)
        return f'CoefDict({dict_str})'

    def __add__(self, other):
        coef_dict = copy.deepcopy(self)
        for power, coef in other.items():
            coef_dict[power] += coef
        return CoefDict(coef_dict)

    def __sub__(self, other):
        return self.__add__(other.__neg__())

    def __mul__(self, other):
        # Todo: Karatsuba
        coef_dict = CoefDict()
        for power, coef in ((sum(p), prod(c))
                            for p, c in (zip(*i) for i in product(self.items(), other.items()))):
            coef_dict[power] += coef
        return coef_dict

    def __divmod__(self, other) -> tuple:
        """
        Implements expanded polynomial synthetic division
        P(x) = D(x)Q(x) + R(x)
        :param self: P(x)
        :param other: D(x)
        :return: Q(x), R(x)
        """
        # Zero checks
        if not other:
            raise ZeroDivisionError
        elif not self:
            return CoefDict(), CoefDict()

        # Check if degree of numerator >= degree of denominator
        self_deg, other_deg = self.degree(), other.degree()
        if self_deg < other_deg:
            return CoefDict(), self

        # Shifts quotient power so that the remainder coefficients have negative power
        quotient = CoefDict({i - other_deg: v for i, v in self.items()})

        # Extracts leading term and negates divisor
        leading_coef = other[other_deg]
        divisor = copy.deepcopy(other)
        del divisor[other_deg]
        divisor = -divisor

        # Synthetic division
        for i in reversed(range(self_deg - other_deg + 1)):
            dropped_coef = quotient[i] / leading_coef
            quotient += CoefDict({i - other_deg + p: dropped_coef * v for p, v in divisor.items()})

        # Extracts remainder from negative powers of quotient
        remainder = CoefDict({p + other_deg: quotient.pop(p) for p in [*quotient.keys()] if p < 0})

        # Rescales the quotient for non-monic divisors
        quotient = CoefDict({i: v / leading_coef for i, v in quotient.items()})

        return quotient, remainder

    def __floordiv__(self, other):
        return self.__divmod__(other)[0]

    def __mod__(self, other):
        return self.__divmod__(other)[1]

    def __getitem__(self, k):
        return self.dict.__getitem__(k)

    def __setitem__(self, k, v):
        self.dict.__setitem__(k, v)

    def __delitem__(self, k):
        self.dict.__delitem__(k)

    def keys(self):
        return self.dict.keys()

    def values(self):
        return self.dict.values()

    def items(self):
        return self.dict.items()

    def pop(self, k):
        return self.dict.pop(k)

    def degree(self):
        self.sanitize()
        return max(self.keys()) if self else Decimal('Inf')

    def is_constant(self) -> bool:
        """
        :return:  Whether the polynomial is a constant one (Zero polynomial is not constant)
        """
        self.sanitize()
        try:
            x = any(i != 1 for i in self.keys()) and bool(self.dict[0])
            return x
        except KeyError:
            return False


class Polynomial:
    """
    Class for a single variable polynomial
    Priority for descending ordered polynomials (except for from_iterable)
    Stored as a dictionary: power -> coefficient, and an integer degree
    """

    def __init__(self, /, coef_dict: CoefDict, *, variable: str = 'x'):
        """
        Dunder Init
        :param coef_dict: CoefDict
        :param variable: The polynomial variable
        """
        self.variable = variable
        self.coef_dict = coef_dict

    @classmethod
    def from_str(cls, /, poly_str: str, *, variable: str = 'x'):
        """
        Create a polynomial object from a string. Has to be a valid polynomial string for proper usage
        :param poly_str: The given string
        :param variable: The polynomial variable
        :return: The corresponding polynomial object
        """
        groups = re.findall(fr'(\A\b|[+-])(\d*)({variable})?(?:\^(\d*))?', poly_str)
        coef_dict = CoefDict()
        for sgn, coef, var, power in groups:
            coefficient = Decimal(coef if coef else 1) * (-1 if sgn == '-' else 1)
            term_power = int(power) if power else 1 if var else 0
            coef_dict[term_power] += coefficient
        return cls(coef_dict, variable=variable)

    @classmethod
    def from_iterable(cls, /, coef_iter: Sequence[Decimal], *, is_descending: bool = False, variable: str = 'x'):
        """
        Create a polynomial object from an Iterable
        Has to be an Iterable[Decimal | int] of either ascending or descending order
        :param coef_iter: The given iterable
        :param is_descending: Whether the iterable has descending coefficients
        :param variable: The polynomial variable
        :return: The corresponding polynomial object
        """
        coef_dict = CoefDict()
        if is_descending:
            coef_iter = reversed(coef_iter)
        for p, v in enumerate(coef_iter):
            coef_dict[p] += v
        return cls(coef_dict, variable=variable)

    def __eq__(self, other):
        return self.variable == other.variable and (
                {i: v for i, v in self.coef_dict.items() if not v.is_zero()} ==
                {i: v for i, v in other.coef_dict.items() if not v.is_zero()}
        )

    def __bool__(self):
        return bool(self.degree)

    def __call__(self, inp_num: int | float | Decimal) -> Decimal:
        """
        Evaluates the polynomial at the specified number
        :param inp_num: Specified number
        :return: Result
        """
        return sum((coef * Decimal(inp_num ** power) for power, coef in self.coef_dict.items()), Decimal(0))

    def __add__(self, other):
        if self.variable != other.variable:
            return NotImplemented
        return Polynomial(self.coef_dict.__add__(other.coef_dict), variable=self.variable)

    def __neg__(self):
        return Polynomial(self.coef_dict.__neg__(), variable=self.variable)

    def __sub__(self, other):
        if self.variable != other.variable:
            return NotImplemented
        return Polynomial(self.coef_dict.__sub__(other.coef_dict), variable=self.variable)

    def __mul__(self, other):
        if self.variable != other.variable:
            return NotImplemented
        return Polynomial(self.coef_dict.__mul__(other.coef_dict), variable=self.variable)

    def __divmod__(self, other):
        if self.variable != other.variable:
            return NotImplemented
        return tuple(Polynomial(i, variable=self.variable) for i in (self.coef_dict.__divmod__(other.coef_dict)))

    def __floordiv__(self, other):
        if self.variable != other.variable:
            return NotImplemented
        return Polynomial(self.coef_dict.__floordiv__(other.coef_dict), variable=self.variable)

    def __mod__(self, other):
        if self.variable != other.variable:
            return NotImplemented
        return Polynomial(self.coef_dict.__mod__(other.coef_dict), variable=self.variable)

    def get_list(self, *, descending: bool = True) -> list[Decimal]:
        if descending:
            return [self.coef_dict[i] for i in reversed(range(self.degree() + 1))]
        else:
            return [self.coef_dict[i] for i in range(self.degree() + 1)]

    def get_string(self, *, descending: bool = True):
        rtn_str = ''
        for power, coef in sorted(self.coef_dict.items(), reverse=descending):
            match coef, power:
                case 0, _:
                    pass
                case v, 0:
                    rtn_str += coef_display(v, is_first=not rtn_str, is_constant=True)
                case v, 1:
                    rtn_str += f'{coef_display(v, is_first=not rtn_str)}{self.variable}'
                case v, p:
                    rtn_str += f'{coef_display(v, is_first=not rtn_str)}{self.variable}^{p}'
        return rtn_str or '0'

    def __str__(self):
        # TODO: Implement superscript power notation
        return self.get_string()

    def __repr__(self):
        return self.__str__()

    def degree(self) -> int:
        return self.coef_dict.degree()

    def is_constant(self) -> bool:
        return self.coef_dict.is_constant()

    def get_roots(self) -> tuple[ComplexDecimal, ...]:
        pass


def polyify(inp: str | Sequence | CoefDict, /, **kwargs) -> Polynomial:
    """
    Converts an input into a polynomial
    :param inp: A str of the polynomial, an iterable with the coefficients of the polynomial, or the CoefDict
    :param kwargs:
        - variable: The polynomial variable, defaults to x
        - is_descending: Descending kwarg for Polynomial.from_iterable
    :return: Polynomial object
    """
    match inp:
        case str():
            return Polynomial.from_str(inp, **kwargs)
        case inp if isinstance(inp, Sequence):
            return Polynomial.from_iterable(inp, **kwargs)
        case CoefDict():
            return Polynomial(inp, **kwargs)
        case unknown:
            raise InvalidPolynomialTypeError(type(unknown))


def coef_display(num: Decimal, *, is_first: bool = False, is_constant: bool = False):
    """
    Returns '+num' or 'num' or '-num' depending on the polynomial term
    Also removes 1 if needed
    :param num: The term coefficient
    :param is_first: Whether the term is the first term
    :param is_constant: Whether the term is the constant term
    :return: The operator string
    """
    sign = Decimal(1).copy_sign(num)
    sign = '' if is_first and sign == 1 else ('+' if sign == 1 else '-')
    mag = num.copy_abs()
    return f'{sign}{"" if not is_constant and mag == 1 else mag}'


def polynomial_main():
    p = polyify('x^100-1')
    q = polyify('x^5-1')
    print(p, q)
    print(divmod(p, q))


if __name__ == '__main__':
    # Todo: more tests
    # Todo: Implement Horner's rule
    # Todo: Maybe Karatsuba?
    # Todo: Restructure class to remove CoefDict
    polynomial_main()
