from typing import Any, Callable, Iterable, TypeVar

SRC = TypeVar('SRC')
MID = TypeVar('MID')
DST = TypeVar('DST')
Transform = Callable[[SRC], DST]
Chainable = Callable[[Iterable[SRC]], Iterable[DST]]


def pipe(items: Iterable[Any], *chains: Chainable[Any, Any]) -> Iterable[Any]:
    if len(chains) == 0:
        return items
    if len(chains) == 1:
        return chains[0](items) 
    return chains[-1](pipe(items, *chains[:-1]))


def apply(items: Iterable[SRC], tr: Transform[SRC, DST]) -> Iterable[DST]:
    return (tr(item) for item in items)
