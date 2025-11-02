from dataclasses import dataclass

@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int
    
    def __repr__(self) -> str:
        return f' Token("{self.type}", "{self.value}", {self.line},{self.column}) '


        

class Tokenizerc:
    def __init__(self, source: str) -> None:
        self.source: str = source
        self.size: int= len(source)
        self.pos = 0
        self.line=0
        self.col=0
        
        self.tokens :list[Token] = []
        self.current_line = []
        

    def _eof(self) -> bool:
        return self.pos == self.size
    
    def _peek(self, n:int=1) -> str:
        if self.pos+n <= self.size:
            return self.source[self.pos:self.pos+n]
        else:
            raise IndexError("tried to peek into nothingness")
    
    
    def _advance(self, n:int=1)-> str:
        if self.pos+n <= self.size:
            val = self.source[self.pos:self.pos + n]
            for ch in val:
                if ch == "\n":
                    self.line += 1
                    self.col = 0
                else:
                    self.col += 1
            self.pos += n
            return val
        else:
            raise IndexError("tried to advance into nothingness")
       


    def _consume_space(self) -> None:
        self.pos+=1

    def _consume_coment(self)-> None:
        self.pos+=1
        while not self._eof() and not self._peek() == "\n":
            self._advance()


    def _consume_string(self) -> None:
        self.pos+= 1
        tmp: str = ""
        while(not self._eof() and self._peek() != '"'):
            tmp += self._advance()

        self.tokens.append(Token("STR", tmp, self.line, self.col))

    def _consume_keyw_type_id(self) -> None:
        tmp: str = ""
        while(not self._eof() and (self._peek().isalnum() or self._peek() == "_") ):
            tmp += self._advance()

        if tmp in keywords:
            self.tokens.append(Token("KEYWORD",tmp, self.line, self.col))
        elif tmp in types:

            if self._peek() == "~":
                tmp+="~"
                self.pos+=1
            self.tokens.append(Token("TYPE",tmp, self.line, self.col))
        else:
            self.tokens.append(Token("IDENTIFIER",tmp, self.line, self.col))
    
    def _consume_num(self) -> None:
        tmp: str | int = ""
        while(not self._eof() and self._peek().isnumeric()):
            tmp += self._advance()
        
        try:
            tmp = int(tmp) #cast to int as a test cast back to str to fit in token
        except:
            raise SyntaxError("failed to parse number")
        self.tokens.append(Token("INT",str(tmp), self.line, self.col))

    def _consume_symbol(self) -> None:

        self.tokens.append(Token("SYMBOL",self._advance(), self.line, self.col))

    def _consume_char(self) -> None:
        char = self._peek(3)
        if char[0]=="'" and char[1].isascii() and char[2]=="'":
            self.tokens.append(Token("CHAR",char[1], self.line, self.col))
        else:
            raise SyntaxError(f"misformed char: {char}")
    
    def _consume_op(self):
        op = self._peek(2)
        if op in operators:
            self.tokens.append(Token("OP", self._advance(2), self.line, self.col))
        else:
            self.tokens.append(Token("OP",self._advance(), self.line, self.col))

    def _consume_ref_deref(self):
        pre = self._advance()
        tmp: str = ""
        while(not self._eof() and self._peek().isalnum()):
            tmp += self._advance()

        if pre == "~":
            self.tokens.append(Token("DEREF",tmp, self.line, self.col))

        else:
            self.tokens.append(Token("REF",tmp, self.line, self.col))

            


    def Tokenize(self):
        while not self._eof():
            ch: str = self._peek()
            if ch.isspace():
                self._consume_space()
            elif ch == "#":
                self._consume_coment()
            elif ch == '"':
                self._consume_string()
            elif ch == "'":
                self._consume_char()
            elif ch.isalpha():
                self._consume_keyw_type_id()
            elif ch.isnumeric():
                self._consume_num()
            elif ch in symbols:
                self._consume_symbol()
            elif ch in operators:
                self._consume_op()
            elif ch in ["~","$"]:
                self._consume_ref_deref()
            else:
                raise SyntaxError("unknown syntax")
        
        #print(self.source)
        print(self.tokens)



TOKEN_TYPES: set[str] = {
    "KEYWORD",
    "IDENTIFIER",
    "TYPE",
    "INT",
    "STR",
    "CHAR",
    "OP",
    "SYMBOL",
    "REF",
    "DEREF"
}

symbols:set[str] = {",","(",")","{","}",";",}
operators: set[str]={"+", "-", "*", "/", "=", "<",">", "==", "!=", "!", "<<", ">>",">=","<=", "&", "|", "^"}
keywords: set[str] = {"let", "const", "return", "for", "while", "break", "if", "else", "func"}

types: set[str] = {"n8","n16","n32","n64","un8","un16","un32","un64", "void",     
         "n8~", "n16~", "n32~", "n64~", "un8~", "un16~", "un32~", "un64~"}

if __name__ == "__main__":

    with open("tokenize_tiny/input.txt","r") as raw:
        read: str = raw.read()

    Tokenize = Tokenizerc(read)
    Tokenize.Tokenize()

