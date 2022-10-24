import time
from abc import ABC
from collections.abc import Iterable
from typing import TypeVar, SupportsFloat

from iterrific.base.iter import every

T = TypeVar('T')
class Second(SupportsFloat, ABC):...


def slow(items: Iterable[T], wait: Second, cycle: int) -> Iterable[T]:
    return every(items, cycle, do=lambda _: time.sleep(float(wait)))

def c(x:int, y:int): return True
