from decimal import Decimal

import pytest

from src.useful_tools.math.polynomial import polyify


@pytest.mark.parametrize('p_input,order,p_output', [
    ('0', True, '0'),
    ('-0', True, '0'),
    ('1', True, '1'),
    ('17', True, '17'),
    ('-17', True, '-17'),
    ('0', False, '0'),
    ('-0', False, '0'),
    ('1', False, '1'),
    ('17', False, '17'),
    ('-17', False, '-17'),
])
def test_constant_polynomial_from_str_to_str(p_input: str, order: bool, p_output: str):
    """
    Tests string representations of polynomials of degree 0
    :param p_input: Input polynomial from str
    :param order: Ascending or descending display
    :param p_output: Output polynomial
    """
    assert polyify(p_input).get_string(descending=order) == p_output


@pytest.mark.parametrize('p_input,order,p_output', [
    ([0], True, '0'),
    ([Decimal('-0')], True, '0'),
    ([1], True, '1'),
    ([17], True, '17'),
    ([-17], True, '-17'),
    ([0], False, '0'),
    ([Decimal('-0')], False, '0'),
    ([1], False, '1'),
    ([17], False, '17'),
    ([-17], False, '-17'),
])
def test_constant_polynomial_from_iter_to_str(p_input: list, order: bool, p_output: str):
    """
    Tests string representations of polynomials of degree 0
    :param p_input: Input polynomial from iterable
    :param order: Ascending or descending display
    :param p_output: Output polynomial
    """
    assert polyify(p_input).get_string(descending=order) == p_output


@pytest.mark.parametrize('p_input,order,p_output', [
    ('1+x', True, 'x+1'),
    ('10x+1', True, '10x+1'),
    ('1-10x', True, '-10x+1'),
    ('1x-1', True, 'x-1'),
    ('-4x+7', True, '-4x+7'),
    ('x^2+2x+1', True, 'x^2+2x+1'),
    ('2x^2-7x+6', True, '2x^2-7x+6'),
    ('15x^8-x', True, '15x^8-x'),
    ('7x^2-7x^8+7x^1+7x^2+0+7', True, '-7x^8+14x^2+7x+7'),
    ('1+x', False, '1+x'),
    ('10x+1', False, '1+10x'),
    ('1-10x', False, '1-10x'),
    ('1x-1', False, '-1+x'),
    ('-4x+7', False, '7-4x'),
    ('x^2+2x+1', False, '1+2x+x^2'),
    ('2x^2-7x+6', False, '6-7x+2x^2'),
    ('15x^8-x', False, '-x+15x^8'),
    ('7x^2-7x^8+7x^1+7x^2+0+7', False, '7+7x+14x^2-7x^8'),
])
def test_polynomial_from_str_order_invariance(p_input: str, order: bool, p_output: str):
    """
    Tests string representations of polynomials of nonzero degree
    :param p_input: Input polynomial from str
    :param order: Ascending or descending display
    :param p_output: Output polynomial
    """
    assert polyify(p_input).get_string(descending=order) == p_output


@pytest.mark.parametrize('p_input,order,p_output', [
    ([1, 1], True, 'x+1'),
    ([1, 10], True, '10x+1'),
    ([1, -10], True, '-10x+1'),
    ([-1, 1], True, 'x-1'),
    ([7, -4], True, '-4x+7'),
    ([1, 2, 1], True, 'x^2+2x+1'),
    ([6, -7, 2], True, '2x^2-7x+6'),
    ([0, -1, 0, 0, 0, 0, 0, 0, 15], True, '15x^8-x'),
    ([7, 7, 14, 0, 0, 0, 0, 0, -7], True, '-7x^8+14x^2+7x+7'),
    ([1, 1], False, '1+x'),
    ([1, 10], False, '1+10x'),
    ([1, -10], False, '1-10x'),
    ([-1, 1], False, '-1+x'),
    ([7, -4], False, '7-4x'),
    ([1, 2, 1], False, '1+2x+x^2'),
    ([6, -7, 2], False, '6-7x+2x^2'),
    ([0, -1, 0, 0, 0, 0, 0, 0, 15], False, '-x+15x^8'),
    ([7, 7, 14, 0, 0, 0, 0, 0, -7], False, '7+7x+14x^2-7x^8'),
])
def test_polynomial_from_iterable_to_str(p_input: list, order: bool, p_output: str):
    """
    Tests string representations of polynomials of nonzero degree
    :param p_input: Input polynomial from iterable
    :param order: Ascending or descending display
    :param p_output: Output polynomial
    """
    assert polyify(p_input).get_string(descending=order) == p_output


