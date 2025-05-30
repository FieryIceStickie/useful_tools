from typing import Self, override
from attrs import evolve, frozen

colors = {
    "black": 0,
    "red": 1,
    "green": 2,
    "yellow": 3,
    "blue": 4,
    "purple": 5,
    "cyan": 6,
    "white": 7,
}


@frozen
class Color:
    is_bold: int = 0
    color: int = 30

    def __getattr__(self, key: str) -> Self | str:
        match key:
            case "clear":
                return "\x1b[0m"
            case "bold":
                return evolve(self, is_bold=1)
            case "hi":
                return evolve(self, color=self.color + 60)
            case color if color in colors:
                return evolve(self, color=self.color + colors[color])
            case _:
                raise KeyError

    @override
    def __str__(self) -> str:
        return f"\x1b[{self.is_bold};{self.color}m"


c = Color()

if __name__ == "__main__":
    print(repr(
        f'{c.bold.yellow}[{c.blue}%(asctime)s'
        f'{c.bold.white}|{c.cyan}%(name)s'
        f'{c.bold.yellow}]{c.bold.white}:{c.hi.green}%(levelname)s'
        f'{c.bold.white}: {c.clear}%(message)s'
    ).replace(r'\x1b', r'\u001b').replace("'", '"'))
