import heapq
from collections import deque
from typing import Iterable, TypeVar

C = TypeVar('C', complex, tuple[int, ...])
S = TypeVar('S')


delta_abbreviation_dict = {
        '+': (-1, 1j, 1, -1j),
        '*': (-1-1j, -1, -1+1j, 1j, 1+1j, 1, 1-1j, -1j)
    }


def bfs(node_map: set[C] | dict[C, S], start: C, end: C, *,
        return_path: bool = False,
        bounds: tuple[int, int, int, int] | None = None,
        empty_token: S = '.',
        deltas: str | Iterable[C] = '+'
        ) -> int | list[C]:
    """
    Performs breadth first search on a grid
    :param node_map: Takes either a set of valid points or a dict of coord -> token with empty_token
    :param start: Starting coordinate
    :param end: Ending coordinate
    :param return_path: returns path if True else length of path
    :param bounds:
    :param empty_token: Empty_token if node_map is a dictionary
    :param deltas:
    :return:
    """
    if isinstance(node_map, dict):
        node_map = {k for k, v in node_map.items() if v == empty_token}

    if bounds:
        rmin, rmax, cmin, cmax = bounds
    else:
        rows, cols = zip(*((z.real, z.imag) for z in node_map))
        rmin, rmax, cmin, cmax = min(rows), max(rows), min(cols), max(cols)

    if isinstance(deltas, str):
        deltas = delta_abbreviation_dict[deltas]

    active = deque([(start, () if return_path else 0)])
    visited = set()
    while active:
        current, info = active.popleft()
        if current == end:
            return info
        visited.add(current)
        active.extend((z, info + ((z,) if return_path else 1))
                      for d in deltas
                      if (z := current + d) in node_map
                      and rmin <= z.real <= rmax
                      and cmin <= z.imag <= cmax
                      and z not in visited)


if __name__ == '__main__':
    grid = '''
#####
#...#
#.###
#...#
#####
'''
    grid_dict = {x+1j*y: v for x, row in enumerate(grid.strip().splitlines()) for y, v in enumerate(row)}
    print(grid_dict)
    print(bfs(grid_dict, 1+3j, 3+3j, return_path=True, deltas=(-1j, 1, 1j, 1+1j)))