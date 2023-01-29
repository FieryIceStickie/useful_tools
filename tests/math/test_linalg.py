import pytest
from src.useful_tools.math.linalg import row_echelon_form
import numpy as np
from numpy.typing import ArrayLike


@pytest.mark.parametrize('input_matrix, output_matrix, matrix_shape, output_pivots', [
    (
     [1, 2,
      3, 4],

     [1, 2,
      0, 1],

     (2, 2),
     [(0, 0), (1, 1)]
    ),

    (
     [1, 2, 3,
      4, 5, 6,
      7, 8, 9],

     [1, 2, 3,
      0, 1, 2,
      0, 0, 0],

     (3, 3),
     [(0, 0), (1, 1)]
    ),

    (
     [2, 1, -3, -10,
      -2, 3, 1, 8,
      7, -2, -4, 6],

     [1, 1/2, -3/2, -5,
      0, 1, -1/2, -1/2,
      0, 0, 1, 51/5],

     (3, 4),
     [(0, 0), (1, 1), (2, 2)]
    ),

    (
     [3, 2, 8, 1, 1,
      3, 1, 5, 6, 3,
      1, 4, 7, 7, 5],

     [1, 2/3, 8/3, 1/3, 1/3,
      0, 1, 3, -5, -2,
      0, 0, 1, -70/17, -2],

     (3, 5),
     [(0, 0), (1, 1), (2, 2)]
    )
])
def test_row_echelon_form(input_matrix: ArrayLike,
                          output_matrix: ArrayLike,
                          matrix_shape: tuple[int, int],
                          output_pivots: list[tuple[int, int]]):
    """
    Tests turning matrices into row_echelon form
    Note: doesn't take into account non-uniqueness of row echelon form
    :param input_matrix: Matrix before row echelon
    :param output_matrix: Matrix after row echelon
    :param matrix_shape: Shape of the matrix
    :param output_pivots: Pivot indices of row echelon matrix
    """
    prec = 10 ** -15

    input_matrix = np.array(input_matrix, dtype=float).reshape(*matrix_shape)
    output_matrix = np.array(output_matrix, dtype=float).reshape(*matrix_shape)
    expected_matrix, pivots = row_echelon_form(input_matrix)

    diff_matrix = expected_matrix - output_matrix
    assert pivots == output_pivots
    assert np.all(np.logical_and(-prec < diff_matrix, diff_matrix < prec))

# TODO: Add more test cases
