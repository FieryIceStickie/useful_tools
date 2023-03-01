from collections import deque
import heapq
from typing import TypeVar

C = TypeVar('C', complex, tuple[int, ...])
S = TypeVar('S')


def bfs(node_map: set[C] | dict[C, S], start: C, end: C, *,
        return_path: bool = False,
        bounds: tuple[int, int, int, int] | None = None,
        empty_val: S = '.',
        deltas: str | tuple[C] = '+'
        ) -> int | list[C]:
    if isinstance(node_map, dict):
        node_map = {k for k, v in node_map.items() if v == empty_val}

    if bounds:
        rmin, rmax, cmin, cmax = bounds
    else:
        rows, cols = zip(*((z.real, z.imag) for z in node_map))
        rmin, rmax, cmin, cmax = min(rows), max(rows), min(cols), max(cols)

    match deltas:
        case '+':
            deltas = (-1, 1j, 1, -1j)
        case '*':
            deltas = (-1-1j, -1, -1+1j, 1j, 1+1j, 1, 1-1j, -1j)
        case (*deltas,):
            pass
        case unknown:
            raise ValueError(f"{unknown} of type {type(unknown)} is not valid for parameter 'deltas'")

    active = deque([(start, () if return_path else 0)])
    visited = set()
    while active:
        current, info = active.popleft()
        if current == end:
            return (*info, end) if return_path else info
        visited.add(current)
        active.extend((z, (*info, current) if return_path else info + 1)
                      for d in deltas
                      if (z := current + d) in node_map
                      and rmin <= z.real <= rmax
                      and cmin <= z.imag <= cmax
                      and z not in visited)


if __name__ == '__main__':
    grid = '''#####
#...#
#.###
#...#
#####'''
    grid_dict = {x+1j*y: v for x, row in enumerate(grid.splitlines()) for y, v in enumerate(row)}
    print(grid_dict)
    print(bfs(grid_dict, 1+3j, 3+3j, return_path=False, deltas=(-1j, 1+0j, 1j, 1+1j)))