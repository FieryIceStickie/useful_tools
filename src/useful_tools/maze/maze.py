from collections import deque
from itertools import cycle, product
from typing import Iterator, Sequence

import numpy as np
from PIL import Image, ImageDraw


def quantize_img(raw_img_arr: np.ndarray) -> np.ndarray:
    """
    Turns all pixels in the image to either black or white
    :param raw_img_arr: Raw array of RGB values of the image
    :return: Array of black and white values of the image
    """
    quantized_img_arr = raw_img_arr / 255
    quantized_img_arr = np.around(quantized_img_arr)
    quantized_img_arr *= 255
    quantized_img_arr = quantized_img_arr.astype(int)
    return quantized_img_arr


def get_pixel_array(img_arr: np.ndarray, row_idx: tuple[int], col_idx: tuple[int]) -> np.ndarray:
    """
    Turns the pixels of the image into pixels of the maze
    :param img_arr: Quantized array of black and white values of the image
    :param row_idx: Indices for row pixels of the maze
    :param col_idx: Indices for col pixels of the maze
    :return: Boolean array of maze pixels (True is wall, False is path)
    """
    shape = len(row_idx), len(col_idx)
    rows, cols = zip(*product(row_idx, col_idx))

    pixel_arr = np.invert(np.any(img_arr, axis=2))
    pixel_arr = pixel_arr[np.array(rows), np.array(cols)].reshape(shape)
    return pixel_arr


def truncate_pixel_arr(pixel_arr: np.ndarray, bottom_padding: int, right_padding: int) -> np.ndarray:
    """
    Truncates any whitespace pixels outside the maze
    :param bottom_padding: Number of pixels needed to be truncated on the bottom
    :param right_padding: Number of pixels needed to be truncated on the right
    :param pixel_arr: Pixel array
    :return: Truncated pixel array with no pixels outside border of maze
    """
    return pixel_arr[:-bottom_padding, :-right_padding]


def bfs(pixel_arr: np.ndarray, start: complex, end: complex) -> tuple[complex]:
    """
    Breadth first search
    :param pixel_arr: Boolean array of pixels
    :param start: Starting index written in complex form
    :param end: End index written in complex form
    :return: Tuple of complex numbers corresponding to the shortest path through the maze
    """
    visited = {start}
    active: deque[tuple[complex, ...]] = deque([(start,)])
    try:
        while True:
            path = active.popleft()
            if (current_node := path[-1]) == end:
                break
            candidates: list[complex] = []
            for d in (-1, 1j, 1, -1j):
                new_node = current_node + d
                if new_node in visited:
                    continue
                try:
                    if pixel_arr[ctt(new_node)]:
                        continue
                except IndexError:
                    continue
                candidates.append(new_node)
                visited.add(new_node)
            active.extend(path + (node,) for node in candidates)
    except IndexError as e:
        print('No path found to exit.')
        raise e
    return path


def ctt(z: complex, /) -> tuple[int, int]:
    """
    Complex To Tuple
    a and b are integers
    :param z: a+bi
    :return: (a, b)
    """
    return int(z.real), int(z.imag)


def display(arr: np.ndarray):
    """
    Displays a pixel array with # being walls and . being paths
    :param arr: Pixel array
    """
    print('\n'.join(''.join('#' if elem else '.' for elem in row) for row in arr))


def path_display(arr: np.ndarray, path: tuple[complex, ...]):
    """
    Displays a pixel array with '#' being walls and '.' being paths, as well as ' ' for a certain path
    :param arr: Pixel array
    :param path: Given path to display
    """
    print('\n'.join(
        ''.join(' ' if complex(row, col) in path else ('#' if elem else '.')
                for col, elem in enumerate(line)
                ) for row, line in enumerate(arr)))


def alternating_range(start: int, stop: int, steps: Sequence[int] = (1,)) -> Iterator[int]:
    """
    Like range() but with alternating steps
    :param start: Starting number
    :param stop: Ending number
    :param steps: Tuple of steps to cycle through
    :return: Generator
    """
    step = cycle(steps)
    val = start
    while val < stop:
        yield val
        val += next(step)


def main():
    raw_img = Image.open('../storage/maze/maze.png')
    # noinspection PyTypeChecker
    raw_img_arr = np.array(raw_img)
    raw_img_arr = raw_img_arr[:, :, :3]  # Only RGB values, not RGBA
    quantized_img_arr = quantize_img(raw_img_arr)

    # Top left maze pixel's midpoint = (15, 22)
    # Bottom right maze pixel's midpoint = (620, 513)
    row_idx = tuple(alternating_range(15, 620, (7, 6, 6, 7, 6)))
    col_idx = tuple(alternating_range(22, 513, (7, 6, 6, 7, 6)))
    pixel_arr = get_pixel_array(quantized_img_arr, row_idx, col_idx)
    pixel_arr = truncate_pixel_arr(pixel_arr, 1, 2)

    # Start = 93, 65
    # End = 93, 61
    path = bfs(pixel_arr, 93+65j, 93+61j)
    idx_path = [ctt(i) for i in path]
    pixel_loc = [(row_idx[i], col_idx[j]) for i, j in idx_path]

    draw = ImageDraw.Draw(raw_img)
    # ImageDraw uses reversed coordinates for some reason
    draw.line([(j, i) for i, j in pixel_loc], fill=(255, 0, 0), width=3)
    raw_img.save('Completed Maze.png')


def foo():
    x = 1
    while x:
        if x:
            return




if __name__ == '__main__':
    main()
