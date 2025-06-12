import sys
i=1.1
a=11
arEr=[1,2,3]
cond = bool(True)

print(sys.getsizeof(i))
print(sys.getsizeof(a))
print(sys.getsizeof(arEr))
print(sys.getsizeof(cond))


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
        else:
            raise ValueError(f"Unexpected token: {token}")

    def get_precedence(op):
        return {
            '<=' :1,
            '>=' :1,
            '!=' :1,
            '==' :1,
            '!'  :1,
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
            elif op == '>=':
                result = int(a >= b)

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


#important paradigma desing stuff

line = ["INTEGER>1", ",", "INTEGER>2", "+", "INTEGER>1", ",", "INTEGER>4"]
arr = []


chunks = []
current = []

for token in line:
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

print(arr)

def is_arr_type(test:str):
    var_types=["n8","n16","n32","n64","un8","un16","un32","un64",     
             "n8~","n16~","n32~","n64~","un8~","un16~","un32~","un64~"]
    return test.endswith("[]") and (test[:-2] in var_types )

print(is_arr_type("n8[]"))
print(is_arr_type("n8["))
print(is_arr_type("n8]"))
print(is_arr_type("n[]"))
