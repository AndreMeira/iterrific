from typing import Protocol, Union, Iterable


class ReadOnlyTree(Protocol):
    @property
    def left(self) -> Union['Tree', None]: ...
    @property
    def right(self) -> Union['Tree', None]: ...


class WritableTree(Protocol):
    left: Union['Tree', None]
    right: Union['Tree', None]


Tree = Union[ReadOnlyTree, WritableTree]


def traverse(tree: Tree) -> Iterable[Tree]:
    if hasattr(tree, 'left') and tree.left:
        yield from traverse(tree.left)

    yield tree
    if hasattr(tree, 'right') and tree.right:
        yield from traverse(tree.right)




