import pytest
from misc.misc import sum_of_restricted_digit_sum_less_than_n


@pytest.mark.parametrize(
    'n,target_digit_sum,result',
    [
        (50, 5, (165, 6)),
        (103, 5, (165, 6)),
        (104, 5, (269, 7)),
        (772336, 23, (14795778894, 41376)),
        (983693, 34, (21091918012, 34093)),
        (926632, 32, (21560278369, 39275)),
        (344820, 8, (130583152, 1160)),
        (848847, 21, (13408397238, 37456)),
        (861822, 24, (18995240055, 46961)),
        (765002, 18, (7115080617, 24151)),
        (220732, 30, (922595097, 7426)),
        (282759, 31, (1399735210, 8614)),
        (66668, 32, (34974932, 775)),
        (28164, 19, (27449810, 1907)),
        (70141, 38, (4277714, 70)),
        (732190, 26, (15843830698, 42434)),
        (423427, 17, (2790920601, 15201)),
        (551915, 6, (50733282, 461)),
        (535796, 9, (296415225, 1945)),
        (817404, 12, (1303009767, 6012)),
        (860960, 41, (2989918427, 4762)),
        (86089, 39, (5320599, 74)),
        (219864, 48, (0, 0)),
        (1999999999999, 100, (391906666666442720, 243542))
    ])
def test_sum_of_restricted_digit_sum_less_than_n(n: int, target_digit_sum: int, result: tuple[int, int]):
    assert sum_of_restricted_digit_sum_less_than_n(n, target_digit_sum) == result


@pytest.mark.parametrize(
    'n,target_digit_sum,base,result',
    [
        (50, 5, 16, (110, 4)),
        (50, 5, 13, (92, 4))
    ]
)
def test_sum_of_restricted_digit_sum_less_than_n_bases(n: int, target_digit_sum: int,
                                                       base: int, result: tuple[int, int]):
    assert sum_of_restricted_digit_sum_less_than_n(n, target_digit_sum, base=base) == result


if __name__ == '__main__':
    pass
