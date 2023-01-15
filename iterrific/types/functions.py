from typing import Callable, Iterable, Sequence, TypeAlias, TypeVar

from iterrific.types.common import Chunked, Stream


T = TypeVar('T')
G = TypeVar('G')

Source: TypeAlias = Callable[[], G]

# Classic Unary function
Cast:      TypeAlias = Callable[[T], G]
Reduce:    TypeAlias = Callable[[Iterable[T]], G]
Spread:    TypeAlias = Callable[[T], Sequence[G]]
Broadcast: TypeAlias = Callable[[Iterable[T]], Iterable[G]]

# Operators
Next:    TypeAlias = Callable[[T], T]
Fold:    TypeAlias = Callable[[T, T], T]
Unfold:  TypeAlias = Callable[[T], Sequence[T]]
Flatten: TypeAlias = Callable[[Chunked[T]], Stream[T]]