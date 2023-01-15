from typing import ParamSpec, TypeVar, Callable, Generic

P = ParamSpec('P')
T = TypeVar('T')


class Node(Generic[P, T]):
    operation: Callable[P, T]

    def __init__(self, func: Callable[P, T]):
        self.operation = func

    def exec(self, *args: P.args, **kwargs: P.kwargs) -> T:
        # @fixme support keyword args and all
        return self.operation(*args, **kwargs)
