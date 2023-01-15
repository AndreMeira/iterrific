from typing import Iterable, TypeVar

from iterrific.deprecated.lbd import Lbd, LbdWrapper
from iterrific.deprecated.range import Rng
from iterrific.deprecated.send import Send as _S, Stream as _ST
from iterrific.deprecated.func import Function, Exp, Partial

X = Lbd()
R = Rng()
F = Function
P = Partial
T = TypeVar("T")


def send(value: T) -> _S[T]:
    return _S(value)


def stream(value: Iterable[T]) -> _ST[T]:
    return _ST(value)
