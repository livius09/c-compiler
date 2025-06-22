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

#big holly bomboclat
tokens = ['ARR>ncm', '[', 'INTEGER>1', '+', 'INTEGER>1', ']']
start = tokens.index('[')
end = tokens.index(']')
content = tokens[start + 1:end]
print(content)  # ['INTEGER>1', '+', 'INTEGER>1']

"".isalnum()
def size_lookup(lok_type:str):
    types={"n8":1,"n16":2,"n32":4,"n64":8,"un8":1,"un16":2,"un32":4,"un64":8,   "n8~":8,"n16~":8,"n32~":8,"n64~":8,"un8~":8,"un16~":8,"un32~":8,"un64~":8}
    if lok_type in types.keys() or (lok_type.endswith("[]") and lok_type[:-2] in types):
        if (lok_type.endswith("[]")):
            return types[lok_type[:-2]]
        else:
            return types[lok_type]
    else:
        raise SyntaxError(f"var type {lok_type} doese not exist")

def get_mov_size(var_type:str)->str:
            #   0       1           2       3       4        5    6   7      8
        return ["", "BYTE PTR", "WORD PTR", "", "DWORD PTR", "", "", "", "QWORD PTR"][size_lookup(var_type)]

print(get_mov_size("n32"))


ofset_table = []

# ANSI escape background colors
bg_colors = [
    '\033[41m',  # Red
    '\033[42m',  # Green
    '\033[43m',  # Yellow
    '\033[44m',  # Blue
    '\033[45m',  # Magenta
    '\033[46m',  # Cyan
    '\033[47m',  # White
    '\033[100m', # Grey
]
RESET = '\033[0m'

def add_ofset_table(node: dict):
    var_type = node['var_type']
    var_name = node['var_name']
    type_size = size_lookup(var_type)
    if is_arr_type(var_type):
        var_len = node['len']
        for i in range(var_len):
            for k in range(type_size):
                ofset_table.append(f"{var_name}[{i}] byte:{k}")
    else:
        for j in range(type_size):
            ofset_table.append(f"{var_name} byte:{j}")

def print_ofst():
    color_map = {}
    color_index = 0
    index=0

    for entry in ofset_table:
        index-=1
        # Extract the array/group prefix (like a[0], a[1], or just a)
        if '[' in entry:
            prefix = entry.split('[')[0]  # Get the base name like 'arr' from 'arr[0] byte:1'
        else:
            prefix = entry.split(' ')[0]  # Just the variable name

        # Assign a background color for the entire array or var
        if prefix not in color_map:
            color_map[prefix] = bg_colors[color_index % len(bg_colors)]
            color_index += 1

        color = color_map[prefix]
        print(str(index)+"\t" + color + entry + RESET)

# --- Mock helpers ---
def size_lookup(var_type):
    return {"int": 4, "char": 1, "float": 4}.get(var_type.replace("[]", ""), 1)

def is_arr_type(var_type):
    return var_type.endswith("[]")

# --- Test example ---
add_ofset_table({"var_name": "a", "var_type": "int", "size": 4})
add_ofset_table({"var_name": "b", "var_type": "char[]", "len": 3, "size": 1})
add_ofset_table({"var_name": "c", "var_type": "float[]", "len": 2, "size": 4})
print_ofst()



abc={"x":{"name":2,"type":4},"e":{"name":4,"type":7}}

def get_fart(nam:str):
    return abc[nam]

get_fart("x")["name"]="ligma"

print(abc)