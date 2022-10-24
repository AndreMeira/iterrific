from collections.abc import Iterable
from pathlib import PosixPath
from typing import Union, NamedTuple


class Item(NamedTuple):
    path: PosixPath
    level: int


def tree(path: Union[str, PosixPath], level:int = 0) -> Iterable[PosixPath]:
    if isinstance(path, str):
        yield from tree(PosixPath(path))
        return

    yield Item(path, level)
    if not path.is_dir():
        return

    dirs = []
    for subpath in path.iterdir():
        if not subpath.is_dir():
            yield Item(subpath, level)
            continue
        dirs.append(subpath)

    for subdir in dirs:
        yield Item(subdir, level)
        yield from tree(subdir, level + 1)


def flat(path: Union[str, PosixPath], level: int = 0) -> Iterable[PosixPath]:
    if isinstance(path, str):
        return flat(PosixPath(path))

    yield Item(path, level)
    if not path.is_dir():
        return

    dirs = []
    for subpath in path.iterdir():
        if not subpath.is_dir():
            yield Item(subpath, level)
            continue
        dirs.append(subpath)

    for subdir in dirs:
        yield Item(subdir, level)
    for subdir in dirs:
        yield from flat(subdir, level + 1)
