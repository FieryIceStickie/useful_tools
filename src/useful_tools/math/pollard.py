from math import gcd


def f(x: int, n: int) -> int:
    return (pow(2, x, n) + 1) % n


def main():
    q = 17
    n = q * 6871
    print(n)
    a = b = 2

    for i in range(1000):
        print(f'${i}$, ${a}$, ${b}$, ${gcd(a - b, n)}$, ${a % q}$, ${b % q}$', sep=', ', end=',\n')
        if a == b and i:
            break
        a = f(a, n)
        b = f(f(a, n), n)


if __name__ == '__main__':
    main()
