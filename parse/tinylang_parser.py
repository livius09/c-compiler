

#parser
[
  {
    "type": "LetDeclaration",
    "var_type": "n32",
    "name": "x",
    "val": {
      "type": "Literal",
      "val": 5
    }
  },
  {
    "type": "ReturnStatement",
    "val": {
      "type": "Identifier",
      "name": "x"
    }
  }
]

#not mine
def parM(tokens: list):
    print(tokens)
    def parse_primary(token):
        if token.startswith("INTEGER>"):
            return {"type": "Literal", "val": int(token.split(">")[1])}
        elif token.startswith("IDENTIFIER>"):
            return {"type": "Identifier", "name": token.split(">")[1]}
        else:
            raise ValueError(f"Unexpected token: {token}")

    def get_precedence(op):
        return {
            '!=':1,
            '==':1,
            '!': 1,
            '>': 1,
            '<': 1,
            '+': 2,
            '-': 2,
            '*': 3,
            '/': 3,
            '%': 3,
        }.get(op, -1)  # Unknown ops = very low precedence

    def fold_constants(left, op, right):
    # If both sides are integer literals: constant fold
      if left["type"] == "Literal" and right["type"] == "Literal":
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
          elif op == '>=':
              result = int(a >= b)

          # Return folded literal if result was computed
          if result is not None:
              return {"type": "Literal", "val": result}

      # Algebraic simplification with 0 or 1
      if op == '+' and right["type"] == "Literal" and right["val"] == 0:
          return left
      if op == '+' and left["type"] == "Literal" and left["val"] == 0:
          return right

      if op == '-' and right["type"] == "Literal" and right["val"] == 0:
          return left

      if op == '*' and ((left["type"] == "Literal" and left["val"] == 0) or
                        (right["type"] == "Literal" and right["val"] == 0)):
          return {"type": "Literal", "val": 0}

      if op == '*' and right["type"] == "Literal" and right["val"] == 1:
          return left
      if op == '*' and left["type"] == "Literal" and left["val"] == 1:
          return right

      if op == '/' and right["type"] == "Literal" and right["val"] == 1:
          return left

      # Not foldable
      return {
          "type": "BinExp",
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
#                left = Identifier("a"),
#                op = "+",
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
              tmp["type"] = "letdec"
              tmp["name"] = line[i][2].split(">")[1]
              tmp["var_type"] = line[i][1].split(">")[1]

              math_part = line[i][line[i].index('=') + 1:]

              if len(math_part) == 1:
                  value = {}
                  if math_part[0].startswith("IDENTIFIER>"):
                      value["type"] = "IDENTIFIER"
                      value["name"] = math_part[0].split(">")[1]
                  elif math_part[0].startswith("INTEGER>"):
                      value["type"] = "INTEGER"
                      value["val"] = int(math_part[0].split(">")[1])
                  tmp["val"] = value
              else:
                  tmp["val"] = parM(math_part)

          case "func":
              tmp["type"] = "function_dec"
              tmp["name"] = line[i][2]
              tmp["parameter"] = []
              for a in range(1, len(line[i]) - 2, 2):
                  tmp["parameter"].append({
                      "type": line[i][a].split(">")[1],
                      "name": line[i][a+1].split(">")[1]
                  })

              body, body_consumed = parse(line[i+1:])
              tmp["body"] = body
              consumed += body_consumed

          case "return":
              tmp["type"] = "return"
              tmp["val"] = parM(line[i][2:])

          case "if":
              tmp["type"] = "if"
              tmp["exp"] = parM(line[i][1:])
              body, body_consumed = parse(line[i+2:])
              tmp["body"] = body
              consumed += 2 + body_consumed  # +2 for 'If' line and '{' line

          case _:
              if line[i][0].startswith("IDENTIFIER>"):
                  tmp["type"] = "asing"
                  tmp["name"] = line[i][0].split(">")[1]
                  tmp["val"] = parM(line[i][2:])
              elif line[i][0].startswith("FUNCT>"):
                  tmp["type"] = "fcall"
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

      out.append(tmp)
      i += consumed

  return out, i

  
          
lal=[['Let', 'TYPE>n64', 'IDENTIFIER>x', '=', 'INTEGER>1'],['Let', 'TYPE>n64', 'IDENTIFIER>y', '=', 'INTEGER>1']]       
lol=[['IDENTIFIER>y', '=','IDENTIFIER>y',"+", 'INTEGER>1',"*", 'INTEGER>1']]
lla=[['If', 'IDENTIFIER>x', '==', 'INTEGER>2'], '{', ['IDENTIFIER>x', '=', 'INTEGER>1',"+",'INTEGER>1'], '}']

out,lines=parse(lla)
print(out)
