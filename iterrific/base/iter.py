import operator
from collections import deque
from collections.abc import Callable
from collections.abc import Sequence
from itertools import pairwise, chain, islice
from typing import TypeVar, Iterable, Any, Union, Tuple, ParamSpec, TypeAlias


from iterrific.types.common import Stream
from iterrific.types.functions import Cast


T = TypeVar('T')
G = TypeVar('G')
Check:    TypeAlias = Callable[[T], bool]
Select:   TypeAlias = Callable[[Tuple[T, T]], Tuple[bool, bool]]
Collapse: TypeAlias = Callable[[T, T], bool]
Cutter:   TypeAlias = Callable[[T, T], bool]
Params = ParamSpec('Params')


def force_bool(func: Callable[Params, Any]) -> Callable[Params, bool]:
    return lambda *args, **kwargs: bool(func(*args, **kwargs))


def consume(stream: Stream[T]) -> None:
    list(stream) 


def indices(items: Stream[T], check: Check) -> Stream[int]:
    return (i for i, item in enumerate(items) if check(item))


def router(rules: Stream[tuple[Check[T], Cast[T, G]]]) -> Cast[T, G]:
    def handler(request: T) -> G:
        handler = next(handler for match, handler in rules if match(request))
        return handler(request)
    return handler


def distinct(items: Stream[T], collapse: Collapse[T] = force_bool(operator.eq)) -> Stream[T]:
    try:
        stream = iter(items)
        current = next(stream)
        for item in stream:
            if collapse(current, item):
                continue
            yield current
            current = item
        yield current
    except StopIteration:
        return


def keep(items: Stream[T], select: Select[T]) -> Stream[T]:
    stream = iter(items)
    last = next(stream)
    for item in stream:
        match select((last, item)):
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
        if countdown >= 0:
            countdown -= 1
        if check(item):
            countdown = ahead


def previous(items: Stream[T], check: Check[T], ahead: int = 1):
    buffer = deque(islice(items, 0, ahead), maxlen=ahead)
    for item in islice(items, ahead, None):
        if check(item):
            yield buffer[0]
        buffer.append(item)


def every(items: Stream[T], cycle: int) -> Stream[T]:
    filtr = lambda i: (i + 1) % cycle == 0
    return (item for i, item in enumerate(items) if filtr(i))


def process(items: Stream[T], do: Callable[[T], Any]) -> Stream[T]:
    handler = lambda item: (item, do(item))[0]
    return (handler(item) for item in items)


def cut(stream: Stream[T], cutter: Cutter[T]) -> Iterable[Sequence[T]]:
    return cutiter(stream, cutter)


def cutiter(stream: Stream[T], cutter: Cutter[T]) -> Iterable[Sequence[T]]:
    chunk: Sequence[T] = tuple()
    streaming: Union[Stream[T], Iterable[object]]
    streaming = chain(stream, [endofstream := object()])

    for head, tail in pairwise(streaming):
        chunk = (*chunk, head)  # type: ignore[arg-type]
        if tail is endofstream:
            yield chunk
            return
        if cutter(head, tail):  # type: ignore[arg-type]
            yield chunk
            chunk = []
