from functools import cache


@cache
def max_len_of_seq(searches: int, targets: int) -> int | float:
    """Solves the problem of
    Find the largest N such that given an array of N items and
    m target items, we can always find m target items in at most
    n searches

    Args:
        searches: n
        targets: m

    Returns:
        N
    """
    if targets == 0:
        # No targets means array can be as large as we want
        print(f'{searches} {targets} is inf')
        return 50000
    if searches == 0:
        # If we can't query anything, then m == N
        # Unless we have no targets, which is covered above
        print(f'{searches} {targets} is {targets}')
        return targets
    # If we search and get a correct answer, then we're searching
    # an array that is smaller by 1 element with 1 less search and
    # 1 less target, since we can adjust future results with our known
    # number to ignore it
    best_len = max_len_of_seq(searches - 1, targets - 1) + 1
    # Otherwise, we get (k, m - k) as an answer
    for left_targets in range(targets + 1):
        right_targets = targets - left_targets
        # Given (k, m - k) as the answer, find the best array
        best_len_given_answer = 0
        # We allocate some number of searches for the left which maximizes the array
        for left_searches in range(searches):
            right_searches = searches - 1 - left_searches
            print(f'{searches} {targets} ({left_searches}, {right_searches}) ({left_targets}, {right_targets})')
            max_len = (
                1
                + max_len_of_seq(left_searches, left_targets)  #
                + max_len_of_seq(right_searches, right_targets)
            )
            best_len_given_answer = max(best_len_given_answer, max_len)
        best_len = min(best_len, best_len_given_answer)
    print(f'{searches} {targets} = {best_len}')
    return best_len
    # [0, 1]


def main():
    print(max_len_of_seq(1, 1))
    print(max_len_of_seq(4, 2))


if __name__ == '__main__':
    main()
