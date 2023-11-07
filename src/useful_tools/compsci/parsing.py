from typing import Iterator, Mapping
from collections import defaultdict
import re


def shunting_yard_polynomial(
        inp: str,
        num_regex: str,
        /,
        namespace: Mapping[str, str] | None = None
) -> Mapping[int, str]:
    """
    Uses the shunting yard algorithm to evaluate a polynomial string
    :param inp:
    :param num_regex:
    :param namespace:
    :return:
    """
    namespace = namespace or {}

    tokens = re.iter(fr'({re.escape(num_regex)}|)')




if __name__ == '__main__':
    pass