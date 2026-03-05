import numpy as np

L = np.array(
    [
        [1, 0, 0, 0, 0],
        [1 / 2, 1, 0, 0, 0],
        [0, 2 / 3, 1, 0, 0],
        [-2 / 3, 1 / 2, 1 / 5, 1, 0],
        [1 / 4, 4 / 5, -1, 0, 1],
    ]
)
U = np.array([[3, 0, 1], [0, -4, 2], [0, 0, 1], [0, 0, 0], [0, 0, 0]])
b = np.array([33, -19 / 2, -61 / 3, -178 / 5, -191 / 20])

print(np.linalg.solve(L, b))

a = np.array([33, -26, -3, 0, 0])

print(L @ a)
print(b)

print(np.linalg.lstsq(U, a))

print(L @ U @ np.array([12, 5, -3]))
