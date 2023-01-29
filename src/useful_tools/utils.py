from pathlib import Path
from os import PathLike


def src_path() -> PathLike:
    return Path(__file__).parent.parent
