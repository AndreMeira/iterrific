from itertools import cycle
from typing import Callable, Iterable, Sequence, TypeAlias, TypeVar


T = TypeVar('T')

Stream:   TypeAlias = Iterable[T]
Chunked:  TypeAlias = Stream[Sequence[T]]
Infinite: TypeAlias = Stream[T]  # alias to signify a infinite stream
infinite: Callable[[Stream[T]], Infinite[T]] = cycle
