from collections.abc import Iterable
from pathlib import Path
from typing import Union, NamedTuple


class Item(NamedTuple):
    path: Path
    level: int


def tree(path: Union[str, Path], level: int = 0) -> Iterable[Item]:
    path = Path(path)
    yield Item(path, level)

    subdirs = path.iterdir() \
        if path.is_dir() else []

    for subpath in subdirs:
        yield from tree(subpath, level=level+1)

