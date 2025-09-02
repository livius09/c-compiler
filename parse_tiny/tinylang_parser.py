

#parser
[
  {
    "kind": "LetDeclaration",
    "var_type": "n32",
    "name": "x",
    "val": {
      "kind": "literal",
      "val": 5
    }
  },
  {
    "kind": "ReturnStatement",
    "val": {
      "kind": "identifier",
      "name": "x"
    }
  }
] # type: ignore

#not mine
def parM(tokens: list[str]):
    #print("math pars:")
    #print(tokens)
    def parse_primary(token:str)-> dict:
        if token.startswith("INTEGER>"):
            return {"kind": "literal", "val": int(token.split(">")[1])}
        elif token.startswith("IDENTIFIER>"):

            name :str= token.split(">")[1]

            global constants

            if name in constants.keys():
                return {"kind": "literal", "val": constants[name]}
            else:   #only symbolic here
                #print(constants)
                return {"kind": "identifier", "name": name}
            
        elif token.startswith("REFRENCE>"):
            return {"kind": "refrence", "name": token.split(">")[1]}
        elif token.startswith("DEREFRENCE>"):
            return {"kind": "derefrence", "name": token.split(">")[1]}
        elif token.startswith("ARR>"):
            content :str =token.split(">")[2]

            if content.isdecimal():
                stuff={"kind": "literal", "val":int(content)}
            elif content.isalnum():
                stuff={"kind": "Identifier", "name": content}
            else:
                raise SyntaxError("arr indicies must be ints of identifiers not: "+str(content))

            return {"kind": "arrac", "name": token.split(">")[1],"pos":stuff}
        
        elif token.startswith("FUNCT>"):
            pass    #still need to implement ts for some reason
            
            tmp={}
            tmp["kind"] = "fcall"
            tmp["name"] = token.split(">")[1]
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
                tmp["para"].append(parM(current_param))
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


    def parse_expression(tokens:list[str], precedence:int=0):
        if not tokens:
            return None

        left = parse_primary(tokens.pop(0))

        while tokens:
            op = str(tokens[0])
            op_prec = get_precedence(op)
            if op_prec < precedence:
                break

            tokens.pop(0)  # consume the op
            right = parse_expression(tokens, op_prec + 1)
            left = fold_constants(left, op, right) # type: ignore

        return left

    return parse_expression(tokens[:])  # Copy list to avoid modifying input

#FunctionDeclaration(
#    name = "plus",
#    parameters = [
#        Parameter(type="n64", name="a"),
#        Parameter(type="n64", name="b")
#    ],
#    body = [
#        ReturnStatement(
#            value = BinaryExpression(
#                left = identifier("a"),
#                op = "+",
#                right = identifier("b")
#            )
#        )
#    ]
#)


#[['Let', 'TYPE>n64', 'IDENTIFIER>x', '=', 'INTEGER>1'], 
# ['Let', 'TYPE>n64', 'IDENTIFIER>x2', '=', 'INTEGER>6', '+', 'IDENTIFIER>x'], 
# ['Func', 'IDENTIFIER>plus', 'TYPE>n64', 'IDENTIFIER>a'], 
# '{', 
# ['Return', 'IDENTIFIER>a'], 
# '}']

#with open("tokenize/output.txt","r") as raw:
#    read = raw.read()





var_types :list[str]= ["n8","n16","n32","n64","un8","un16","un32","un64",     
             "n8~","n16~","n32~","n64~","un8~","un16~","un32~","un64~"] 

global constants
constants :dict[str, int]= {"false":0,"true":1}  #replace table for the constants only used in Mparse


