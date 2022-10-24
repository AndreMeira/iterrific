from dataclasses import dataclass
from datetime import datetime
from typing import Set


@dataclass
class TimestampTick:
    tick: datetime


@dataclass
class Tick:
    tick: int


class TicTac:
    """
    This Class represent a lazy tick clock
    It doesn't produce all ticks
    But only the ones that it is fed with.
    It never produces a tick that is in the past.
    By default it produces the tick 0.
    clock = TicTac()
    next(clock)  # 0
    ...
    clock.add(1)
    clock.add(5)
    next(clock)  # 1
    next(clock)  # 5
    ...
    clock.add(5)
    clock.add(9)
    next(clock)  # 9
    ...
    clock.add(8)
    next(clock)  # throw StopIteration
    """

    now: int
    events: Set[int]

    def __init__(self):
        self.events = {0}

    def add(self, tick: int):
        if tick > self.now:
            self.events.add(tick)

    def __next__(self) -> Tick:
        try:
            current = min(self.events)
            self.events.remove(current)
            return Tick(current)
        except KeyError:
            raise StopIteration

    def __iter__(self):
        return self


class Timestamped:
    """
    This Class represent a lazy wall clock
    It doesn't produce all datetimes
    But only the ones that it is fed with.
    It never produces a tick that is in the past.
    now = datetime.now()
    clock = Timestamped(now)
    next(clock)  # 0
    ...
    clock.add(now + timedelta(second=2))
    clock.add(now + timedelta(second=3))
    next(clock)  # now + timedelta(second=2)
    next(clock)  # now + timedelta(second=3)
    ...
    clock.add(now + timedelta(second=3))
    clock.add(now + timedelta(second=4))
    next(clock)  # # now + timedelta(second=4)
    next(clock)  # throw StopIteration
    """
    events: Set[datetime]
    now: datetime

    def __init__(self, start: datetime):
        self.events = {start}

    def add(self, date: datetime):
        if date > self.now:
            self.events.add(date)

    def __next__(self) -> TimestampTick:
        try:
            current = min(self.events)
            self.events.remove(current)
            return TimestampTick(current)
        except KeyError:
            raise StopIteration

    def __iter__(self):
        return self
