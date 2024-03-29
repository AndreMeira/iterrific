from functools import partial
from typing import Callable, Concatenate, ParamSpec, TypeVar
from iterrific.types.common import Stream


SRC = TypeVar('SRC')
DST = TypeVar('DST')
P = ParamSpec('P')
Rest = ParamSpec('Rest')
SplitableParams = Concatenate[Stream[SRC], Rest]


def bindable(func: Callable[P, Stream[DST]]) -> Callable[P, Stream[DST]]:
    def bind(
        func: Callable[Concatenate[Stream[SRC], Rest], Stream[DST]], 
        *args: Rest.args, **kwargs: Rest.kwargs
    ) -> Callable[[Stream[SRC]], Stream[DST]]:
        return partial(func, *args, **kwargs)
    setattr(func, 'bind', bind)
    return func
