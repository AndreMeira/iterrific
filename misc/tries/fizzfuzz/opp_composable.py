from itertools import chain
from typing import Sequence, Protocol

Labels = Sequence[str]


class Labeler(Protocol):
    def get_labels(self, i: int) -> Labels: ...


class LabelMaker:
    
    modulo: int
    label: str
    
    def __init__(self, modulo: int, label: str) -> None:
        self.label = label
        self.modulo = modulo
    
    def get_labels(self, i: int) -> Labels:
        if i % self.modulo == 0:
            return (self.label,)
        return ()
    

class LabelComposer:
    
    makers: Sequence[LabelMaker]
    
    def __init__(self, *makers: LabelMaker) -> None:
        self.makers = makers
        
    def get_labels(self, i: int) -> Labels:
        nested = (maker.get_labels(i) for maker in self.makers)
        labels = chain.from_iterable(nested)
        return list(labels)


class NumberRendered:
    
    labeler: Labeler
    
    def __init__(self, labeler: Labeler) -> None:
        self.labeler = labeler
        
    def render(self, i: int):
        labels = self.labeler.get_labels(i)
        return ''.join(labels) or str(i)


class App:
    
    def labeler(self) -> Labeler:
        return LabelComposer(
            LabelMaker(3, 'Fizz'),
            LabelMaker(5, 'Buzz'),
        )
    
    def renderer(self) -> NumberRendered:
        return NumberRendered(self.labeler())
    
    def main(self):
        renderer = self.renderer()
        for i in range(100):
            print(renderer.render(i))