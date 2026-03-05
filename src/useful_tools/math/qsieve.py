from math import gcd, floor, sqrt


def main():
    n = 1649
    q = floor(sqrt(n))
    m = 3

    x = [*range(q - m, q + m + 1)]
    y = [i ** 2 - n for i in x]
    print(*(f'${i}$'for i in x),sep=', ' )


if __name__ == '__main__':
    main()
