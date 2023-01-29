from typing import Callable

from attrs import define

inputs = map(str, [1, 3.1415, -12, 1729, 'hello world', 0x603b5, 1+0j, 3, 'END', 10])
def input(_): return print(str(_), w:=next(inputs)) or w


@define(str=False)
class Message:
    msg: str

    def __str__(self):
        return self.msg


@define(eq=False)
class Verify:
    msg: Message
    fn: Callable[[str, Message], bool]

    def __eq__(self, other: str):
        return self.fn(other, self.msg)


def check_end(inp: str, msg: Message) -> bool:
    msg.msg = ['Invalid number, please try again: ', 'Enter another one: '][inp.isnumeric()]
    return inp.lower() in ('', 'stop', 'exit', 'end')


m = Message('Enter numbers: ')
numbers = [int(w) for w in iter(lambda: input(m), Verify(m, check_end)) if w.isnumeric()]
print(numbers)
