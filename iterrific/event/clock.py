from datetime import datetime
from itertools import count
from typing import Generator, Optional

from iterrific.event.lazy import Tick, TimestampTick, Timestamped as TimestampedClock


def monotonic() -> Generator[Tick, None, None]:
    seq = count()
    while True:
        yield Tick(next(seq))


def timestamp(
    start: Optional[datetime] = None
) -> Generator[TimestampTick, None, None]:
    clock = TimestampedClock(start or datetime.now())
    while True:
        yield next(clock)