@pytest.mark.parametrize('p1_input,p2_input,p_output', [
    ('1+x', '1-x', '2'),
    ('-x+1', 'x-1', '0'),
    ('0', '1', '1'),
    ('1', 'x^3+7x^2-8x+3', 'x^3+7x^2-8x+4'),
    ('x^2+7x+8', '7x-1', 'x^2+14x+7'),
    ('x^2+2x+1', 'x^2-2x+1', '2x^2+2'),
    ('3x^2+7x+15', 'x^4+10x^3-7x^2+1', 'x^4+10x^3-4x^2+7x+16'),
    ('x^19+1', 'x^3-x', 'x^19+x^3-x+1')
])
def test_polynomial_addition(p1_input: str, p2_input: str, p_output: str):
    """
    Tests addition of polynomials
    :param p1_input: Input polynomial1 from str
    :param p2_input: Input polynomial2 from str
    :param p_output: Output polynomial1 + polynomial2
    :return:
    """
    assert polyify(p1_input) + polyify(p2_input) == polyify(p_output)


@pytest.mark.parametrize('p1_input,p2_input,p_output', [
    ('1+x', '1-x', '-x^2+1'),
    ('x+1', 'x+1', 'x^2+2x+1'),
    ('1', 'x^3+7x^2-8x+3', 'x^3+7x^2-8x+3'),
    ('0', 'x^3+7x^2-8x+3', '0'),
    ('0', '1', '0'),
    ('x^2+7x+8', '7x-1', '7x^3+48x^2+49x-8'),
    ('x^2+2x+1', 'x^2-2x+1', 'x^4-2x^2+1'),
    ('3x^2+7x+15', 'x^4+10x^3-7x^2+1', '3x^6+37x^5+64x^4+101x^3-102x^2+7x+15'),
    ('x^19+1', 'x^3-x', 'x^22-x^20+x^3-x')
])
def test_polynomial_multiplication(p1_input: str, p2_input: str, p_output: str):
    assert polyify(p1_input) * polyify(p2_input) == polyify(p_output)


@pytest.mark.parametrize('p1_input,p2_input,p1_output,p2_output', [
    ('0', 'x', '0', '0'),
    ('1', 'x', '0', '1'),
    ('x', 'x', '1', '0'),
    ('x', 'x+1', '1', '-1'),
    ('x^2', 'x+1', 'x-1', '1'),
    ('x^99', 'x^100', '0', 'x^99'),
    ('x^2+2x+1', 'x-1', 'x+3', '4'),
    ('x^10-1', 'x-1', 'x^9+x^8+x^7+x^6+x^5+x^4+x^3+x^2+x+1', '0'),
    ('7x^5+4x^4-39x^3+x-6', 'x^3-7x^2+9x-9', '7x^2+53x+269', '1469x^2-1943x+2415'),

])
def test_polynomial_divmod(p1_input: str, p2_input: str, p1_output: str, p2_output: str):
    assert divmod(polyify(p1_input), polyify(p2_input)) == (polyify(p1_output), polyify(p2_output))


@pytest.mark.parametrize('p1_input, p2_input', [
    ('x^2+1', '0'),
    ('x', '0'),
    ('0', '0')
])
def test_polynomial_zero_div(p1_input: str, p2_input: str):
    with pytest.raises(ZeroDivisionError):
        divmod(polyify(p1_input), polyify(p2_input))
