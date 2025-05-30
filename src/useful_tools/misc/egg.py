import json
from collections.abc import Iterator
from enum import StrEnum, auto
from itertools import dropwhile
from operator import itemgetter
from typing import Any, Self

from attrs import evolve, frozen
from frozendict import frozendict
from rich.pretty import pprint
from tqdm.rich import tqdm


class TankError(Exception):
    pass


class Egg(StrEnum):
    TACHYON = auto()
    DILITHIUM = auto()
    ANTIMATTER = auto()
    DARK_MATTER = auto()


type Supply = frozendict[Egg, int]


@frozen
class State:
    tank: Supply
    farm: Egg

    ship: Supply
    tank_size: int

    def __rich_repr__(self) -> Iterator[Any]:
        yield str(self.farm)
        for egg, count in sorted(self.tank.items(), key=lambda s: enum_key[s[0]]):
            yield str(egg), count

    def sim(self) -> tuple[Self, int]:
        tank = {**self.tank}
        num_ships = self.tank_size + 1
        next_farm: Egg | None = None

        for egg, num_needed in self.ship.items():
            if egg == self.farm:
                continue
            potential_num = tank.get(egg, 0) // num_needed
            if potential_num < num_ships:
                num_ships = potential_num
                next_farm = egg
            elif potential_num == num_ships:
                raise TankError(f'Both {egg} and {next_farm} are limited')
        if next_farm is None:
            raise TankError('Only one egg, no switching needed')

        num_ships += 1
        for egg, num_needed in self.ship.items():
            if egg == self.farm:
                continue
            tank[egg] -= num_needed * num_ships
        del tank[next_farm]
        tank[self.farm] = self.tank_size - sum(tank.values())
        return evolve(self, farm=next_farm, tank=frozendict(tank)), num_ships

    def sim_until(self, egg: Egg) -> tuple[Self, int]:
        total_ships = 0
        while True:
            self, num_ships = self.sim()
            total_ships += num_ships
            if self.farm == egg:
                break
        return self, total_ships

    @classmethod
    def from_json(cls, state_json: dict[str, Any], ship: Supply, tank_size: int) -> Self:
        farm = state_json.pop('farm')
        return cls(
            tank=supply(**state_json),
            farm=names_to_enum[farm],
            ship=ship,
            tank_size=tank_size,
        )

    def to_json(self) -> dict[str, Any]:
        return {
            'farm': self.farm,
            **self.tank,
        }


names_to_enum = {
    'tachyon': Egg.TACHYON,
    'dilithium': Egg.DILITHIUM,
    'antimatter': Egg.ANTIMATTER,
    'dark_matter': Egg.DARK_MATTER,
}
enum_key = {
    Egg.TACHYON: 0,
    Egg.DILITHIUM: 1,
    Egg.ANTIMATTER: 2,
    Egg.DARK_MATTER: 3,
}


def supply(**eggs: int) -> Supply:
    return frozendict({names_to_enum[egg]: count for egg, count in eggs.items()})


def iter_start_states(farm: Egg, ship: Supply, tank_size: int) -> Iterator[State]:
    for dilithium in range(1, tank_size + 1):
        for antimatter in range(1, tank_size - dilithium + 1):
            dark_matter = tank_size - dilithium - antimatter
            yield State(
                supply(
                    dilithium=dilithium,
                    antimatter=antimatter,
                    dark_matter=dark_matter,
                ),
                farm,
                ship,
                tank_size,
            )


type StateGraph = dict[State, tuple[State, int]]


def get_viable_states(farm: Egg, ship: Supply, tank_size: int) -> StateGraph:
    rtn: StateGraph = {}
    seen: set[State] = set()
    for state in tqdm(iter_start_states(farm, ship, tank_size), total=124750):
        if state in seen:
            continue
        curr: StateGraph = {}
        try:
            while state not in curr:
                curr[state] = next_state, _ = state.sim_until(farm)
                state = next_state
        except TankError:
            pass
        else:
            rtn |= curr
        seen |= curr.keys()
    return rtn


def save_viable_states(filename: str, viable_states: StateGraph, ship: Supply, tank_size: int):
    with open(filename, 'w') as file:
        print(json.dumps({'ship': ship, 'tank_size': tank_size}), file=file)
        for state, (next_state, num_eggs) in viable_states.items():
            state_json = {'num_eggs': num_eggs, 'state': state.to_json(), 'next_state': next_state.to_json()}
            print(json.dumps(state_json), file=file)


def load_viable_states(filename: str) -> StateGraph:
    rtn: StateGraph = {}
    with open(filename, 'r') as file:
        lines = iter(file)
        header_json = json.loads(next(lines))
        ship: Supply = frozendict(header_json['ship'])
        tank_size: int = header_json['tank_size']
        for line in file.readlines():
            line_json = json.loads(line)
            state_json, next_state_json, num_eggs = itemgetter('state', 'next_state', 'num_eggs')(line_json)
            state = State.from_json(state_json, ship, tank_size)
            next_state = State.from_json(next_state_json, ship, tank_size)
            rtn[state] = next_state, num_eggs
    return rtn


def get_cycles(graph: StateGraph) -> set[tuple[State, ...]]:
    cycles: set[tuple[State, ...]] = set()
    seen: set[State] = set()
    for state in graph:
        if state in seen:
            continue
        curr_chain: dict[State, None] = {state: None}
        curr = state
        found = False
        while True:
            curr, _ = graph[curr]
            if curr in curr_chain:
                break
            elif curr in seen:
                found = True
                break
            curr_chain[curr] = None
        if found:
            continue
        cycles.add(tuple(dropwhile(curr.__ne__, iter(curr_chain))))
        seen |= curr_chain.keys()
    return cycles


def is_normalized(tank: Supply):
    return tank[Egg.DILITHIUM] < tank[Egg.ANTIMATTER] < tank[Egg.DARK_MATTER]


def main():
    ex_hen = supply(tachyon=2, dilithium=6, antimatter=6, dark_matter=6)
    tank_size = 500
    # viable_states = get_viable_states(Egg.TACHYON, ex_hen, tank_size)
    # save_viable_states('storage/egg/viable_states.jsonl', viable_states, ex_hen, tank_size)
    # graph = load_viable_states('storage/egg/viable_states.jsonl')

    # cycles = get_cycles(graph)
    # normalized_cycles = {
    #     cycle for cycle in cycles
    #     if is_normalized(cycle[0].tank)
    # }
    # for i, cycle in enumerate(normalized_cycles, start=1):
    #     print(f'Cycle {i}:')
    #     state = cycle[0]
    #     min_ship = tank_size
    #     curr = state
    #     pprint(state)
    #     while True:
    #         curr, num_ships = curr.sim()
    #         print(num_ships)
    #         pprint(curr)
    #         min_ship = min(min_ship, num_ships)
    #         if curr == state:
    #             break
    #     print(f'{min_ship = }', end='\n'*5)

    start = State(
        supply(tachyon=125, antimatter=125, dark_matter=250),
        Egg.DILITHIUM,
        ex_hen,
        tank_size,
    )
    curr = start
    pprint(curr)
    while True:
        curr, num_ships = curr.sim()
        print(num_ships)
        pprint(curr)
        if curr == start:
            break


if __name__ == '__main__':
    main()
