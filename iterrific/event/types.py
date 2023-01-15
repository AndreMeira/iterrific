from datetime import datetime
from typing import Protocol, TypeVar


T = TypeVar('T', covariant=True)


class TickProtocol(Protocol):
    tick: int


class TimestampedTickProtocol(Protocol[T]):
    tick: datetime
