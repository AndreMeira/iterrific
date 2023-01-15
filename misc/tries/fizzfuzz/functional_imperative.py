from itertools import count, islice
from typing import Callable, Generic, Sequence, TypeVar

from iterrific.types.common import Stream, infinite
from iterrific.base.iter import consume, process
from iterrific.types.functions import Cast


T = TypeVar("T")
G = TypeVar("G")
Labels = Sequence[str]

class Map(Generic[T, G]):
    handler: Callable[[T], G]

    def __init__(self, fn: Callable[[T], G]):
        self.handler = fn

    def __call__(self, stream: Stream[T]) -> Stream[G]:
        return (self.handler(item) for item in stream)

        
def buzz(i: int) -> Labels:
    return ('Buzz',) if i % 3 else ()
      
def fizz(i: int) -> Labels:
      return ('Fizz',) if i % 5 else ()        
        
def label(i: int) -> Labels:
    return (*buzz(i), *fizz(i))

def labelled_number(i: int) -> tuple[int, Labels]:
    return (i, label(i))

def print_labelled(labelled: tuple[str, Labels]):
    labels = ''.join(labelled[1])
    print(labels or str(labelled[0]))

def main():
    start    = count  # for readiblity only
    numbers  = infinite(start(0))
    labelall = Map(labelled_number)
    labelled = labelall(numbers)
    hundred  = islice(labelled, 100)
    printall = process(hundred, do=print_labelled)
    consume(printall)


