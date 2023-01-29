import numpy as np


def naive_tribonacci(n: int) -> list[int]:
    tribonacci_seq = [0, 0, 1]
    for _ in range(n-1):
        tribonacci_seq.append(sum(tribonacci_seq[-3:]))
    return tribonacci_seq


if __name__ == '__main__':
    print(naive_tribonacci(10))
    # [0, 0, 1, 1, 2, 4, 7, 13, 24, 44, 81, 149]
