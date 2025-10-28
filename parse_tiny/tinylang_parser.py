from dataclasses import dataclass

@dataclass
class Token:
    type: str
    value: str | int
    line: int
    column: int
    
    def __repr__(self) -> str:
        return f" ({self.type}, Val: {self.value}, {self.line}:{self.column}) "

class parser:
    def __init__(self, tlist) -> None:
        self.source :list[Token] =  tlist
        self.size= len(self.source)
        