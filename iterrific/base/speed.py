import time
from collections.abc import Iterable
from typing import TypeVar

from iterrific.base.iter import every, process

T = TypeVar('T')


def slow(items: Iterable[T], wait: float, cycle: int) -> Iterable[T]:
    stream = every(items=items, cycle=cycle)
    return process(stream, do=lambda _: time.sleep(wait))
