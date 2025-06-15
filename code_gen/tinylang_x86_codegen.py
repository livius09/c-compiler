def formulate_math(node:dict, context="asing"): #asing, cond
    nodetype = node['kind']
    
    if nodetype == "Identifier":
        return [f"mov rax, [{node['name']}]"]
    
    if nodetype == "literal":
        return [f"mov rax, {node['val']}"]

    if nodetype == "refrence":
        return [f"lea rax, {node['name']}"]
    
    if nodetype == "derefrence":
       return [f"mov rax, [{node['name']}]",  # rax = address of pointee
                "mov rax, [rax]"]             # rax = value at that address
    
    if nodetype == "Fcall":
        return formulate_fcals(node)

    if nodetype == "binexp":
        code = []
        cmpops=["==","!=","<",">","<=",">="]

        code += formulate_math(node['left'],context)
        code.append("push rax")
        code += formulate_math(node['right'],context)
        code.append("pop rbx")

        op = node['op']
        if op == "+":
            code.append("add rax, rbx")
        elif op == "-":
            code.append("sub rax, rbx")
        elif op == "*":
            code.append("imul rax, rbx")
        elif op == "/":
            code.extend(["cqo",                    #sign-extend RAX into RDX:RAX
                        "idiv rbx"               # result: quotient in RAX, remainder in RDX
                        ])
        elif op == "%":
            code.extend(["cqo",                    #sign-extend RAX into RDX:RAX
                        "idiv rbx",               # result: quotient in RAX, remainder in RDX
                        "mov rax, rdx"
                        ])
        elif op in cmpops:
            code.append("cmp rax, rbx")
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

            curtype = params[i]['kind']

            if curtype == "binexp":
                code.extend(formulate_math)
                code.append(f"mov {regs[i]}, rax")
            elif curtype == "Identifier":
                
                varname = params[i]['name']
                vartype = vars[varname]

                if dectypes[i] == vartype:
                    code.append(f"mov {regs[i]}, [{varname}]")

                else:
                    raise TypeError(f"expected type {dectypes[i]} but got {vartype} on arg {i} of function call {fname}")

            elif curtype == "literal":
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
vars={}         #x:n8    contains the var name as key and type as value
functions={}    #print:[char[],n64]    contains the function name as key and the value is the types of the parameter in order
regs= ["edi","esi","edx","ecx","r8d","r9d"]    #the regs for giving over function arguments
data=[]         #data section of asm
var_types=["n8","n16","n32","n64","un8","un16","un32","un64",     
             "n8~","n16~","n32~","n64~","un8~","un16~","un32~","un64~"]

def size_lookup(lok_type:str):
    types={"n8":1,"n16":2,"n32":4,"n64":8,"un8":1,"un16":2,"un32":4,"un64":8,     "n8~":8,"n16~":8,"n32~":8,"n64~":8,"un8~":8,"un16~":8,"un32~":8,"un64~":8}
    if (lok_type.endswith("[]")):
        return types[lok_type[:-2]]
    else:
        return types[lok_type]


def is_arr_type(test:str):
    return test.endswith("[]") and (test[:-2] in var_types )

def label_generator():
    num = 0
    while True:
        yield num
        num+=1 

label_gen = label_generator()


iflockup={"==": "jne",
          "!=": "je" ,
          "<" : "jle",
          ">" : "jg" ,
          }

looplockup = {"==": "je",
              "!=": "jne",
              "<":  "jg",
              ">":  "jle"
              }


