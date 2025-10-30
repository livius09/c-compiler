from dataclasses import dataclass

@dataclass
class Token:
    type: str
    value: str | int
    line: int
    column: int
    
    def __repr__(self) -> str:
        return f" ({self.type}, Val: {self.value}, {self.line}:{self.column}) "

class parserc:
    def __init__(self, tlist) -> None:
        self.source :list[Token] =  tlist
        self.size= len(self.source)
        
        self.pos = 0

        astl = []

    def _eof(self):
        return self.pos == self.size

    def peek(self, n:int=1):
        if self.pos+n <= self.size:
            return self.source[self.pos:self.pos+n]
        else:
            raise IndexError("tried to peek into nothingness")
        
    def advance(self,n:int=1):
        if self.pos+n <= self.size:
            return self.source[self.pos:self.pos+n]
        else:
            raise IndexError("tried to advance into nothingness")
        
    def parse(self):
        pass
