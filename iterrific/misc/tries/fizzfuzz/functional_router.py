from typing import Callable, Sequence, TypeAlias
from iterrific.types.functions import Cast
from iterrific.base.iter import router, process, consume


Label:    TypeAlias = str
GetLabel: TypeAlias = Cast[int, Label]
Match:    TypeAlias = Callable[[int], bool]
Rules:    TypeAlias = Sequence[tuple[Match, GetLabel]]


def rules() -> Rules:
    return (
        (lambda x: x % 15 == 0, lambda _: 'FizzBuzz'),
        (lambda x: x % 5  == 0, lambda _: 'Buzz'),
        (lambda x: x % 3  == 0, lambda _: 'Fizz'),
        (lambda _: True,        lambda x: str(x))
    )
    
def main():
    handler = router(rules=rules)
    texts = map(handler, range(100))
    effects = process(texts, do=print)
    consume(effects)
    
"""
@case
def game(i): 
    return str(i)    

@game.match(lambda x: x % 15 == 0)
def fizzbuzz(_) -> Label: 
    return 'FizzBuzz'

@game.match(lambda x: x % 5 == 0)
def fizzbuzz(_) -> Label: 
    return 'Buzz'

@game.match(lambda x: x % 3 == 0)
def fizzbuzz(_) -> Label: 
    return 'Fizz'

def main():
    for i in range(100):
        print(game(i))
"""    
