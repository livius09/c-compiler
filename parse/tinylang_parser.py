

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
]

#not mine
def parM(tokens: list):
    def parse_primary(token):
        if token.startswith("INTEGER>"):
            return {"kind": "literal", "val": int(token.split(">")[1])}
        elif token.startswith("IDENTIFIER>"):
            return {"kind": "identifier", "name": token.split(">")[1]}
        elif token.startswith("REFRENCE>"):
            return {"kind": "refrence", "name": token.split(">")[1]}
        elif token.startswith("DEREFRENCE>"):
            return {"kind": "derefrence", "name": token.split(">")[1]}
        elif token.startswith("ARR>"):
            content=token.split(">")[2]

            if content.isdecimal():
                stuff={"kind": "literal", "val":int(content)}
            elif content.isalnum():
                stuff={"kind": "Identifier", "name": content}

            return {"kind": "arrac", "name": token.split(">")[1],"pos":stuff}
        
        else:
            raise ValueError(f"Unexpected token: {token}")

    def get_precedence(op):
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

    def fold_constants(left, op, right):
    # If both sides are integer literals: constant fold
        if left["kind"] == "literal" and right["kind"] == "literal":
            a, b = left["val"], right["val"]
            result = None
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


    def parse_expression(tokens, precedence=0):
        if not tokens:
            return None

        left = parse_primary(tokens.pop(0))

        while tokens:
            op = tokens[0]
            op_prec = get_precedence(op)
            if op_prec < precedence:
                break

            tokens.pop(0)  # consume the op
            right = parse_expression(tokens, op_prec + 1)
            left = fold_constants(left, op, right)

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





var_types = ["n8","n16","n32","n64","un8","un16","un32","un64",     
             "n8~","n16~","n32~","n64~","un8~","un16~","un32~","un64~"]


def parse(line: list[list[str]]):
    out = []
    i = 0

    while i < len(line):
        tmp = {}
        consumed = 1  # by default, assume we consume this line

        match line[i][0].lower():
            case "}":
                break

            case "let":
                is_arr = False
                var_type = line[i][1].split(">")[1]


                if var_type in var_types:
                    tmp["var_type"] = var_type
                elif var_type.endswith("[]") and (var_type[:-2] in var_types):
                    tmp["var_type"] = var_type
                    is_arr = True
                else:
                    raise SyntaxError("type cant be: "+ var_type)
                

                if line[i][2].startswith("IDENTIFIER>"):

                    tmp["name"] = line[i][2].split(">")[1]

                elif line[i][3].startswith("IDENTIFIER>"):

                    tmp["name"] = line[i][3].split(">")[1]
                else:
                    raise SyntaxError("no given identifier for "+line[i][3]+line[i][2])



                if len(line[i]) > 3 and line[i][3] == "=": 
                    #is an initialazion

                    tmp["kind"] = "letinit"

                    

                    if is_arr:

                        lene = line[i+2].count(",")+1
                        tmp["len"] = lene
                        
                        arr = []


                        chunks = []
                        current = []

                        for token in line[i+2]:
                            if token == ",":
                                chunks.append(current)
                                current = []
                            else:
                                current.append(token)

                        # Append the last chunk
                        if current:
                            chunks.append(current)

                        # Now call parM() on each chunk
                        for chunk in chunks:
                            arr.append(parM(chunk))

                        tmp["val"] = arr
                        i+=3
                        

  

                    else:
                        var_type = line[i][1].split(">")[1]

                        math_part = line[i][line[i].index('=') + 1:]

                        tmp["val"] = parM(math_part)

                else:
                    #is and decl

                    tmp["kind"] = "letdec"

                    if is_arr:
                        tmp["len"] = int(line[i][2].split(">")[1])



            case "func":
                tmp["kind"] = "func_dec"
                tmp["name"] = line[i][2].split(">")[1]
                tmp["ret_type"]= line[i][1].split(">")[1]
                tmp["param"] = []
                for a in range(1, len(line[i]) - 4, 4):
                    tmp["param"].append({
                        "type": line[i][a].split(">")[1],
                        "name": line[i][a+1].split(">")[1]
                    })

                body, body_consumed = parse(line[i+2:])
                tmp["body"] = body
                consumed += body_consumed

            case "return":
                tmp["kind"] = "ret"
                tmp["val"] = parM(line[i][1:])


            case "if":
                tmp["kind"] = "if"
                tmp["exp"] = parM(line[i][1:])
                body, body_consumed = parse(line[i+2:])
                tmp["body"] = body
                consumed += 2 + body_consumed  # +2 for 'If' line and '{' line
            
            case "while":
                tmp["kind"]="while"
                tmp["exp"] = parM(line[i][1:])
                body, body_consumed = parse(line[i+2:])
                tmp["body"] = body
                consumed += 2 + body_consumed  # +2 for 'while' line and '{' line
            
            case "for":
                
                tmp["kind"] = "for"

                tmp["init"] = parse([line[i+1]])[0][0]
                print(line[i])
                print(line[i+1])
                print(line[i+2])
                print(line[i+3])
                tmp["exp"] = parM(line[i+2])
                tmp["incexp"] = parse([line[i+3]])[0]
                
                tmp["body"], body_consumed = parse(line[i+5:])
                i += 5 
                consumed += body_consumed + 5


            case _:
                if line[i][0].startswith("IDENTIFIER>"):
                    tmp["kind"] = "asing"
                    tmp["name"] = line[i][0].split(">")[1]
                    tmp["val"] = parM(line[i][2:])

                elif line[i][0].startswith("FUNCT>"):
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

                elif line[i][0].startswith("TYPE>") and line[i][1].startswith("FUNCT>"):
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
                    #'ARR>ncm>2', '=', 'INTEGER>2'
                    tmp["kind"] = "asing"
                    tmp["name"] = line[i][0].split(">")[1]
                    
                    content=line[i][0].split(">")[2]

                    if content.isdecimal():
                        stuff={"kind": "literal", "val":int(content)}
                    elif content.isalnum():
                        stuff={"kind": "Identifier", "name": content}
                    else:
                        raise SyntaxError("arr aces only suports literal and identifier")

                    tmp["pos"]=stuff

                    tmp["val"] = parM(line[i][2:])

                else:
                    raise SyntaxError(line[i])
                    pass


        if tmp != {}:
            out.append(tmp)

        if consumed == 0:
            consumed+=1
        else:
            i += consumed

    return out, i

  
          

