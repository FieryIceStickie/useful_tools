# Decorator that validates type hints
# like
# @check_type
# def foo(s: int, a: list[str]) -> tuple[str, int]:
#     ...
# would check at runtime that
# isinstance(s, int),
# isinstance(a, list) and all(isinstance(i, str) for i in a)
# isinstance(rtn, tuple) and isinstance(rtn[0], str) and instance(rtn[1], int)