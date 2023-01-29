import random
from collections import Counter


def get_value_freq(pulls: int) -> list[tuple[int, int]]:
    """
    Given the probability of a 5* and number of pulls, finds the frequencies of number of pulls needed to roll a 5*
    :param pulls: Number of pulls
    :return: the frequencies of minimum pulls
    """
    c = Counter()
    for _ in range(pulls):
        i = 1
        pull_sim = pull(p_gen(1))
        while next(pull_sim):
            i += 1
            pull_sim.send(p_gen(i))
        c[i] += 1
    return c.most_common()


def pull(p: float):
    while True:
        if (x := (yield random.random() >= p)) is not None:
            p = x


def p_gen(i: int) -> float:
    """
    Probability generator
    :param i: ith pull
    :return: probability
    """
    return 0.006 if i < 76 else 0.324 if i < 90 else 1


def main():
    random.seed('shirakamifubuki')
    trials = 100_000
    values = get_value_freq(trials)
    print(f'{values=}')
    avg = sum(i * v for i, v in values) / trials
    print(f'{avg=}')


if __name__ == '__main__':
    main()
