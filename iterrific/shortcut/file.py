from functools import partial as _
from os import PathLike
import re
from typing import Any, Callable, List, Union, Iterable
from os import PathLike


def read(path: Union[PathLike[Any], str, bytes]) -> str:
    with open(path) as f:
        return f.read()


def lines(path: Union[PathLike[Any], str, bytes]) -> Iterable[str]:
    with open(path) as f:
        return (line for line in f)


def grep(pattern: Union[re.Pattern[Any], str]) -> Callable[[str], List[str]]:
    if isinstance(pattern, str):
        pattern = re.compile(pattern)
    return _(re.findall, pattern)
