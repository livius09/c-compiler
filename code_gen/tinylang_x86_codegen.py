#.text	Program code (instructions)
#.rodata	Read-only data like string literals
#.data	Initialized global and static variables
#.bss	Uninitialized globals/statics (zero-initialized)
#.plt	Procedure Linkage Table (for dynamic linking)
#.got	Global Offset Table (for dynamic linking)

#section .data
#   x dq 0
#   y dq 0

#ecx 
#edx 
#esi 
#edi
vars={}         #x:n8    contains the var name as key and type as value
functions={}    #print:[char[],n64]    contains the function name as key and the value is the types of the parameter in order


def gen(a:list[dict]):
    data=[]         #data section of asm
    text=[]         #text section so the actual executed asm
    regs= ['edi","esi","edx","ecx","r8d","r9d']    #the regs for giving over function arguments

    for node in a:
        match node['type']:
            
            case "letdec":    #if its a let decl add the name and type to the vars dict if theyr already in there from and eror and generate the code for putting the value in
                identify =node['name']
                vartype = node['vartype']
                if identify in vars.keys():
                    raise SyntaxError("variable has already been declared")
                else:
                    vars[identify] = vartype

                dotype = node['val']['type']

                if dotype == "Literal":
                    data.append(f"{node['name']} dq {node['val']['val']}")
                elif dotype == "identifier":
                    data.append(f"{node['name']} dq {node['val']['val']}")

                    text.append(f"mov rax , [{identify}]")
                    text.append(f"mov [{node['name']}] , rax")


            case "asing":    #genreate code for the normal "x=y+1" statements
                name = node['name']
                curtype = node['val']['type']
                if name in vars.keys():
                    if curtype == "Literal":
                        text.append(f"mov [{name}] , {node['val']['val']}")
                    elif curtype == "BinExp":
                        formulate_math(node['val'])
                        text.append(f"mov [{name}] , rax")

                    
                    elif curtype == "Identifier":
                        text.append(f"mov rax , [{node['val']['name']}]")
                        text.append(f"mov [{node['name']}] , rax")


                else:
                    raise SyntaxError("variable has not been declared")

            case "fcall":    #genertate code for function calls and checking the parameter types
                fname = node['name']
                if fname in functions.keys():
                    params = node['para']
                    dectypes = functions[fname]
                    
                    for i in range(len(params)):

                        curtype = params[i]['type']

                        if curtype == "BinExp":
                            pass
                        elif curtype == "Identifier":
                            
                            varname = params[i]['name']
                            vartype = vars[varname]

                            if dectypes[i] == vartype:
                                text.append(f"mov {regs[i]} [{varname}]")

                            else:
                                raise TypeError(f"expected type {dectypes[i]} but got {vartype} on arg {i} of function call {fname}")

                        elif curtype == "Literal":
                            text.append(f"mov {regs[i]} {params[i]['val']}")


                    else:
                        raise SyntaxError(f"functions {fname} has not been declared")


                
            case "function_dec":

                if len(params) > len(regs):
                    raise SyntaxError("to many args")
             
init = {'type': 'asing', 'name': 'y', 'val': {'type': 'BinExp', 'op': '+', 'left': {'type': 'Identifier', 'name': 'y'}, 'right': {'type': 'Literal', 'val': 1}}}          

def formulate_math(node:dict):
    if node['type'] == "Identifier":
        return [f"mov rax [{node['name']}]"]
    
    if node['type'] == "Literal":
        return [f"mov rax {node['val']}"]

    if node['type'] == "BinExp":
        code = []

        code += formulate_math(node['left'])
        code.append("push rax")
        code += formulate_math(node['right'])
        code.append("pop rbx")

        op = node['op']
        if op == "+":
            code.append("add rax rbx")
        elif op == "-":
            code.append("sub rax rbx")
        elif op == "*":
            code.append("imul rax rbx")
        elif op == "/":
            code.extend(["cqo",                    #sign-extend RAX into RDX:RAX
                        "idiv rbx"               # result: quotient in RAX, remainder in RDX
                        ])
        elif op == "%":
            code.extend(["cqo",                    #sign-extend RAX into RDX:RAX
                        "idiv rbx",               # result: quotient in RAX, remainder in RDX
                        "mov rax rdx"
                        ])

        else:
            raise SyntaxError("uknown operation: "+op)
        
        return code


print(formulate_math(init['val']))