def parse(line: list[list[str]])-> tuple[list[dict], int]:
    out = []
    i = 0

    while i < len(line):
        tmp = {}
        consumed :int= 1  # default: consume at least this line

        match line[i][0].lower():
            case "}":
                return out, i+1

            case "let":
                is_arr = False
                var_type = line[i][1].split(">")[1]
                tmp["kind"] = ""

                if var_type in var_types:
                    tmp["var_type"] = var_type
                elif var_type.endswith("[]") and (var_type[:-2] in var_types):
                    tmp["var_type"] = var_type
                    is_arr = True
                else:
                    raise SyntaxError("type cant be: "+ var_type)

                # Find identifier
                for tok in line[i]:
                    if tok.startswith("IDENTIFIER>"):
                        tmp["name"] = tok.split(">")[1]
                        break
                else:
                    raise SyntaxError("no given identifier in "+str(line[i]))

                if "=" in line[i]:
                    tmp["kind"] = "letinit"
                    if is_arr:
                        arr_line = line[i+2]
                        chunks :list[list[str]]= []
                        current = []

                        for token in arr_line:
                            if token == ",":
                                chunks.append(current)
                                current = []
                            else:
                                current.append(token)

                        if current:
                            chunks.append(current)

                        tmp["len"] = len(chunks)
                        tmp["val"] = [parM(chunk) for chunk in chunks]
                        consumed = 3
                    else:
                        math_part = line[i][line[i].index("=") + 1:]
                        tmp["val"] = parM(math_part)
                else:
                    tmp["kind"] = "letdec"
                    if is_arr:
                        tmp["len"] = int(line[i][2].split(">")[1])

            case "const":
                name=line[i][1].split(">")[1]

                if name  in constants.keys():
                    raise SystemError(f"constant: {name} already exists")
                
                math_part = line[i][line[i].index("=") + 1:]

                try:
                    constants[name] = int(parM(math_part)["val"])   # type: ignore #warning cause idk and to int conversion is to fail on purpose
                except:
                    raise SyntaxError(f"const can only be a number known at compile time\nName:{name}")





            case "func":        #for functions being declared
                tmp["kind"] = "func_dec"
                tmp["name"] = line[i][2].split(">")[1]
                tmp["ret_type"] = line[i][1].split(">")[1]
                tmp["param"] = []

                for a in range(4, len(line[i]), 2):
                    tmp["param"].append({
                        "type": line[i][a].split(">")[1],
                        "name": line[i][a+1].split(">")[1]
                    })
                    print("inside of funcdec loop")
                    print(line[i][a])
                    print(line[i][a+1])


                body, body_consumed = parse(line[i+2:])
                tmp["body"] = body
                consumed = 3 + body_consumed    #3 for func,{,}

            case "return":
                tmp["kind"] = "ret"
                tmp["val"] = parM(line[i][1:])

            case "if":
                tmp["kind"] = "if"
                tmp["exp"] = parM(line[i][1:])

                # Parse the "if" body (skip the '{' at i+1)
                body, body_consumed = parse(line[i + 2:])
                tmp["body"] = body

                # Where the "else" would be if present
                after_if_index = i + 2 + body_consumed

                # Check for "else" directly after the closing "}"
                if after_if_index < len(line) and line[after_if_index][0] == "else":
                    
                    # Parse else body (skip the '{' at after_if_index+1)
                    else_body, else_body_consumed = parse(line[after_if_index + 2:])
                    tmp["else_body"] = else_body

                    # Total consumed: if start to end of else body
                    consumed = (after_if_index + 2 + else_body_consumed) - i
                else:
                    # No else found
                    consumed = 2 + body_consumed


            case "while":
                tmp["kind"] = "while"
                tmp["exp"] = parM(line[i][2:])
                body, body_consumed = parse(line[i+2:])
                tmp["body"] = body
                consumed = 2 + body_consumed

            case "for":
                tmp["kind"] = "for"
                tmp["init"] = parse([line[i+1]])[0]
                tmp["exp"] = parM(line[i+2])
                tmp["incexp"] = parse([line[i+3]])[0]
                tmp["body"], body_consumed = parse(line[i+5:])
                consumed = 5 + body_consumed

            case _:
                if line[i][0].startswith("IDENTIFIER>"):    #for the asings like "x=1"
                    tmp["kind"] = "asing"
                    tmp["name"] = line[i][0].split(">")[1]
                    tmp["val"] = parM(line[i][2:])

                elif line[i][0].startswith("FUNCT>"):       #for standalone function calls
                    tmp["kind"] = "fcall"
                    tmp["name"] = line[i][0].split(">")[1]
                    tmp["para"] = []
                    j = 1
                    current_param = []
                    while j < len(line[i]):
                        if line[i][j] == ",":
                            tmp["para"].append(parM(current_param))
                            current_param = []
                        else:
                            current_param.append(line[i][j])
                        j += 1
                    if current_param:
                        tmp["para"].append(parM(current_param))

                elif line[i][0].startswith("TYPE>") and line[i][1].startswith("FUNCT>"):    #wth ?
                    tmp["kind"] = "fun_dec"
                    tmp["name"] = line[i][1].split(">")[1]
                    tmp["ret_type"] = line[i][0].split(">")[1]
                    tmp["para"] = []
                    j = 1
                    current_param = []
                    while j < len(line[i]):
                        if line[i][j] == ",":
                            tmp["para"].append(parM(current_param))
                            current_param = []
                        else:
                            current_param.append(line[i][j])
                        j += 1
                    if current_param:
                        tmp["para"].append(parM(current_param))

                elif line[i][0].startswith("ARR>"):
                    tmp["kind"] = "asing"
                    tmp["name"] = line[i][0].split(">")[1]
                    content = line[i][0].split(">")[2]
                    if content.isdecimal():
                        tmp["pos"] = {"kind": "literal", "val": int(content)}
                    elif content.isalnum():
                        tmp["pos"] = {"kind": "Identifier", "name": content}
                    else:
                        raise SyntaxError("arr aces only suports literal and identifier")
                    tmp["val"] = parM(line[i][2:])
                else:
                    raise SyntaxError(str(line[i]) + " at: " + str(i))

        if tmp != {}:
            out.append(tmp)

        i += consumed

    return out, i




