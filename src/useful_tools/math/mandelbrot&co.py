from itertools import product
from typing import Generator
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from PIL import Image


def drange(start: float, stop: float, step: float = 1) -> Generator[float, None, None]:
    d = start
    while (d := d + step) < stop:
        yield d


def converges(c: complex, max_iter: int) -> bool:
    z = 0
    i = 0
    while i < max_iter:
        i += 1
        z = z ** 2 + c
        if abs(z) > 4:
            return False
    return True


def display_mandelbrot(x_step: float, y_step: float, max_iter: int) -> str:
    return '\n'.join(''.join('.#'[converges(x+1j*y, max_iter)]
                             for x in drange(-2.1, 0.7+x_step, x_step))
                     for y in drange(-1.12, 1.12+y_step, y_step))


def main():
    # # Naive
    # print(display_mandelbrot(2.8/80, 2.24/24, 100))
    #
    # pixels = numpy_mandelbrot(2800, 2240)
    # np.save('src/useful_tools/storage/mandelbrot/mandelbrot.npy', pixels)
    # noinspection PyTypeChecker
    # pixels = np.load(Path(__file__).parent.parent / 'storage/mandelbrot/mandelbrot.npy')
    #
    # # Matplotlib
    # plt.imshow(pixels, cmap='inferno')
    # plt.show()
    #
    # # PIL
    # img = Image.fromarray(np.uint8(cm.magma(pixels/np.max(pixels)) * 255))
    # img.show()
    ...


def numpy_mandelbrot(width: int, height: int, max_iter: int = 100):
    real = np.linspace(-2.1, 0.7, width).reshape((1, width))
    imag = np.linspace(-1.12, 1.12, height).reshape((height, 1))
    c = real + 1j*imag
    z = np.zeros(c.shape, dtype=np.complex128)
    escape_time = np.zeros(c.shape, dtype=np.int8)
    mask = np.ones(c.shape, dtype=bool)
    for t in range(max_iter):
        z[mask] = np.square(z[mask]) + c[mask]
        escaped = np.greater(np.abs(z), 2, out=np.zeros(c.shape, dtype=bool), where=mask)
        escape_time[escaped] = t
        mask[escaped] = False
    return escape_time


def numpy_julia(width: int, height: int, max_iter: int = 100, bounds=(-2.1, 0.7, -1.12, 1.12)):
    real = np.linspace(*bounds[:2], width).reshape((1, width))
    imag = np.linspace(*bounds[2:], height).reshape((height, 1))
    z = real + 1j*imag
    shape = z.shape
    escape_time = np.zeros(shape, dtype=np.int8)
    mask = np.ones(shape, dtype=bool)
    for t in range(1, max_iter+1):
        z[mask] = z[mask]**2-0.1-0.7j
        escaped = np.greater(np.abs(z), 2, out=np.zeros(shape, dtype=bool), where=mask)
        escape_time[escaped] = t
        mask[escaped] = False
    return escape_time


if __name__ == '__main__':
    main()
    # # pixels = numpy_julia(2800, 2240, 256, bounds=(-2, 2, -2, 2))
    # with open('/storage/temp_numpy_file.npy', 'rb') as f:
    #     # noinspection PyTypeChecker
    #     # np.save(f, pixels)
    #     pixels = np.load(f)
    # new_pixels = np.where((pixels == 0)[:, :, np.newaxis],
    #                       np.array([208, 111, 49, 255]),
    #                       cm.magma(pixels/np.max(pixels)) * 255)
    # img = Image.fromarray(np.uint8(new_pixels))
    # img.show()
