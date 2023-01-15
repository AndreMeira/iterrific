from typing import Optional


class PrintFizzBuzzNumber:
    
    COUNT = 100
    FIZZ = 3
    BUZZ = 5
    
    current: Optional[int]
    
    def __init__(self, count: int = COUNT) -> None:
        self.COUNT = count
    
    def run(self):
        for i in range(self.COUNT):
            self.set_current(i)
            self.print_current()
            
    def set_current(self, i: int) -> None:
        self.current = i
        
    def print_current(self) -> None:
        if self.current % (self.FIZZ * self.BUZZ) == 0:
            print('FizzBuzz')
        elif self.current % self.FIZZ:
            print('Fizz')
        elif self.current % self.BUZZ:
            print('Buzz')
        else: 
            print(self.current)
        