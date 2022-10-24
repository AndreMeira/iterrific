from collections import defaultdict, deque
from enum import Enum
from itertools import count
from typing import List, Callable, Any, MutableMapping, Set, Deque, Iterable, Iterator


class NoOutput(BaseException):
    pass


class CollectorEvent(Enum):
    result = 'result'


class Collector:
    # namespace
    Unsubscribe = Callable[[None], None]

    # attribute types
    Signal = Callable[..., Any]
    Signals = List[Signal]

    output: Signal
    signals: Signals
    queue: Set[Signal]
    replace: Set[Signal]
    sequence: Iterator[int]
    current: MutableMapping[Signal, Any]
    queues: MutableMapping[Signal, Deque[Any]]
    listeners: MutableMapping[CollectorEvent, List[int]]
    handlers: MutableMapping[int, Callable]

    def __init__(self, signals: Signals, output: Signal):
        self.sequence = count()
        self.current = {}
        self.queue = set()
        self.replace = set()
        self.output = output
        self.signals = signals
        self.listeners = defaultdict()
        self.queues = defaultdict(deque)

    def queue_value(self, signals: Iterable[Signal]):
        self.queue.update(signals)

    def replace_value(self, signals: Iterable[Signal]):
        self.queue.update(signals)

    def listen(self, event: CollectorEvent, func: Callable) -> Unsubscribe:
        innerid = next(self.sequence)
        self.handlers[innerid] = func
        self.listeners[event].append(innerid)
        return lambda: self.remove_handler(innerid, event)

    def remove_handler(self, innerid: int, event: CollectorEvent):
        del self.handlers[innerid]
        self.listeners[event].remove(innerid)

    def update(self, signal: Signal, value: Any):
        if signal in self.replace \
        or signal not in self.queue \
        or signal not in self.current:
            self.current[signal] = value
            self.discharge()
            return

        self.queues[signal]\
            .appendleft(value)

    def discharge(self):
        if not self.is_complete():
            return
        try:
            args = self.prepare()
            result = self.output(*args)
            self.forward(result)
        except NoOutput:
            pass
        finally:
            self.current.clear()
            self.recharge()

    def forward(self, result: Any):
        event = CollectorEvent.result
        for innerid in self.listeners[event]:
            self.handlers[innerid](result)

    def is_complete(self):
        sigs = {self.signals}
        charged = {self.current.keys()}
        return sigs == charged

    def prepare(self):
        return [
            self.current[sig]
            for sig in self.signals
        ]

    def recharge(self):
        for signal, queue in self.queues.items():
            self.update(signal, queue.pop())

    def indices(self, signal: Signal):
        return [
            i for i, sig
            in enumerate(self.signals)
            if sig == signal
        ]