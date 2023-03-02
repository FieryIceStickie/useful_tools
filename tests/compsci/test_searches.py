import pytest
from itertools import pairwise

from src.useful_tools.compsci.searches import bfs, C, S, delta_abbreviation_dict


@pytest.mark.parametrize('grid,start,end,deltas,bounds,exp_cost', [
    ('''
#####
#...#
###.#
#...#
#####
    ''', 1+1j, 3+1j, '+', None, 6),
    ('''
#####
#...#
###.#
#...#
#####
    ''', 1+1j, 3+1j, '*', None, 4),
    ('''
#####
#...#
#.#.#
#...#
#####
    ''', 1+1j, 3+1j, (1j, -1j, 1+1j, 1-1j), (1, 3, 1, 3), 4),
    ('''
.#.##..
.......
.#.###.
#...#..
..#....
##.##.#
......#
    ''', 0, 6, '*', None, 7),
    ('''
.#.##..
.......
.#.###.
#...#..
..#....
##.##.#
......#
    ''', 0, 6, '+', None, 16),
    ('''
.#.##..
.......
.#.###.
#...#..
..#....
##.##.#
......#
    ''', 0, 6, '+', (0, 6, 0, 4), None)
])
def test_bfs(grid: str, start: complex, end: complex,
             deltas: tuple[C, ...], bounds: tuple[int, int, int, int],
             exp_cost: int):
    node_map = {x+1j*y: v
                for x, row in enumerate(grid.strip().splitlines())
                for y, v in enumerate(row)}
    assert exp_cost == bfs(node_map, start, end, bounds=bounds, deltas=deltas)
    if exp_cost is not None:
        path = bfs(node_map, start, end, bounds=bounds, deltas=deltas, return_path=True)
        assert len(path) == exp_cost
        deltas_as_z = delta_abbreviation_dict.get(deltas, deltas)
        assert all(z2-z1 in deltas_as_z for z1, z2 in pairwise(path))


if __name__ == '__main__':
    pass
