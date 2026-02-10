from dataclasses import dataclass

basicop = ["+", "-", "*", "/", "<",">", "&", "|", "^"]


@dataclass
class Token:
    type: str
    val: str
    line: int
    column: int
    
    def __repr__(self) -> str:
        return f' Token("{self.type}", "{self.val}", {self.line},{self.column}) '

class parserc:
    def __init__(self, tlist:list[Token]) -> None:
        self.source :list[Token] =  tlist #the input of raw tokens
        self.size= len(self.source)
        self.pos = 0
        self.astlist :list[dict] = [] #the actual output

        self.constants :dict[str, int]= {"false":0,"true":1}  #replace table for the constants only used in Mparse

    def parM(self) -> dict[str,int|str|dict]:

        def parse_primary()-> dict[str,int|str]:
            if self._eof():
                raise SyntaxError("Unexpected end of input")

            token = self.advance()

            # Stop parsing if we hit a semicolon or closing bracket
            if token.type == "SYMBOL" and token.val in [";", ")", ",","]"]:
                # Step back one so the parent parser can handle it
                self.pos -= 1
                raise StopIteration("End of expression")

            if token.type == "INT":
                return {"kind": "literal", "val": int(token.val)}
            elif token.type == "IDENTIFIER":
                name: str = token.val
                if name in self.constants:
                    return {"kind": "literal", "val": self.constants[name]}
                return {"kind": "identifier", "name": name}
            
            elif token.type == "char":
                return {"kind": "literal", "val": ord(token.val)} 
            
            elif token.val == "(":

                fparams = []
                while True:
                    fparams.append(self.parM())

                    seper = self.advance()

                    if seper.val == ",":
                        pass
                    elif seper.val == ")":
                        break
                    else:
                        self.expecter(seper, [",",","])

                    print("inside of funcdec loop")


                return {"kind":"fcall", "name": token.val, "param": fparams}  # type: ignore
            
            
            else:
                raise ValueError(f"Unexpected token in expression: {token}")

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


        def parse_expression(precedence:int=0) -> dict[str,int|dict|str]:

            try:
                left = parse_primary()
            except StopIteration:
                # End of expression, return empty literal or None
                return {"kind": "literal", "val": 0}

            while not self._eof():
                next_token = self.peek()

                # Stop at semicolon or other terminators
                if next_token.type == "SYMBOL" and next_token.val in [";", ")", ","]:
                    break

                if next_token.type != "OP":
                    break

                op = next_token.val
                op_prec = get_precedence(op)
                if op_prec < precedence:
                    break

                self.advance()  # consume operator
                right = parse_expression(op_prec + 1)
                left = fold_constants(left, op, right)

            return left # type: ignore


        return parse_expression()
        

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
            tmp=self.source[self.pos]
            self.pos+=1
            return tmp
        else:
            raise IndexError("tried to advance into nothingness")
        
    def let_parse(self):
        ttype:Token = self.advance()
        if ttype.type == "TYPE" or ttype.type == "IDENTIFIER":
            if self.peek()=="[":
                self.advance()
                if self.peek() == "]":  #means that its just an arr type
                    pass
                else:                   #means we have an arr size declaration
                    aarlen= self.parM()["val"]
                    
                    
            tname: Token= self.advance()
            if tname.type == "IDENTIFIER":

                folowing = self.peek()
                
                if folowing.val == "=":
                    self.advance()
                    if self.peek().val == "{":
                        #array init
                        self.advance() #consume [
                        arrvals = []
                        while True:
                            arrvals.append( self.parM() )
                            sep = self.advance()
                            if sep.val == ",":
                                continue
                            elif sep.val == "}":
                                break
                            else:
                                self.expecter(sep, [",","}"])

                        return {"kind":"letinit", "name": tname.val, "var_type":ttype.val, "val":arrvals,  "len":len(arrvals) }

                    val = self.parM()
                    self.advance()
                    return {"kind":"letinit", "name": tname.val, "var_type":ttype.val, "val":val }
                    
                elif folowing.val == ";":
                    self.expecter(self.advance(), ["=",";"])
                    return {"kind":"letdec", "name": tname.val, "var_type" : ttype.val}
                
                else:
                    self.expecter(folowing, ["=",";"])


    def     ident_parse(self,first:Token):
        second_token : Token = self.advance() 
        second_token_val = second_token.val

        
        tdict = {"kind":"asing", "acces": self.acces_parse(first,second_token), "val":{} }
        #ttmp = str(self.advance().val) # type: ignore levi is sexy
        #print("tmp "+str(second_token))
        
        
        if second_token_val == "=":
            tdict["val"] = self.parM()
            self.advance()

        elif second_token_val == "+" and self.peek().val == "+":
            tdict["val"] = {"kind": "binexp", "op": "+", "left": {"kind": "Identifier", "name": first.val} , "right": {"kind":"literal", "val": 1}}

        elif second_token_val == "-" and self.peek().val == "-":
           tdict["val"]= {"kind": "binexp", "op": "-", "left": {"kind": "Identifier", "name": first.val} , "right": {"kind":"literal", "val": 1}}

        elif second_token_val in basicop and self.peek().val == "=":
            rightval=self.parM()
            self.advance()
            tdict["val"]={"kind": "binexp", "op": second_token_val, "left": {"kind": "Identifier", "name": first.val} , "right": rightval }
        else:
            raise SyntaxError(f"Unexpected Token type in asing {second_token.type}:{second_token.val} on {self.liner(second_token)}")

        return tdict


    def while_parse(self):

        
        self.expecter(self.advance(), ["("])

        cond = self.parM()

        self.expecter(self.advance(), [")"])

        body = self.parse_block()

        return {"kind":"while", "exp" : cond, "body" : body}
    
    def if_parse(self):
        
        self.expecter(self.advance(), ["("])


        cond = self.parM()

        self.expecter(self.advance(), [")"])

        body = self.parse_block()

        return {"kind":"if", "exp" : cond, "body" : body}
    
    def const_parse(self) -> None:
        tmp: Token= self.advance()
        name = tmp.val

        if name  in self.constants.keys():
            raise SystemError(f"constant: {name} already exists {tmp.line}:{tmp.column}")
        
        
        self.expecter(self.advance(),["="])

        try:
            self.constants[name] = int(self.parM()["val"])   # type: ignore # cause idk and to int conversion is to fail on purpose
        except:
            raise SyntaxError(f"const can only be a number known at compile time\nName:{name}, on {tmp.line}:{tmp.column}")
        
        self.advance() #consume ; 

        return None
    
    def struct_parse(self):
        tocheck: Token  = self.advance()

        if tocheck.type == "TYPE":
            raise SyntaxError(f"you cant redefine {tocheck.val} as a struct {self.liner(tocheck)}")

        name: str = tocheck.val

        fields:list = self.parse_block()


        return {"kind":"struct_dec", "name": name , "members": fields}

        


    def for_parse(self):
        self.expecter(self.advance(),["("])

        initexp = self.parse_statement()

        self.expecter(self.advance(),[";"])

        testexp = self.parse_statement()

        self.expecter(self.advance(),[";"])

        incexp = self.parse_statement()

        self.expecter(self.advance(),[";"])

        self.expecter(self.advance(),[")"])

        body = self.parse_block()
        

        return {"kind":"for",  "init":initexp,"exp":testexp, "incexp":incexp , "body": body}
    
    def func_parse(self):
        ftype = self.advance()

        fname = self.advance()

        self.expecter(self.advance(),["("])


        fparams = []
        while True:
            fparams.append({
                "type": self.advance().val,
                "name": self.advance().val
            })

            seper = self.advance()

            if seper.val == ",":
                pass
            elif seper.val == ")":
                break
            else:
                self.expecter(seper, [",",")"])
            

            print("inside of funcdec loop")


        body = self.parse_block()


        

        return {"kind":"function_dec", "name": fname , "param": fparams, "ret_type": ftype, "body": body}
    
    def acces_parse(self, token:Token, nexttoken:Token):



        acces = {}

        base: str= token.val

        acclist = []

        print("next")
        print(nexttoken)


        while True:

            if nexttoken.val == ".":
                name: str = self.advance().val

                modifier: str = self.peek().val

                if modifier == "[":
                    self.advance()
                    index = self.parM()
                    self.expecter(self.advance(), ["]"])
                    acclist.append({'kind': 'arrac', 'name': name, 'pos': index})

                elif modifier == "(":
                    self.advance()

                    fparams = []
                    while True:
                        fparams.append(self.parM())

                        seper: Token = self.advance()

                        if seper.val == ",":
                            pass
                        elif seper.val == ")":
                            fparams = []
                            while True:
                                fparams.append(self.parM())

                                seper = self.advance()

                                if seper.val == ",":
                                    pass
                                elif seper.val == ")":
                                    break
                                else:
                                    self.expecter(seper, [",",","])
                                

                                print("inside of funcdec loop")

                            acclist.append({"kind":"fcall", "name": name, "param": fparams})
                        else:
                            self.expecter(seper, [",",","])
                        

                        print("end of funcdec loop")


                else:
                    acclist.append({"kind":"field",  "name": name})

            else:
                break


            nexttoken = self.peek()

        acces = {'kind': 'acces', "base": base, "access" : acclist}   

        
        

        return acces

    def expecter(self,val:Token,expected:list[str]):
        if val.val not in expected:
            raise SyntaxError(f"Expected {' or '.join(expected)} but got {val.val} on {self.liner(val)}")
        
    def liner(self, pos:Token)->str:
        return f"{pos.line}:{pos.column}"


        
    def parse_statement(self):
        first:Token = self.advance()
        
        match first.type:
            case "IDENTIFIER":
                return self.ident_parse(first)

            case "KEYWORD":
                match first.val:
                    case "let":
                        return self.let_parse()
                        
                    case "if":
                        return self.if_parse()

                    case "while":
                        return self.while_parse()
                    
                    case "for":
                        return self.for_parse()

                    case "func":
                        return self.func_parse()
                    
                    case "const":
                        return self.const_parse()
                        
                    case "return":
                        self.advance()
                        retval=self.parM()
                        self.expecter(self.advance(),[";"])
                        return   {"kind":"ret", "val": retval }
                    
                    case "struct":
                        return self.struct_parse()

                    
                    case _:
                        print("Astlist:")
                        print(self.astlist)

                        print("Folowing Tokens:")
                        print(self.source[self.pos:])
                        raise SyntaxError(f"Unexpected keyword {first.val} on {self.liner(first)}")
                    
            case _:
                print("Astlist:")
                print(self.astlist)

                print("Folowing Tokens:")
                print(self.source[self.pos:])
                raise SyntaxError(f"Unexpected Token type {first.type}:{first.val} on {self.liner(first)}")

                

    def parse_block(self):
        """Parse a { ... } block, return list of statements."""
        stmts = []

        self.expecter(self.advance(),["{"])

        while not self._eof() and self.peek().val != "}":
            val = self.parse_statement()
            if val != None:
                stmts.append(val)

        self.expecter(self.advance(),["}"])

        return stmts

    def parse(self):
        while not self._eof():
            stmt = self.parse_statement()
            #print(stmt)
            self.astlist.append(stmt) # type: ignore
        return self.astlist

