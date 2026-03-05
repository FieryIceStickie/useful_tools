import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt


def k1(s: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    return 1 - np.cos(s)


def k2(s: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    return s**2 / 2 + 1 - np.cos(s)


def k3(s: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    return -s * np.cos(s) + np.sin(s)


def k4(s: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    return -(s**2) * np.cos(s) + 2 * s * np.sin(s) + 2 * np.cos(s) - 2


def main():
    for name, k in [
        ('sin_s', k1), 
        ('s+sin_s', k2), 
        ('s*sin_s', k3), 
        ('s^2*sin_s', k4), 
    ]:
        make_fig(f'{name}.png', k, 50, 64)

def make_fig(filename: str, k, end: int, n_points: int):
    """

    Args:
        k (): integral of signed curvature (K in doc)
        filename: filename
        end: plot curve over [-end, end]
        n_points: number of points to sample for each interval [n, n+1] 
    """
    s_values = np.linspace(0, end, n_points * end, dtype=np.float64)
    ds = 1 / n_points
    x_pos = np.cumsum(-np.sin(k(s_values)) * ds)
    x_pos = np.concatenate([[0], x_pos])
    y_pos = np.cumsum(np.cos(k(s_values)) * ds)
    y_pos = np.concatenate([[0], y_pos])
    x_neg = x_pos if k == k3 else -x_pos
    y_neg = -y_pos

    fig, ax = plt.subplots()
    ax.plot(x_pos, y_pos, color='orangered', label=r'$s\ge0$')
    ax.plot(x_neg, y_neg, color='deepskyblue', label=r'$s\le0$')
    ax.set_aspect('equal')

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    plt.show()



if __name__ == '__main__':
    main()
