from typing import Any, Callable, Generic, Iterable, TypeVar, overload

from iterrific.wrapper.lbd import Lbd


G = TypeVar("G")
T = TypeVar("T")


class Send(Generic[T]):
    
    # attributes namespace
    value: T
    end = ...
    
    def __init__(self, value: T) -> None:
        self.value = value
    
    @overload
    def __or__(self, func: Callable[[T], G]) -> 'Send[G]': ...
    
    @overload
    def __or__(self, func: 'ellipsis') -> T: ...

    def __or__(self, func: Any) -> Any:
        if func is self.end:
            return self.value
        if func is Stream:
            return Stream(self.value)  # type: ignore
        return Send(func(self.value))
    
    def __rshift__(self, func: Callable[[Any], G]) -> 'Stream[G]':
        return Stream(map(func, self.value))  # type: ignore


M = TypeVar("M")
N = TypeVar("N")


class Stream(Generic[M]):
    
    end = ...
    value: Iterable[M]

    def __init__(self, value: Iterable[M]) -> None:
        self.value = value
        
    @overload
    def __or__(self, func: Callable[[M], N]) -> 'Stream[N]': ...
    
    @overload
    def __or__(self, func: 'ellipsis') -> Iterable[M]: ...
    
    def __or__(self, func: Any) -> Any:
        if func is Lbd.ALL:
            return Send(self.value)
        if func is self.end:
            return self.value
        return Stream(map(func, self.value))
