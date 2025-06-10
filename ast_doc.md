# AST DOC
### this is the doc on how the ast is structured and what each node has and what i means
*= wildcard
types = ["n8","n16","n32","n64","un8","un16","un32","un64", "n8~","n16~","n32~","n64~","un8~","un16~","un32~","un64~"]
ops   = ["<=",">=", "!=", "==", "!", ">", "<", "+", "-", "*", "/", "%"]
### Kind:
every node regardles of what it is has this and it and as the name entails it tells you what the node is:
#### primary
    these are primary kinds these can not acour in vals or binexp

##### letdec:
declares a variable and moves the val into it
puts the name : type in the vars dict
    {"kind":"letdec", "name": "*" "var_type":"*types", "val":"*"}
##### asing:
    updates a variable whit val
    {"kind":"asing", "name": "*", "val":"*"}

##### fcall:
    stands to generate a stand alone function call whit the return value being discarded
    param is a list of paramethers that contains secondary nodes 
    {"kind":"fcall", "name": "*", "param":[*node,*node,*node] }

##### function_dec:
    to declare a function 
    params contains the types of the args
    body contains nodes that execute on fcall
    
    {"kind":"function_dec", "name": "*", "param":[*type,*type,*type], "ret_type":*types body: [*node] }

##### if:
    well a if |:
    {"kind":"if", "exp":binexp, "body":[*node]}

##### if_else:
    well a if whit an else |:
    
    {"kind":"if_else", "exp":binexp, "body":*node, "else_body":[*node]}

##### while:
    well a while loop |:
    {"kind":"while", "exp":binexp, "body":[*node]}

##### for:
    a for loop a bit more interesting
    init is for example let n64 i = 0
    exp is the condition
    incexp is e.g the i++
    
    {"kind":"for", "exp":binexp, "init":("ledec"||"asing"), "incexp":"binexp" "body":[*node]}

#### Secondary:
    these are inside val or binexp

##### literal:
    a literal int value

    {"kind":"literal", "val": *int}

##### identifier:
    a variable 
    in the futur ading: "type": *type
    field
    
    {"kind": "Identifier", "name": "*"}

##### refrence:
    loads the memory adres of a variable

    {"kind": "refrence", "name": "*"}

##### derefrence:
    derefrence the value stored in a ptr
    
    {"kind": "derefrence", "name": "*"}
            

#### binary expresion:
    a binary operation betwen left and right specified by the op

    {"kind": "binexp", "op": "*ops", "left": *node , "right": *node}






nptr = [{"kind": "letdec", "var_type": "n8", "name": "num", "val": {"kind": "literal", "val": 2}}, {"kind": "letdec", "var_type": "n8~", "name": "ptr", "val": {"kind": "refrence", "name": "num"}}, {"kind": "letdec", "var_type": "n32", "name": "refnum", "val": {"kind": "binexp", "op": "+", "left": {"kind": "derefrence", "name": "ptr"}, "right": {"kind": "literal", "val": 1}}}]

init = {"kind": "asing", "name": "y", "val": {"kind": "binexp", "op": "+", "left": {"kind": "Identifier", "name": "y"}, "right": {"kind": "literal", "val": 1}}}    