testlist = [ Token("KEYWORD", "struct", 0,6) ,  Token("IDENTIFIER", "wonam_t", 0,14) ,  Token("SYMBOL", "{", 0,15) ,  Token("KEYWORD", "let", 1,7) ,  Token("TYPE", "un8", 1,11) ,  Token("IDENTIFIER", "age", 1,15) ,  Token("SYMBOL", ";", 1,16) ,  Token("KEYWORD", "let", 2,7) ,  Token("TYPE", "un16", 2,12) ,  Token("IDENTIFIER", "num", 2,16) , Token("SYMBOL", ";", 2,22) ,  Token("SYMBOL", "}", 3,1) ]

tester = [ Token("KEYWORD", "let", 0,3) ,  Token("TYPE", "un16", 0,8) ,  Token("IDENTIFIER", "num", 0,12) ,  Token("SYMBOL", ";", 0,13) ]

moretest = [ Token("KEYWORD", "struct", 0,6) ,  Token("IDENTIFIER", "wonam", 0,12) ,  Token("SYMBOL", "{", 0,14) ,  Token("KEYWORD", "let", 1,7) ,  Token("TYPE", "un8", 1,11) ,  Token("IDENTIFIER", "age", 1,15) ,  Token("SYMBOL", ";", 1,16) ,  Token("SYMBOL", "}", 2,1) ,  Token("KEYWORD", "let", 4,3) ,  Token("IDENTIFIER", "wonam", 4,9) ,  Token("IDENTIFIER", "maria", 4,15) ,  Token("SYMBOL", ";", 4,16) ,  Token("IDENTIFIER", "maria", 6,5) ,  Token("SYMBOL", ".", 6,6) ,  Token("IDENTIFIER", "age", 6,9) ,  Token("OP", "=", 6,11) ,  Token("INT", "20", 6,14) ,  Token("SYMBOL", ";", 6,15) ]

if __name__ == "main":
    Pparser = parserc(moretest)

    print(Pparser.parse())