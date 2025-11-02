from dataclasses import dataclass
#from multipledispatch import dispatch

basicop = ["+", "-", "*", "/", "<",">", "&", "|", "^"]


@dataclass
class Token:
    type: str
    val: str
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

    def parM(self, tokens: list[Token]) -> dict[str,int|str|dict]:
        #print("math pars:")
        #print(tokens)
        def parse_primary(token:Token)-> dict:
            if token.type == "INT":
                return {"kind": "literal", "val": int(token.val)}
            elif token.type=="IDENTIFIER":

                name :str= token.val

                if name in self.constants.keys():
                    return {"kind": "literal", "val": self.constants[name]}
                else:   #only symbolic here
                    #print(constants)
                    return {"kind": "identifier", "name": name}
                
            elif token.type=="REF":
                return {"kind": "refrence", "name": token.val}
            elif token.type=="DEREF":
                return {"kind": "derefrence", "name": token.val}
            elif token.type == "ARR":                               #very importantitny 
                content :str =token.val

                if content.isdecimal():
                    stuff={"kind": "literal", "val":int(content)}
                elif content.isalnum():
                    stuff={"kind": "Identifier", "name": content}
                else:
                    raise SyntaxError("arr indicies must be ints of identifiers not: "+str(content))

                return {"kind": "arrac", "name": token,"pos":stuff}
            
            elif token.val == "FUNCT":
                pass    #still need to implement ts for some reason
                
                tmp={}
                tmp["kind"] = "fcall"
                tmp["name"] = token.val
                tmp["para"] = []
                j = 1
                current_param = []
                #while j < len(line[i]):
                #    if line[i][j] == ",":
                #        tmp["para"].append(parM(current_param))
                #        current_param = []
                #    else:
                #        current_param.append(line[i][j])
                #    j += 1
                if current_param:
                    tmp["para"].append(self.parM(current_param))
                return tmp
            
            else:
                raise ValueError(f"Unexpected token: {token}")

        def get_precedence(op:str) -> int:
            return {
                '<=' :1,
                '>=' :1,
                '!=' :1,
                '==' :1,
                '!'  :1,
                '&'  :1,
                '|'  :1,
                '<<' :1,
                '>>' :1,
                '^'  :1,
                '>'  :1,
                '<'  :1,
                '+'  :2,
                '-'  :2,
                '*'  :3,
                '/'  :3,
                '%'  :3,
            }.get(op, -1)  # Unknown ops = very low precedence

        def fold_constants(left:dict, op:str, right:dict):
            # If both sides are integer literals: constant fold
            if left["kind"] == "literal" and right["kind"] == "literal":
                a :int = int(left["val"])
                b :int = int(right["val"])
                result :int|None = None
                if op ==   '+':
                    result = a + b
                elif op == '-':
                    result = a - b
                elif op == '*':
                    result = a * b
                elif op == '/':
                    result = a // b if b != 0 else 0
                elif op == '==':
                    result = int(a == b)
                elif op == '!=':
                    result = int(a != b)
                elif op == '<':
                    result = int(a < b)
                elif op == '>':
                    result = int(a > b)
                elif op == '<=':
                    result = int(a <= b)
                elif op == '&':
                    result = int(a & b)
                elif op == '|':
                    result = int(a | b)    
                elif op == '^':
                    result = int(a ^ b) 
                elif op == '>>':
                    result = int(a >> b) 
                elif op == '<<':
                    result = int(a << b)                

                # Return folded literal if result was computed
                if result is not None:
                    return {"kind": "literal", "val": result}

            # Algebraic simplification with 0 or 1
            if op == '+' and right["kind"] == "literal" and right["val"] == 0:
                return left
            if op == '+' and left["kind"] == "literal" and left["val"] == 0:
                return right

            if op == '-' and right["kind"] == "literal" and right["val"] == 0:
                return left

            if op == '*' and ((left["kind"] == "literal" and left["val"] == 0) or
                            (right["kind"] == "literal" and right["val"] == 0)):
                return {"kind": "literal", "val": 0}

            if op == '*' and right["kind"] == "literal" and right["val"] == 1:
                return left
            if op == '*' and left["kind"] == "literal" and left["val"] == 1:
                return right

            if op == '/' and right["kind"] == "literal" and right["val"] == 1:
                return left
            
            if op == '>>' and right["kind"] == "literal" and right["val"] == 0:
                return left
            
            if op == '<<' and right["kind"] == "literal" and right["val"] == 0:
                return left

            # Not foldable
            return {
                "kind": "binexp",
                "op": op,
                "left": left,
                "right": right
            }


        def parse_expression(tokens:list[Token], precedence:int=0):
            if not tokens:
                return None

            left = parse_primary(tokens.pop(0))

            while tokens:
                op: str = str(tokens[0].val)
                op_prec: int = get_precedence(op)
                if op_prec < precedence:
                    break

                tokens.pop(0)  # consume the op
                right = parse_expression(tokens, op_prec + 1)
                left = fold_constants(left, op, right) # type: ignore

            return left

        return parse_expression(tokens[:])  # type: ignore # Copy list to avoid modifying input
        

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
                    self.astlist.append({"kind":"asing", "name": first.val, "val":{"kind": "binexp", "op": ttmp, "left": {"kind": "Identifier", "name": first.val} , "right": 1}}) #fix


            case "KEYWORD":
                match first.val:
                    case "let":
                        ttype: Token = self.advance()
                        if ttype.type == "TYPE":
                            tname: Token= self.advance()
                            if tname.type == "IDENTIFIER":
                                if self.advance().val == "=":
                                    pass


                    case "const":
                        tmp: Token= self.advance()
                        name = tmp.val

                        if name  in self.constants.keys():
                            raise SystemError(f"constant: {name} already exists")
                        
                        self.advance()
                        math_part = []

                        try:
                            self.constants[name] = int(self.parM(math_part)["val"])   # type: ignore # cause idk and to int conversion is to fail on purpose
                        except:
                            raise SyntaxError(f"const can only be a number known at compile time\nName:{name}, on {tmp.line}:{tmp.column}")


testlist: list[Token] = [ Token("KEYWORD", "const", 0,5) ,  Token("IDENTIFIER", "pi_round3", 0,14) ,  Token("OP", "=", 0,15) ,  Token("INT", "3", 0,16) ,  Token("SYMBOL", ";", 0,17) ,  Token("KEYWORD", "let", 0,20) ,  Token("TYPE", "n8~", 0,22) ,  Token("IDENTIFIER", "thing", 0,27) ,  Token("OP", "=", 0,28) ,  Token("IDENTIFIER", "pi", 0,30) ,  Token("OP", "+", 0,31) ,  Token("INT", "1", 0,32) ,  Token("SYMBOL", ";", 0,33) ]

mtestlist: list[Token] = [Token("INT", "2", 0,29) ,  Token("OP", "*", 0,30) ,  Token("IDENTIFIER", "true", 0,32) ,  Token("OP", "+", 0,33) ,  Token("INT", "1", 0,34) ,  Token("SYMBOL", ";", 0,35)]

parser = parserc([])

print(parser.parM(mtestlist))