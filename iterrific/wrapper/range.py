from typing import Iterable


class Rng:
    def __getitem__(self, s: slice) -> Iterable[int]:
        return range(s.start or 0, s.stop, s.step or 1)