def gen(a:list[dict],scope=True):   #true is global false is local
    text=[]         #text section so the actual executed asm
    


    
    for node in a:
        match node['kind']:
            
            case "letinit":    #if its a let decl add the name and type to the vars dict if theyr already in there from and eror and generate the code for putting the value in
                var_name =node['name']
                vartype = node['var_type']
                if var_name in vars.keys():
                    raise SyntaxError(f"variable: {var_name} has already been declared")
                else:
                    vars[var_name] = vartype

                if  not is_arr_type(vartype):
                    dotype = node['val']['kind']
                else:
                    dotype = ""

                if dotype == "literal":
                    data.append(f"{var_name} dq {node['val']['val']}")

                elif dotype == "identifier":
                    data.append(f"{var_name} dq 0")

                    text.append(f"mov rax , [{var_name}]")
                    text.append(f"mov [{var_name}] , rax")

                elif dotype == "binexp":
                    data.append(f"{var_name} dq 0")
                    
                    text.extend(formulate_math(node['val']))
                    text.append(f"mov [{var_name}], rax")

                elif dotype == "refrence":
                    data.append(f"{var_name} dq 0")

                    text.append(f"lea rax, [{node['val']['name']}]")
                    text.append(f"mov [{var_name}], rax")

                elif dotype == "derefrence":
                    data.append(f"{var_name} dq 0")
                    print("ligma sigma")
                    text.append(f"mov rax, [{node['name']}]")  # rax = address of pointee
                    text.append("mov rax, [rax]")              # rax = value at that address
                    text.append(f"mov [{var_name}], rax")

                elif is_arr_type(vartype):
                    vars[var_name] = vartype
                    if is_arr_type(vartype):
                        data.append(var_name+":")
                        for nana in node['val']:
                            if nana["kind"] == "literal":
                                data.append(f"\t.long \t {nana['val']}")

            case "letdec":
                var_name =node['name']
                vartype = node['var_type']
                if (var_name in vars.keys()):
                    raise SyntaxError(f"variable: {var_name} has already been declared")
                else:
                    vars[var_name] = vartype
                    if is_arr_type(vartype):
                        pass

                    else:
                        
                        vars[var_name] = vartype
                        data.append(f"{var_name} dq 0")

            case "asing":    #genreate code for the normal "x = y+1" statements
                write_name = node['name']
                dotype = node['val']['kind']
                if write_name in vars.keys():
                    if dotype == "literal":
                        text.append(f"mov [{write_name}], {node['val']['val']}")

                    elif dotype == "binexp":
                        text.extend(formulate_math(node['val']))
                        text.append(f"mov [{write_name}], rax")

                    elif dotype == "identifier":
                        text.append(f"mov rax, [{node['val']['name']}]")
                        text.append(f"mov [{write_name}], rax")

                    elif dotype == "Fcall":
                        text.extend(formulate_fcals(node['val']))
                        text.append(f"mov [{write_name}], rax")

                    elif dotype == "refrence":
                        text.append(f"lea rax {node['val']['name']}")
                        text.append(f"mov [{write_name}], rax")

                    elif dotype == "derefrence":
                        text.append(f"mov rdx, [{node['val']['name']}]")
                        text.append("mov rax, [rdx]")
                        text.append(f"mov [{write_name}], rax")
                    elif dotype=="arrac":
                        
                        #{'kind': 'asing', 'name': 'num', 'val': {'kind': 'arrac', 'name': 'ncm', 'pos': {'kind': 'literal', 'val': 1}}}

                        if node["val"]["pos"]["kind"] == "literal":
                            print(node)
                            read_name = node["val"]['name']
                            pos = node["val"]["pos"]["val"]
                            pos*=size_lookup(vars[read_name])
                            text.append(f"mov rax, {read_name}[rip+{pos}]")
                            text.append(f"mov [{write_name}], rax")

                        elif  node["val"]["pos"]["kind"] == "identifier":
                            #mov eax, lala[0+rax*4]
                            read_name = node["val"]['name']
                            size = size_lookup(vars[node["val"]["name"]])
                            text.append(f"mov rax, [{node['val']['pos']['name']}]")
                            text.append(f"mov rax, {read_name}[0+rax*{size}]")
                            text.append(f"mov [{write_name}], rax")
                            
                        else:
                            raise("nicht skibidy")


                else:
                    raise SyntaxError(f"variable:{write_name} has not been declared")

            case "fcall":    
                formulate_fcals(node)


                
            case "function_dec":
                params = node["param"]
                fname = node['name']

                if len(params) > len(regs):
                    raise SyntaxError("to many args in function: " + fname)
                else:
                    functions[fname]= params

                    text.append(f".{fname}:")
                    text.extend(gen(node["body"]))
            
            case "if":
                
                text.extend(formulate_math(node["exp"],"cond"))

                lnum = next(label_gen)
                

                text.append(f'{iflockup[node["exp"]["op"]]} .L{lnum}')      #jne .L1
                
                text.extend(gen(node["body"]))
                
                text.append(f".L{lnum}:")
                

            case "if_else":
                text.extend(formulate_math(node["exp"],"cond"))
                endl = next(label_gen)
                
                elsel= next(label_gen)

                text.append(f'{iflockup[node["exp"]["op"]]} .L{lnum}')      #jne .L1
                text.extend(gen(node["body"]))
                text.append(f"jmp .L{endl}")

                text.append(f".L{elsel}:")
                text.extend(gen(node["else_body"]))

                text.append(f".L{endl}:")

            case "while":
                endla = next(label_gen)
                startla =next(label_gen)
                text.append(f"jmp .L{endla}")
                text.append(f".L{startla}")
                text.extend(gen(node["body"]))
                text.append(f".L{endla}")
                text.extend(formulate_math(node["exp"],"cond"))
                text.append(f'{looplockup[node["exp"]["op"]]} .L{startla}')

            case "for":
                endla = next(label_gen)
                startla =next(label_gen)

                text.extend(gen([node["init"]]))
                text.append(f"jmp .L{endla}")
                text.append(f".L{startla}")

                text.extend(gen(node["body"]))

                text.extend(gen(node["incexp"]))
                text.append(f".L{endla}")
                text.extend(formulate_math(node["exp"],"cond"))
                text.append(f'{looplockup[node["exp"]["op"]]} .L{startla}')
            
            case _:
                pass #raise SyntaxError("ligma")

    return text




             
