from typing import Mapping, Sequence, TypeAlias
from iterrific.base.iter import consume, process
from iterrific.types.functions import Cast
from iterrific.types.common import Stream

Label: TypeAlias = str

def labelmap() -> Mapping[int, Label]:
    return (
        (15, 'FizzBuzz'),
        (5,  'Buzz'),
        (3,  'Fizz')
    )
    
def labels(i: int) -> Stream[Label]:
    return (
        label for modulo, label in labels() 
        if i % modulo == 0
    )
    
def label(i: int) -> Label:
    return next(labels(i), str(i))
    

def main():
    for i in range(100):
        print(label(i))