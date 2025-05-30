def get_horses():
    with open('umamusume.txt', 'r') as f:
        horses = {horse for horse in f.read().split(',') if horse}
    return horses


def normalize(horse):
    return ''.join(sorted(horse.split(' ')))


def add_horses(new_horses: str):
    horses = get_horses() | {nhorse for horse in new_horses.split(',') if (nhorse := normalize(horse))}
    with open('umamusume.txt', 'w') as f:
        f.write(','.join(sorted(horses)))


def get_pastes():
    horses = get_horses()
    pastes = []
    curr = []
    s = -1
    for horse in sorted(horses):
        s += len(horse) + 1
        if s < 256:
            curr.append(horse)
        else:
            pastes.append(','.join(curr))
            curr = [horse]
            s = len(horse)
    pastes.append(','.join(curr))
    return '\n'.join(pastes)


if __name__ == '__main__':
    add_horses('Haruki Iwata')
    print(get_pastes())