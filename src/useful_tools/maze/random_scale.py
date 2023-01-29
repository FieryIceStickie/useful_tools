import random


def random_scale(amount: int) -> list:
    """
    Provides a specified number of musical scales
    :param amount: Amount of scales to request
    :return: A list of tuples of (note, key)
    """
    scale_list = []
    while len(scale_list) != amount:
        note = random.choice(['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'])
        key = random.choice(['Major', 'Minor'])
        if key == 'Minor':
            key = random.choice(['Harmonic', 'Melodic']) + ' ' + key
        if (note, key) not in scale_list:
            scale_list.append((note, key))
    return scale_list


def scale_print(scale_list: list) -> None:
    """
    Prints the scales provided by random_scale with modifiers
    :param scale_list: The output of random_scale
    """
    for i in scale_list:
        method = random.choice(['Tongued', 'Slurred'])
        print(f'{i[0]} {i[1]}, {method}')


if __name__ == '__main__':
    pass