fort = [['for'], ['Let', 'TYPE>n8', 'IDENTIFIER>i', '=', 'INTEGER>0'], ['IDENTIFIER>i', '!=', 'INTEGER>4'], ['IDENTIFIER>i', '=', 'IDENTIFIER>i', '+', 'INTEGER>1'], '{', ['IDENTIFIER>x', '=', 'IDENTIFIER>x', '+', 'INTEGER>1'], '}']
fart = [['for'], ['Let', 'TYPE>n8', 'IDENTIFIER>i', '=', 'INTEGER>0'], ['IDENTIFIER>i', '==', 'INTEGER>1'], ['IDENTIFIER>i', '=', 'IDENTIFIER>i', '+', 'INTEGER>1'], '{', ['IDENTIFIER>e', '=', 'IDENTIFIER>e', '+', 'INTEGER>1'], '}']
ptrt = [['Let', 'TYPE>n8', 'IDENTIFIER>num', '=', 'INTEGER>2'], ['Let', 'TYPE>n8~', 'IDENTIFIER>ptr', '=', 'REFRENCE>num'], ['Let', 'TYPE>n32', 'IDENTIFIER>refnum', '=', 'DEREFRENCE>ptr', '+', 'INTEGER>1']]
arrt = [['Let', 'TYPE>n32', 'IDENTIFIER>num'], ['Let', 'TYPE>n32', 'IDENTIFIER>nam', '=', 'INTEGER>15'], ['Let', 'TYPE>n8[]', 'len>10', 'IDENTIFIER>nbm'], ['Let', 'TYPE>n8[]', 'IDENTIFIER>ncm', '='], '{', ['INTEGER>1', ',', 'INTEGER>2', ',', 'INTEGER>3', ',', 'INTEGER>4'], '}', ['IDENTIFIER>num', '=', 'INTEGER>10']]
arct = [['Let', 'TYPE>n32', 'IDENTIFIER>num'],['ARR>ncm>2', '=', 'INTEGER>2']]
bint = [['Let', 'TYPE>n32', 'IDENTIFIER>num'], ['IDENTIFIER>num', '=', 'INTEGER>1', '<<', 'IDENTIFIER>num'], ['IDENTIFIER>num', '=', 'INTEGER>2', '&', 'IDENTIFIER>num'], ['IDENTIFIER>num', '=', 'INTEGER>2', '|', 'IDENTIFIER>num']]
funt = [['TYPE>n32', 'FUNCT>main', '(', 'TYPE>n8', 'IDENTIFIER>na', ',', 'TYPE>n32', 'IDENTIFIER>num'], '{', ['Return', 'IDENTIFIER>na', '+', 'IDENTIFIER>num'], '}']

test = [['Let', 'TYPE>n64', 'IDENTIFIER>global', '=', 'INTEGER>1', '+', 'INTEGER>2'], ['Func', 'TYPE>void', 'FUNCT>Main', '('], '{', ['Let', 'TYPE>n64', 'IDENTIFIER>local', '=', 'INTEGER>1', '<<', 'INTEGER>1'], ['IDENTIFIER>local', '=', 'IDENTIFIER>global', '+', 'INTEGER>1'], '}']
out,lines = parse(test)
print(out)
