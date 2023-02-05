import numpy as np


def row_echelon_form(m: np.ndarray, /) -> tuple[np.ndarray, list[tuple[int, int]]]:
    """
    Performs Gaussian elimination downwards on the given matrix to reduce it into row echelon form
    Note: leaves the matrix with rows that have leading 1s
    :param m: Input matrix
    :return: Matrix in row echelon form, pivot_indices
    """
    m = m.astype(float)
    pivot_indices: list[tuple[int, int]] = []
    row, col = 0, 0
    rows, cols = m.shape
    while row < rows and col < cols:
        try:
            nonzero_row = row + m[row:, col].nonzero()[0][0]
        except IndexError:
            col += 1
            continue
        if nonzero_row != row:
            m[[row, nonzero_row]] = m[[nonzero_row, row]]
        m[row] /= m[row, col]
        m[row + 1:, col:] -= m[row + 1:, col:col + 1] * m[row, col:]
        pivot_indices.append((row, col))
        row += 1
        col += 1
    return m, pivot_indices


def reduced_row_echelon_form(m: np.ndarray, /) -> tuple[np.ndarray, list[tuple[int, int]]]:
    """
    Performs Gaussian elimination on a matrix to reduce it to reduced row echelon form
    :param m: Input matrix
    :return: Matrix in reduced row echelon form, pivot_indices
    """
    m, pivot_indices = row_echelon_form(m)
    for row, col in reversed(pivot_indices):
        m[:row, col:] -= m[:row, col:col + 1] * m[row, col:]
    return m, pivot_indices


if __name__ == '__main__':
    x = np.array(
        [1, 2, 0, 7,
         6, -1, 2, 0,
         -3, 0, -1, -3]
    ).reshape(3, 4)
    print(x)
    x, indices = reduced_row_echelon_form(x)
    print(x, indices)
