def formulate_math(node:dict, context="asing"): #asing, cond
    nodetype = node['type']

    if nodetype == "Identifier":
        return [f"mov rax [{node['name']}]"]
    
    if nodetype == "Literal":
        return [f"mov rax {node['val']}"]
    
    if nodetype == "Fcall":
        return formulate_fcals(node,context)

    if nodetype == "BinExp":
        code = []
        cmpops=["==","!=","<",">","<=",">="]

        code += formulate_math(node['left'],context)
        code.append("push rax")
        code += formulate_math(node['right'],context)
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
        elif op in cmpops:
            code.append("cmp rax rbx")
            if context == "asing":
                set_instr = {
                        "==": "sete al",
                        "!=": "setne al",
                        "<": "setl al",
                        "<=": "setle al",
                        ">": "setg al",
                        ">=": "setge al"
                    }[op]
                code.append(f"{set_instr}")
                code.append("movzx rax, al")
            
        else:
            raise SyntaxError("uknown operation: "+op)
        
        return code

def formulate_fcals(node:dict):    #genertate code for function calls and checking the parameter types
    code=[]
    fname = node['name']
    if fname in functions.keys():
        params = node['para']
        dectypes = functions[fname]
        
        for i in range(len(params)):

            curtype = params[i]['type']

            if curtype == "BinExp":
                code.extend(formulate_math)
                code.append(f"mov {regs[i]} , rax")
            elif curtype == "Identifier":
                
                varname = params[i]['name']
                vartype = vars[varname]

                if dectypes[i] == vartype:
                    code.append(f"mov {regs[i]} [{varname}]")

                else:
                    raise TypeError(f"expected type {dectypes[i]} but got {vartype} on arg {i} of function call {fname}")

            elif curtype == "Literal":
                code.append(f"mov {regs[i]} {params[i]['val']}")

        code.append(f"call .{fname}")


    else:
        raise SyntaxError(f"functions {fname} has not been declared")




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
vars={"x" : "n8"}         #x:n8    contains the var name as key and type as value
functions={}    #print:[char[],n64]    contains the function name as key and the value is the types of the parameter in order
regs= ['edi","esi","edx","ecx","r8d","r9d']    #the regs for giving over function arguments
data=[]         #data section of asm


def label_gen():
    num = 0
    while True:
        yield num
        num+=1 

iflockup={"==": "jne",
          "!=": "je" ,
          "<" : "jle",
          ">" : "jg" ,
          }


def gen(a:list[dict]):
    text=[]         #text section so the actual executed asm
    
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


            case "asing":    #genreate code for the normal "x = y+1" statements
                name = node['name']
                curtype = node['val']['type']
                if name in vars.keys():
                    if curtype == "Literal":
                        text.append(f"mov [{name}] , {node['val']['val']}")

                    elif curtype == "BinExp":
                        text.extend(formulate_math(node['val']))
                        text.append(f"mov [{name}] , rax")

                    elif curtype == "Identifier":
                        text.append(f"mov rax , [{node['val']['name']}]")
                        text.append(f"mov [{node['name']}] , rax")

                    elif curtype == "Fcall":
                        text.extend(formulate_fcals(node['val']))
                        text.append(f"mov [{name}] , rax")


                else:
                    raise SyntaxError(f"variable:{name} has not been declared")

            case "fcall":    
                formulate_fcals(node)


                
            case "function_dec":
                params = node["param"]
                fname = node['name']

                if len(params) > len(regs):
                    raise SyntaxError("to many args")
                else:
                    text.apend(f".{fname}:")
                    text.extend(gen(node["body"]))
            
            case "if":
                
                text.extend(formulate_math(node["exp"],"cond"))

                lnum = next(label_gen)
                

                text.append(f'{iflockup[node["exp"]["op"]]} .L{lnum}')      #jne .L1
                
                text.extend(gen(node["body"]))
                
                text.append(f".L{lnum}:")
                

            case "if_else":
                text.extend(formulate_math(node["exp"],"cond"))
                endl = label_gen()
                
                elsel= label_gen()

                text.append(f'{iflockup[node["exp"]["op"]]} .L{lnum}')      #jne .L1
                text.extend(gen(node["body"]))
                text.append(f"jmp .L{endl}")

                text.append(f".L{elsel}:")
                text.extend(gen(node["else_body"]))

                text.append(f".L{endl}:")

            case "while":
                pass

    return text




             
init = {'type': 'asing', 'name': 'y', 'val': {'type': 'BinExp', 'op': '+', 'left': {'type': 'Identifier', 'name': 'y'}, 'right': {'type': 'Literal', 'val': 1}}}    
nif=[{'type': 'if', 'exp': {'type': 'BinExp', 'op': '==', 'left': {'type': 'Identifier', 'name': 'x'}, 'right': {'type': 'Literal', 'val': 2}}, 'body': [{'type': 'asing', 'name': 'x', 'val': {'type': 'Literal', 'val': 2}}]}]      
print(gen(nif))



