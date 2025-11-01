from dataclasses import dataclass
#from multipledispatch import dispatch

basicop = ["+", "-", "*", "/", "<",">", "&", "|", "^"]

@dataclass
class Token:
    type: str
    val: str | int
    line: int
    column: int
    
    def __repr__(self) -> str:
        return f" ({self.type}, Val: {self.val}, {self.line}:{self.column}) "

class parserc:
    def __init__(self, tlist) -> None:
        self.source :list[Token] =  tlist #the input of raw tokens
        self.size= len(self.source)
        self.pos = 0
        self.astlist :list[dict] = [] #the actual output

        self.constants :dict[str, int]= {"false":0,"true":1}  #replace table for the constants only used in Mparse

    def parM(self):
        pass
        

    def _eof(self):
        return self.pos == self.size
    
    #@dispatch(object, int)
    #def peek(self, n:int=1) -> list[Token]:
    #    if self.pos+n <= self.size:
    #        return self.source[self.pos:self.pos+n]
    #    else:
    #        raise IndexError("tried to peek into nothingness")
        
    #@dispatch(object)
    def peek(self) -> Token:
        if self.pos+1 <= self.size:
            return self.source[self.pos]
        else:
            raise IndexError("tried to peek into nothingness")

       
    #def advance(self,n:int=1)-> list[Token] | Token:
    #    if self.pos+n <= self.size:
    #        return self.source[self.pos:self.pos+n]
    #    else:
    #        raise IndexError("tried to advance into nothingness")
        
    def advance(self)-> Token:
        if self.pos <= self.size:
            return self.source[self.pos]
        else:
            raise IndexError("tried to advance into nothingness")
        
    def parse(self):
        first:Token = self.advance()
        
        match first.type:
            case "IDENTIFIER":
                ttmp = self.advance().val
                if ttmp == "=":
                    pass
                elif ttmp == "+" and self.peek().val == "+":
                    self.astlist.append({"kind":"asing", "name": first.val, "val":{"kind": "binexp", "op": "+", "left": {"kind": "Identifier", "name": first.val} , "right": {"kind":"literal", "val": 1}}})
                elif ttmp == "-" and self.peek().val == "-":
                    self.astlist.append({"kind":"asing", "name": first.val, "val":{"kind": "binexp", "op": "-", "left": {"kind": "Identifier", "name": first.val} , "right": {"kind":"literal", "val": 1}}})
                elif ttmp in basicop and self.peek().val == "=":
                    self.astlist.append({"kind":"asing", "name": first.val, "val":{"kind": "binexp", "op": ttmp, "left": {"kind": "Identifier", "name": first.val} , "right": self.parM()}})


            case "KEYWORD":
                match first.val:
                    case "let":
                        pass
                    case "const":
                        tmp: Token= self.advance()
                        name = tmp.val

                        if name  in self.constants.keys():
                            raise SystemError(f"constant: {name} already exists")
                        
                        self.advance()
                        math_part = []

                        try:
                            self.constants[name] = int(self.parM(math_part)["val"])   # type: ignore #warning cause idk and to int conversion is to fail on purpose
                        except:
                            raise SyntaxError(f"const can only be a number known at compile time\nName:{name}, on {tmp.line}:{tmp.column}")


