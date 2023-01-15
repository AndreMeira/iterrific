from functools import partial
from typing import Callable, Sequence, TypeAlias
from iterrific.types.functions import Cast
from iterrific.base.iter import consume, process

Label:    TypeAlias = str
GetLabel: TypeAlias = Cast[int, Label]
Match:    TypeAlias = Callable[[int], bool]
Rules:    TypeAlias = Sequence[tuple[Match, GetLabel]]


def divides(i: int, modulo: int) -> bool:
    return i % modulo == 0


def rules() -> Rules:
    return (  # type: ignore[return-value]
        partial(divides, modulo=15), lambda _: 'FizzBuzz',
        partial(divides, modulo=5),  lambda _: 'Buzz',
        partial(divides, modulo=3),  lambda _: 'Fizz',
        partial(divides, modulo=1),  lambda i: str(i),
    )


def rule(i: int, rules: Rules) -> GetLabel:
    return next(
        getlabel for match, getlabel in rules
        if match(i)
    )


def label(i: int, rules: Rules) -> Label:
    getlabel = rule(i, rules=rules)
    return getlabel(i)


def main():
    getlabel = partial(label, rules=rules())
    labels = map(getlabel, range(100))
    effects = process(labels, do=print)
    consume(effects)