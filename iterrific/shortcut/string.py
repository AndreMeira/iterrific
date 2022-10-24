from typing import Callable, Iterable


def startswith(s: str) -> Callable[[str], bool]:
    return lambda x: x.startswith(s)


def split(s: str) -> Callable[[str], Iterable[str]]:
    return lambda x: x.split(s)