init = {'kind': 'asing', 'name': 'y', 'val': {'kind': 'binexp', 'op': '+', 'left': {'kind': 'Identifier', 'name': 'y'}, 'right': {'kind': 'literal', 'val': 1}}}    
nif  = [{'kind': 'if', 'exp': {'kind': 'binexp', 'op': '==', 'left': {'kind': 'Identifier', 'name': 'x'}, 'right': {'kind': 'literal', 'val': 2}}, 'body': [{'kind': 'asing', 'name': 'x', 'val': {'kind': 'literal', 'val': 2}}]}]      
nfor = [{'kind': 'for', 'init': {'kind': 'letinit', 'name': 'i', 'var_type': 'n8', 'val': {'kind': 'literal', 'val': 0}}, 'exp': {'kind': 'binexp', 'op': '==', 'left': {'kind': 'Identifier', 'name': 'i'}, 'right': {'kind': 'literal', 'val': 1}}, 'incexp': [{'kind': 'asing', 'name': 'i', 'val': {'kind': 'binexp', 'op': '+', 'left': {'kind': 'identifier', 'name': 'i'}, 'right': {'kind': 'literal', 'val': 1}}}], 'body': [{'kind': 'asing', 'name': 'x', 'val': {'kind': 'binexp', 'op': '+', 'left': {'kind': 'Identifier', 'name': 'x'}, 'right': {'kind': 'literal', 'val': 1}}}]}]
nptr = [{'kind': 'letinit', 'var_type': 'n8', 'name': 'num', 'val': {'kind': 'literal', 'val': 2}}, {'kind': 'letinit', 'var_type': 'n8~', 'name': 'ptr', 'val': {'kind': 'refrence', 'name': 'num'}}, {'kind': 'letinit', 'var_type': 'n32', 'name': 'refnum', 'val': {'kind': 'binexp', 'op': '+', 'left': {'kind': 'derefrence', 'name': 'ptr'}, 'right': {'kind': 'literal', 'val': 1}}}]
narr = [{'var_type': 'n32', 'name': 'num', 'kind': 'letdec'}, {'var_type': 'n8[]', 'name': 'ncm', 'kind': 'letinit', 'size': 4, 'val': [{'kind': 'literal', 'val': 1}, {'kind': 'literal', 'val': 2}, {'kind': 'literal', 'val': 3}, {'kind': 'literal', 'val': 4}]}, {'kind': 'asing', 'name': 'num', 'val': {'kind': 'arrac', 'name': 'ncm', 'pos': {'kind': 'identifier', 'name': 1}}}]

out = gen(narr)
print(vars)
print(data)
print(out)

with open("./code_gen/readout.txt","w") as file:
    file.write("data:\n")
    for b in data:
        file.write("\t"+b+"\n")
    file.write("text:\n")
    for a in out:
        file.write("\t"+a+"\n")
    file.close
    




