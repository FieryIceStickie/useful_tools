def max_len(n: int) -> tuple[int, ...]:
    colors = [-1]
    cbest = (-1,)
    palette = [*range(n)]

    def solve(k: int, chosen: int) -> None:
        nonlocal cbest
        print(k, len(cbest))
        disallowed = {colors[i] for i in range(1, (k - 1) // 2 + 1) if colors[i] == colors[k - i]}
        if len(disallowed) == n:
            if len(cbest) < len(colors):
                cbest = tuple(colors)
                with open('bests.txt', 'a') as file:
                    print(len(cbest), cbest, file=file)
            return
        for color in palette:
            if color > chosen:
                return
            if color not in disallowed:
                colors.append(color)
                solve(k + 1, chosen + (color == chosen))
                colors.pop()

    solve(1, 0)
    return cbest


def main():
    best = max_len(4)
    print(len(best), best)


if __name__ == '__main__':
    main()
