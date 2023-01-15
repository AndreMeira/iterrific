from typing import Sequence
from iterrific.base.iter import consume, process
from iterrific.types.functions import Cast
from iterrific.types.common import Stream

Labels = Sequence[str]
GetLabel = Cast[int, Labels]


def label_maker(label: str, modulo: int) -> GetLabel:
    cases = {True: (label,),  False: ()}
    return lambda i: cases[i % modulo == 0]

def labelled(i: int) -> tuple[int, Labels]:
    fizz = label_maker("Fizz", 3)
    buzz = label_maker("Buzz", 5)
    return i, (*fizz(i), *buzz(i))


def render(labelled: tuple[int, Labels]) -> str:
    labels = ''.join(labelled[1]) or ''
    return labels or str(labelled[0])


def main():
    numbers = map(labelled, range(100))
    rendered = map(render, numbers)
    effects = process(rendered, do=print)
    consume(effects)
    