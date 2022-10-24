from collections import deque
from collections.abc import Sequence
from itertools import pairwise, chain, islice, compress
from typing import List, TypeVar, Callable, Iterable, Any, Union, Tuple

T = TypeVar('T')
Stream = Iterable[T]
Check = Callable[[T], bool]
Cutter = Callable[[T, T], bool]
Merge = Callable[[Sequence[T, T]], bool]
Keep = Callable[[Sequence[T, T]], Tuple[bool, bool]]
ChunkedStream = Iterable[Sequence[T]]


def iterate(items: Stream[T]) -> Stream[T]:
    for item in items:
        yield item


def cycle(items: Stream[T]) -> Stream[T]:
    while True:
        yield from iterate(items)


def indices(items: Stream[T], check: Check[T]) -> Iterable[int]:
    return (i for i, item in enumerate(items) if check(item))


def merge(items: Stream[T], collapse: Merge[T]) -> Stream[T]:
    stream = iter(items)
    last = next(stream)
    for item in stream:
        if not collapse(last, item):
            yield last
            last = item
    yield last


def keep(items: Stream[T], select: Keep[T]) -> Stream[T]:
    stream = iter(items)
    last = next(stream)
    for item in stream:
        match select(last, item):
            case (int(1), int(1)):
                yield last
                last = item
            case (int(0), int(1)):
                last = item
            case (int(0), int(0)):
                last = next(stream)
            case _: continue
    yield last


def following(items: Stream[T], check: Check[T], ahead: int = 1) -> Stream[T]:
    countdown = -1
    for item in items:
        if countdown == 0:
            yield item
            countdown = -1
        if check(item):
            countdown = ahead
        if countdown:
            countdown -= 1


def previous(items: Iterable[T], check: Check[T], ahead: int = 1):
    buffer = deque(islice(items, 0, ahead), maxlen=ahead)
    for item in islice(items, ahead, None):
        if check(item):
            yield buffer[0]
        buffer.append(item)


def every(items: Iterable[T], cycle: int, do: Callable[[T], Any]) -> Iterable[T]:
    count = 0
    for item in items:
        yield item
        count += 1
        if count % cycle == 0:
            count = 0
            do(item)


def cut(stream: Stream[T], cutter: Cutter[T]) -> ChunkedStream[T]:
    return cutiter(stream, cutter)


def cutiter(stream: Stream[T], cutter: Cutter[T]) -> ChunkedStream[T]:
    chunk: List[T] = []
    streaming: Union[Stream[T], Stream[object]]
    streaming = chain(stream, [endofstream := object()])
    
    for head, tail in pairwise(streaming):
        chunk.append(head)  # type: ignore[type-var]
        if (tail is not endofstream 
            and cutter(head, tail)): # type: ignore[type-var]
            yield chunk
            chunk = []
    yield chunk


def cutsequence(stream: Sequence[T], cutter: Cutter[T]) -> ChunkedStream[T]:
    length = len(stream)

    breakpoints = chain([0], (
        i + 1 for i in range(length - 2)
        if cutter(*stream[i:i+2])
    ), [length])

    return (stream[slice(*s)] for s in pairwise(breakpoints))