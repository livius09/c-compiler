import json


#parser
[
  {
    "type": "LetDeclaration",
    "var_type": "n32",
    "name": "x",
    "value": {
      "type": "Literal",
      "value": 5
    }
  },
  {
    "type": "ReturnStatement",
    "value": {
      "type": "Identifier",
      "name": "x"
    }
  }
]

#FunctionDeclaration(
#    name = "plus",
#    parameters = [
#        Parameter(type="n64", name="a"),
#        Parameter(type="n64", name="b")
#    ],
#    body = [
#        ReturnStatement(
#            value = BinaryExpression(
#                left = Identifier("a"),
#                operator = "+",
#                right = Identifier("b")
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

def parse(line):
  operations=["+","-","*","/","="]
  out = []
  i=0
  
  while (i < len(line)):
    
    tmp = {}
    match line[i][0]:
        
      case "}":
        break
       
      
      case "let":
        
        tmp["type"] = "letdec"
        tmp["var_type"] = line[i][1].split(">")[1]
        math_part = line[i][line[i].index('=') + 1:]

        value={}
        math_part = line.split("=")[1]

        if len(math_part) == 1:
          if math_part[0].startswith("IDENTIFIER>"):
            value["type"] = "IDENTIFIER"
            value["name"] = math_part[0].split(">")[1]

          elif  math_part[0].startswith("INTEGER>"):
            value["type"] = "INTEGER"
            value["val"] = int(math_part[0].split(">")[1])
          
          tmp["val"] = value
        else:
          tmp["val"]=parM(math_part)
        
      case "func":
        
        tmp["type"] = "function_dec"
        tmp["name"] = line[i][2]
        tmp["parameter"]=[]
        for a in range(1,int(len(line[i])-2),2):
          tmp["para"].append({"type":line[i][a].split(">")[1],"name":line[i][a+1].split(">")[1]})

        tmp["body"] = parse(line[i+1:])

      case "return":
        tmp["type"]="return"
        tmp["val"] = parM(line[i][2:])

      case "if":
        tmp["type"] = "IF"
        tmp["epx"]=parM(line[i+1:])
        tmp["body"]=parse(line[i+1:])

    if line[i][0].startswith("IDENTIFIER>"):
      tmp["type"] = "asing"
      tmp["val"]=parM(line[i][2:])
    
    if line[i][0].startswith("FUNCT>"):
      tmp["type"] = "fcall"
      tmp["para"]=[]

      ofset=0
      while(ofset<(len(line[i])-1)):
        pass
         

       

    i+=1
    out.append(tmp)
  return out
  
          
lal=[['Let', 'TYPE>n64', 'IDENTIFIER>x', '=', 'INTEGER>1'],['Let', 'TYPE>n64', 'IDENTIFIER>y', '=', 'INTEGER>1']]       


print(parse(lal)[1].items())



def parM(tokens):
    def parse_primary(token):
        if token.startswith("INTEGER>"):
            return {"type": "Literal", "value": int(token.split(">")[1])}
        elif token.startswith("IDENTIFIER>"):
            return {"type": "Identifier", "name": token.split(">")[1]}
        else:
            raise ValueError(f"Unexpected token: {token}")

    def parse_expression(tokens, precedence=0):
        if not tokens:
            return None

        left = parse_primary(tokens.pop(0))

        while tokens:
            op = tokens[0]
            op_prec = get_precedence(op)

            if op_prec < precedence:
                break

            tokens.pop(0)  # remove operator
            right = parse_expression(tokens, op_prec + 1)

            left = {
                "type": "BinaryExpression",
                "operator": op,
                "left": left,
                "right": right
            }

        return left

    def get_precedence(op):
        if op in ("*", "/"):
            return 2
        elif op in ("+", "-"):
            return 1
        return 0

    # make a copy of the list to avoid modifying the original
    return parse_expression(tokens[:])
