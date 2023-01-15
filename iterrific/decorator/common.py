from typing import TypeAlias, TypeVar
from iterrific.base.iter import Check, router
from iterrific.types.common import Stream
from iterrific.types.functions import Cast, Source


T = TypeVar('T')
G = TypeVar('G')
Routes: TypeAlias = Stream[tuple[Check[T], Cast[T, G]]]


def case(func: Source[Routes[T, G]]) -> Cast[T, G]:
    return router(func())