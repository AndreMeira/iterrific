from typing import TypeAlias
from iterrific.base.iter import consume, process

Label: TypeAlias = str

def getlabel(i: int) -> Label:
    return {
        i % 3  == 0: 'Fizz',
        i % 5  == 0: 'Buzz',
        i % 15 == 0: 'FizzBuzz',
    }.get(True, str(i))
    
def main():
    labels = map(getlabel, range(100))
    effects = process(labels, do=print)
    consume(effects)
    
    