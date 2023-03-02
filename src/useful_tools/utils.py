from os import PathLike
from pathlib import Path


def src_path() -> PathLike:
    return Path(__file__).parent.parent