fort = [['for'], ['Let', 'TYPE>n8', 'IDENTIFIER>i', '=', 'INTEGER>0'], ['IDENTIFIER>i', '!=', 'INTEGER>4'], ['IDENTIFIER>i', '=', 'IDENTIFIER>i', '+', 'INTEGER>1'], '{', ['IDENTIFIER>x', '=', 'IDENTIFIER>x', '+', 'INTEGER>1'], '}']
fart = [['for'], ['Let', 'TYPE>n8', 'IDENTIFIER>i', '=', 'INTEGER>0'], ['IDENTIFIER>i', '==', 'INTEGER>1'], ['IDENTIFIER>i', '=', 'IDENTIFIER>i', '+', 'INTEGER>1'], '{', ['IDENTIFIER>e', '=', 'IDENTIFIER>e', '+', 'INTEGER>1'], '}']
ptrt = [['Let', 'TYPE>n8', 'IDENTIFIER>num', '=', 'INTEGER>2'], ['Let', 'TYPE>n8~', 'IDENTIFIER>ptr', '=', 'REFRENCE>num'], ['Let', 'TYPE>n32', 'IDENTIFIER>refnum', '=', 'DEREFRENCE>ptr', '+', 'INTEGER>1']]
arrt = [['Let', 'TYPE>n32', 'IDENTIFIER>num'], ['Let', 'TYPE>n32', 'IDENTIFIER>nam', '=', 'INTEGER>15'], ['Let', 'TYPE>n8[]', 'len>10', 'IDENTIFIER>nbm'], ['Let', 'TYPE>n8[]', 'IDENTIFIER>ncm', '='], '{', ['INTEGER>1', ',', 'INTEGER>2', ',', 'INTEGER>3', ',', 'INTEGER>4'], '}', ['IDENTIFIER>num', '=', 'INTEGER>10']]
arct = [['Let', 'TYPE>n32', 'IDENTIFIER>num'],['ARR>ncm>2', '=', 'INTEGER>2']]
bint = [['Let', 'TYPE>n32', 'IDENTIFIER>num'], ['IDENTIFIER>num', '=', 'INTEGER>1', '<<', 'IDENTIFIER>num'], ['IDENTIFIER>num', '=', 'INTEGER>2', '&', 'IDENTIFIER>num'], ['IDENTIFIER>num', '=', 'INTEGER>2', '|', 'IDENTIFIER>num']]
funt = [['TYPE>n32', 'FUNCT>main', '(', 'TYPE>n8', 'IDENTIFIER>na', ',', 'TYPE>n32', 'IDENTIFIER>num'], '{', ['Return', 'IDENTIFIER>na', '+', 'IDENTIFIER>num'], '}']
cost = [['const', 'IDENTIFIER>pi', '=', 'INTEGER>3'], ['Let', 'TYPE>n8', 'IDENTIFIER>thing', '=', 'IDENTIFIER>pi', '+', 'INTEGER>1']]
ifel = [['Let', 'TYPE>n8', 'IDENTIFIER>inam', '=', 'INTEGER>10'], ['IDENTIFIER>inam', '=', 'INTEGER>13'], ['if', 'IDENTIFIER>inam', '==', 'INTEGER>1'], '{', ['IDENTIFIER>inam', '=', 'INTEGER>12'], '}', ['else'], '{', ['IDENTIFIER>inam', '=', 'INTEGER>15'], '}']

test = [['Let', 'TYPE>n64', 'IDENTIFIER>global', '=', 'INTEGER>1', '+', 'INTEGER>2'], ['Func', 'TYPE>void', 'FUNCT>Main', '('], '{', ['Let', 'TYPE>n64', 'IDENTIFIER>local', '=', 'INTEGER>1', '<<', 'INTEGER>1'], ['IDENTIFIER>local', '=', 'IDENTIFIER>global', '+', 'INTEGER>1'], '}']

if __name__ == "__main__":
    out,lines = parse(ifel)
    print(out)
