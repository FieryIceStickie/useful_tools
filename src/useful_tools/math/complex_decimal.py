from attrs import define, field
from decimal import Decimal


@define(slots=True, frozen=True)
class ComplexDecimal:
    real: Decimal = field(converter=Decimal)
    imag: Decimal = field(converter=Decimal)

    @classmethod
    def from_complex(cls, /, num: complex):
        return ComplexDecimal(num.real, num.imag)

    def __str__(self):
        return f'{self.real}+{self.imag}j'.replace('+-', '-')

    def __neg__(self):
        return ComplexDecimal(-self.real, -self.imag)

    def conjugate(self):
        return ComplexDecimal(self.real, -self.imag)

    def __add__(self, other):
        return ComplexDecimal(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return self + other.__neg__()


def complexdecimal_main():
    x = ComplexDecimal('Inf', 3)


if __name__ == '__main__':
    complexdecimal_main()
