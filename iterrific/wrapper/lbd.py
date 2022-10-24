from functools import partial as _
from operator import itemgetter
from typing import Any, Callable, Optional, TypeVar, Union, Iterable

T = TypeVar("T")
G = TypeVar("G")


class Lbd:
    ALL = object()
    
    # @FIXME type me correctly
    operation: Callable[..., Any]
    
    def __init__(self, op: Optional[Callable[..., Any]] = None) -> None:
        self.operation = op or type(self).identity()

    def unwrap(self):
        return self.operation
    
    def __add__(self, y: Union[Any, 'Lbd']) -> 'Lbd':
        return type(self)(
            lambda x: 
            self(x) + type(self).cast(y)(x)
        )

    def __radd__(self, y: Union[Any, 'Lbd']) -> 'Lbd':
        return type(self)(
            lambda x:
            type(self).cast(y)(x) + self(x)
        )
    
    def __sub__(self, y: Union[Any, 'Lbd']) -> 'Lbd':
        return type(self)(
            lambda x:
            self(x) - type(self).cast(y)(x)
        )

    def __rsub__(self, y: Union[Any, 'Lbd']) -> 'Lbd':
        return type(self)(
            lambda x:
            type(self).cast(y)(x) - self(x)
        )
        
    def __mul__(self, y: Union[Any, 'Lbd']) -> 'Lbd':
        return type(self)(
            lambda x: 
            self(x) * type(self).cast(y)(x)
        )

    def __rmul__(self, y: Union[Any, 'Lbd']) -> 'Lbd':
        return type(self)(
            lambda x:
            type(self).cast(y)(x) * self(x)
        )
        
    def __div__(self, y: Union[Any, 'Lbd']) -> 'Lbd':
        return type(self)(
            lambda x: 
            self(x) / type(self).cast(y)(x)
        )

    def __rdiv__(self, y: Union[Any, 'Lbd']) -> 'Lbd':
        return type(self)(
            lambda x:
            type(self).cast(y)(x) / self(x)
        )
        
    def __pow__(self, y: Union[Any, 'Lbd']) -> 'Lbd':
        return type(self)(
            lambda x: 
            self(x) ** type(self).cast(y)(x)
        )

    def __rpow__(self, y: Union[Any, 'Lbd']) -> 'Lbd':
        return type(self)(
            lambda x:
            type(self).cast(y)(x) ** self(x)
        )
    
    def __gt__(self, y: Any) -> 'Lbd':
        return type(self)(
            lambda x: 
            self(x) > type(self).cast(y)(x)
        )
    
    def __lt__(self, y: Any) -> 'Lbd':
        return type(self)(
            lambda x: 
            self(x) < type(self).cast(y)(x)
        )
    
    def __ge__(self, y: Any) -> 'Lbd':
        return type(self)(
            lambda x: 
            self(x) >= type(self).cast(y)(x)
        )
    
    def __le__(self, y: Any) -> 'Lbd':
        return type(self)(
            lambda x: 
            self(x) <= type(self).cast(y)(x)
        )
    
    def __eq__(self, y: Any) -> 'Lbd': #type: ignore
        return type(self)(
            lambda x: 
            self(x) == type(self).cast(y)(x)
        )
        
    def __rshift__(self, y: 'Lbd') -> 'Lbd':
        return type(self)(_(map, y))  # type: ignore
    
    def __getitem__(self, key: Any) -> Any:
        # @FIXME correct type please
        if key is ...:
            return self.ALL
        if isinstance(key, Callable):
            f = _(filter, key)
            return type(self)(f)
        return type(self)(
            itemgetter(key)
        )
    
    def __call__(
        self,
        *args: Any,
        **kwargs: Any
    ) -> Any:
        return self.operation(*args, **kwargs)
    
    @staticmethod
    def identity() -> Callable[[T], T]:
        return lambda x: x
    
    @staticmethod
    def value(x: T) -> Callable[..., T]:
        return lambda *a, **k: x
    
    @classmethod
    def cast(cls, x: Any) -> 'Lbd':
        return x if isinstance(x, cls) \
            else cls(cls.value(x))


class LbdWrapper:

    def __getitem__(
        self,
        func: Callable[[T], G]
    ) -> Callable[[Lbd], Lbd]:
        lbd = Lbd(func)
        return lambda x: Lbd(lambda y: lbd(x(y)))

    def __setitem__(
        self,
        symbol: Callable[..., T],
        func: Callable[[T], G]
    ) -> Lbd:
        return Lbd(lambda x: func(symbol(x)))


class PartialWrapper:

    def __getitem__(
        self,
        func: Callable[..., G]
    ) -> Callable[..., Lbd]:
        return lambda *args: Lbd(lambda x: func(
            *type(self).evaluate(args, x)
        ))

    @staticmethod
    def evaluate(
        args: Iterable[Any],
        value: Any
    ) -> Iterable[Any]:
        arguments = []
        for arg in args:
            if isinstance(arg, Lbd):
                arg = arg(value)
            arguments.append(arg)
        return arguments

