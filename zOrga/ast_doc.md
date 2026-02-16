# AST DOC
### this is the doc on how the ast is structured and what each node has and what i means
*= wildcard
types = ["n8","n16","n32","n64","un8","un16","un32","un64", "n8~","n16~","n32~","n64~","un8~","un16~","un32~","un64~"]

ops   = ["<=",">=", "!=", "==", "!", ">", "<", "+", "-", "*", "/", "%","&", "|", "^",]
### Kind:
every node regardles of what it is has this and it and as the name entails it tells you what the node is:
#### primary:
these are primary kinds these can not acour in vals or binexp

#### letinit:
declares a variable and moves the val into it
puts the name : type in the vars dict

    {"kind":"letinit", "name": "*", "var_type":"*types", "val":"*"}
    {"kind":"letinit", "name": "*", "var_type":"*types", "val":[*literal], "len": *n}

#### letdec:
only creates space for the variable 
puts the name : type in the vars dict

    {"kind":"letdec", "name": "*" "var_type":"*types"}
    {"kind":"letdec", "name": "*" "var_type":"*types", "len": *n}

#### asing:
updates a variable whit val

    {"kind":"asing", "acces": *, "val":"*"}

#### fcall:
stands to generate a stand alone function call whit the return value being discarded
param is a list of paramethers that contains secondary nodes

    {"kind":"fcall", "name": "*", "param":[*node,*node,*node] }

#### function_dec:
to declare a function 
params contains the types of the args and theyr name
body contains nodes that execute on fcall
    
    {"kind":"function_dec", "name": "*", "param":[*type,*type,*type], "ret_type":*types "body": [*node] }

#### struct_def:
to declare a structure
in the may contain funtion_dec

    {"kind":"struct_dec", "name": "*", "members":[
        {"kind":"letinit", "name": "*", "var_type":"*types", "val":"*"}
        OR
        {"kind":"letdec", "name": "*" "var_type":"*types"}

        ]
    }

#### if:
well a if |:
the else body is optional but this makes it one ast variante now two

    {"kind":"if", "exp":binexp, "body":[*node] "else_body":[*node]}


#### while:
well a while loop |:

    {"kind":"while", "exp":binexp, "body":[*node]}

#### for:
a for loop a bit more interesting
init is for example let n64 i = 0
exp is the condition
incexp is e.g the i++
    
    {"kind":"for", "exp":binexp, "init":("ledec"||"asing"), "incexp":binexp , "body":[*node]}

#### return:
well just the return expresion

    {"kind":"ret", "val": (binexp || int)}

### Secondary:
these are inside val or binexp

#### literal:
a literal int value

    {"kind":"literal", "val": *int}

#### identifier:
a variable 
in the futur ading: "type": *type
field
    
    {"kind": "Identifier", "acces": "*"}

#### acces:
array, pointer or struct acces
{'kind': 'acces', "base": {"kind": "", "name": ""},
  "access": [
    {"kind": ""}
  ]
}
    ##### Access = {
        {"kind":"field"  "name": str},
        {"kind" : "index":  "expr": node},
        {"kind":"fcall", "fname": str , "params" }
    }

            

#### binary expresion:
a binary operation betwen left and right specified by the op

    {"kind": "binexp", "op": "*ops", "left": *node , "right": *node}

#### unary expresion:
a unary opperation like !, ~ or &

    {"kind": "uniexp", "op": "*ops", "exp": *node }



### locals:
for the locals of the curent scope
pos indicates the ofset to rbp
size in bytes of the whole thing
    {x:{type:n32, ofs:2, size:4}, arr:{type:n16[], ofs:10, len:4, size:8}}

### globals:
for the globals
    {x:{type:n32, size:4}, arr:{type:n16[], len:4, size:8}}

### structs:
user declared types in the form of structs
    { 
        "human":{
                "size":9 ,
                "mebers":
                        {"age":"un8", "money":"n64"}    
                }
    }


### example:
[{"kind": "letdec", "var_type": "n8", "name": "num", "val": {"kind": "literal", "val": 2}}, 
{"kind": "letdec", "var_type": "n8~", "name": "ptr", "val": {"kind": "refrence", "name": "num"}}, 
{"kind": "letdec", "var_type": "n32", "name": "refnum", "val": {"kind": "binexp", "op": "+", "left": {"kind": "derefrence", "name": "ptr"}, "right": {"kind": "literal", "val": 1}}}]

{"kind": "asing", "name": "y", "val": {"kind": "binexp", "op": "+", "left": {"kind": "Identifier", "name": "y"}, "right": {"kind": "literal", "val": 1}}}    
