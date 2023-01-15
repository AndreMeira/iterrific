from functools import partial as _
from typing import Callable, Iterable, TypeVar


T = TypeVar("T")
G = TypeVar("G")


def select(func: Callable[[T], bool]) -> Callable[[Iterable[T]], Iterable[T]]:
    # @FIXME type this correctly
    return _(filter, func) # type: ignore


def transform(func: Callable[[T], G]) -> Callable[[Iterable[T]], Iterable[G]]:
    # @FIXME type this correctly
    return _(map, func) # type: ignore
