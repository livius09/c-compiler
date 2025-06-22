from colorama import *
from utils_stuff import *


def var_mem_asm(var_n:str,imp_locals:dict):
        if var_n in imp_locals.keys():
            var_type = imp_locals[var_n]
            if is_n_type(var_type):
                return f"{get_mov_size(var_type)} [rbp-{imp_locals[var_n]['ofs']}]" 
            
        elif var_n in global_vars.keys():
            var_type = global_vars[var_n]
            if is_n_type(var_type):
                return f"{get_mov_size(var_type)} [{var_n}]" 
        else:
            raise SyntaxError(f"var {var_n} has never been declared")
        


def formulate_math(node:dict, local_var:dict, context="asing",): #asing, cond
    nodetype = node['kind']
    
    if nodetype == "Identifier":
        return [f"mov rax, {node['name']}"]
    
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

        code += formulate_math(node['left'], local_var, context)
        code.append("push rax")
        code += formulate_math(node['right'], local_var, context)
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

def formulate_fcals(node:dict,local_vars:dict):    #genertate code for function calls and checking the parameter types
    code=[]
    fname = node['name']
    if fname in functions.keys():
        params = node['para']
        dectypes = functions[fname]
        
        for i in range(len(params)):

            curtype = params[i]['kind']

            if curtype == "binexp":
                code.extend(formulate_math(params[i]["val"],local_vars))
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

global_vars={}         #x:n8    contains the var name as key and type as value
functions={}    #print:[char[],n64]    contains the function name as key and the value is the types of the parameter in order
regs= ["edi","esi","edx","ecx","r8d","r9d"]    #the regs for giving over function arguments
data=[]         #data section of asm



def gen(a:list[dict],local_vars:dict[dict],scope=True):   #true is global false is local  #local_vars {x:{type:n32, ofs:2, size:4}, arr:{type:n16[], osf:10,len:4,size:8}}
    text=[]         #text section so the actual executed asm
    ofset=0         #ofset for the local vars

    

    
    
    def get_var(var_n:str):
        if var_n in local_vars.keys():
            return local_vars[var_n]
        elif var_n in global_vars.keys():
            return global_vars[var_n]
        else:
            raise SyntaxError(f"var {var_n} doese not exist")
        
    def var_decl(var_n:str):
        if var_n in local_vars.keys():
            return True
        elif var_n in global_vars.keys():
            return True
        else:
            raise SyntaxError(f"var {var_n} doese not exist")
        



    
    for node in a:
        print(node)
        match node['kind']:
            
            case "letinit":    #if its a let decl add the name and type to the vars dict if theyr already in there from and eror and generate the code for putting the value in
                var_name = node['name']
                vartype  = node['var_type']

                if var_decl(var_name):
                    raise SyntaxError(f"variable: {var_name} has already been declared")
    
                tmp={}
                tmp["type"]=vartype

                size = None
                

                if is_arr_type(vartype):
                    tmp["type"] = vartype
                    arrlen = node['len']
                    arrsize = arrlen * size_lookup(vartype)
                    
                    tmp['size'] = arrsize
                    tmp['len'] = arrlen

                    data.append(f"{var_name}:")
                    data.append(f"\t.zero\t{arrsize}")


                if scope:
                    global_vars[var_name] = tmp
                else:
                    ofset+=size
                    tmp['ofs'] = ofset
                    local_vars[var_name] = tmp

                if  not is_arr_type(vartype):
                    val_type = node['val']['kind']
                else:
                    val_type = ""

                if val_type == "literal":
                    data.append(f"{var_name} dq {node['val']['val']}")

                elif val_type == "identifier":
                    data.append(f"{var_name} dq 0")

                    text.append(f"mov rax , {var_mem_asm(node['val']['name'])}")
                    text.append(f"mov {var_mem_asm(var_name)} , rax")

                elif val_type == "binexp":
                    data.append(f"{var_name} dq 0")
                    
                    text.extend(formulate_math(node['val'],local_vars))
                    text.append(f"mov {var_mem_asm(var_name)}, rax")

                elif val_type == "refrence":
                    data.append(f"{var_name} dq 0")

                    text.append(f"lea rax, {var_mem_asm(node['val']['name'])}")
                    text.append(f"mov [{var_name}], rax")

                elif val_type == "derefrence":
                    data.append(f"{var_name} dq 0")
                    text.append(f"mov rax, {var_mem_asm(node['name'])}")  # rax = address of pointee
                    text.append("mov rax, [rax]")              # rax = value at that address
                    text.append(f"mov {var_mem_asm(node['name'])}, rax")

                elif is_arr_type(vartype):
                    vars[var_name] = vartype
                    if is_arr_type(vartype):
                        data.append(var_name+":")
                        for nana in node['val']:
                            if nana["kind"] == "literal":
                                size = size_lookup(vartype[:-2])
                                directive = {1: '.byte', 2: '.word', 4: '.long', 8: '.quad'}[size]
                                data.append(f"\t{directive} \t{nana['val']}")


            case "letdec":
                var_name =node['name']
                vartype = node['var_type']

                if (var_decl(var_name)):
                    raise SyntaxError(f"variable: {var_name} has already been declared")
                else:

                    
                    tmp={}
                    size = None
                    tmp['type'] = vartype

                    if is_arr_type(vartype):
                        tmp["type"] = vartype
                        arrlen = node['len']
                        arrsize = arrlen * size_lookup(vartype)
                        
                        tmp['size'] = arrsize
                        tmp['len'] = arrlen

                        data.append(f"{var_name}:")
                        data.append(f"\t.zero\t{arrsize}")



                    else:
                        size = size_lookup(vartype)
                
                        

                    if scope:
                        global_vars[var_name] = tmp
                    else:
                        ofset+=size
                        tmp['ofs'] = ofset
                        local_vars[var_name] = tmp

            case "asing":    #genreate code for the normal "x = y+1" statements
                write_name = node['name']
                val_type = node['val']['kind']

                if write_name in vars.keys():
                    if val_type == "literal":
                        text.append(f"mov rax, {var_mem_asm(node['val']['val'])}")

                    elif val_type == "binexp":
                        text.extend(formulate_math(node['val']))

                    elif val_type == "identifier":
                        text.append(f"mov rax, {var_mem_asm(node['val']['name'])}")

                    elif val_type == "Fcall":
                        text.extend(formulate_fcals(node['val'], local_vars))

                    elif val_type == "refrence":
                        text.append(f"lea rax, {var_mem_asm(node['val']['name'])}")

                    elif val_type == "derefrence":
                        text.append(f"mov rdx, {var_mem_asm(node['val']['name'])}")
                        text.append(f"mov rax, {get_mov_size(get_var(node['val']['name'])['type'][:-2])} [rdx]")

                    elif val_type=="arrac":
                        
                        #{'kind': 'asing', 'name': 'num', 'val': {'kind': 'arrac', 'name': 'ncm', 'pos': {'kind': 'literal', 'val': 1}}}

                        if node["val"]["pos"]["kind"] == "literal":
                            print(node)
                            read_name = node["val"]['name']
                            pos = node["val"]["pos"]["val"]
                            pos*=size_lookup(vars[read_name])
                            text.append(f"mov rax, {read_name}[rip+{pos}]")

                        elif  node["val"]["pos"]["kind"] == "identifier":
                            #mov eax, lala[0+rax*4]
                            read_name = node["val"]['name']
                            size = size_lookup(vars[node["val"]["name"]])
                            text.append(f"mov rax, {var_mem_asm(node['val']['pos']['name'])}")
                            text.append(f"mov rax, {read_name}[0+rax*{size}]")
                            
                        else:
                            raise("nicht skibidy")
                    
                    
                    if is_arr_type(get_var(write_name)['type']):

                        if write_name in global_vars.keys():
                            if node["pos"]["kind"] == "literal":
                                
                                pos = node["pos"]["val"]
                                pos*=size_lookup(global_vars[write_name]['type'])
                                
                                text.append(f"mov  [rip+{pos}], rax")

                            elif  node["pos"]["kind"] == "identifier":
                                #mov eax, lala[0+rax*4]
                                read_name = node["val"]['name']
                                size = size_lookup(global_vars[node["val"]["name"]])
                                text.append(f"mov rdx, {var_mem_asm(node['val']['pos']['name'])}")
                                text.append(f"mov {write_name}[0+rdx*{size}], rax")

                        elif write_name in local_vars:
                            if node["pos"]["kind"] == "literal":
                                #ofs - i*size
                                
                                pos = node["pos"]["val"]
                                pos*=size_lookup(local_vars[write_name])
                                pos-= (local_vars[write_name]['ofs'])
                                text.append(f"mov {var_mem_asm()} [rbp-{pos}], rax")

                            elif node["pos"]["kind"] == "identifier":
                                #[rbp-ofs+rax*size]
                                ofs = local_vars[write_name]['ofs']
                                read_name = node["val"]['name']
                                size = size_lookup(global_vars[node["val"]["name"]])
                                text.append(f"mov rdx, {var_mem_asm(node['val']['pos']['name'])}")
                                text.append(f"mov {var_mem_asm(write_name)} [rbp-{ofs}+rdx*{size}], rax")

                        else:
                            raise SyntaxError(f"variable {write_name} has never been declared")

                    
                    elif is_ptr_type(vars[write_name]):
                        text.append(f"mov rdx, {var_mem_asm(write_name)}")
                        text.append(f"mov [rdx], rax ")
                        

                    elif is_n_type(vars[write_name]):
                        text.append(f"mov {var_mem_asm(write_name)}, rax")




                else:
                    raise SyntaxError(f"variable:{write_name} has not been declared")

            case "fcall":    
                formulate_fcals(node,local_vars)


                
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
                
                text.extend(formulate_math(node["exp"],local_vars,"cond"))

                lnum = next(label_gen)
                

                text.append(f'{iflockup[node["exp"]["op"]]} .L{lnum}')      #jne .L1
                
                text.extend(gen(node["body"]))
                
                text.append(f".L{lnum}:")
                

            case "if_else":
                text.extend(formulate_math(node["exp"], local_vars, "cond"))
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
                text.extend(formulate_math(node["exp"], local_vars, "cond"))
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
                text.extend(formulate_math(node["exp"],local_vars, "cond"))
                text.append(f'{looplockup[node["exp"]["op"]]} .L{startla}')
            
            case _:
                pass #raise SyntaxError("ligma")

    return text




             
init = {'kind': 'asing', 'name': 'y', 'val': {'kind': 'binexp', 'op': '+', 'left': {'kind': 'Identifier', 'name': 'y'}, 'right': {'kind': 'literal', 'val': 1}}}    
nif  = [{'kind': 'if', 'exp': {'kind': 'binexp', 'op': '==', 'left': {'kind': 'Identifier', 'name': 'x'}, 'right': {'kind': 'literal', 'val': 2}}, 'body': [{'kind': 'asing', 'name': 'x', 'val': {'kind': 'literal', 'val': 2}}]}]      
nfor = [{'kind': 'for', 'init': {'kind': 'letinit', 'name': 'i', 'var_type': 'n8', 'val': {'kind': 'literal', 'val': 0}}, 'exp': {'kind': 'binexp', 'op': '==', 'left': {'kind': 'Identifier', 'name': 'i'}, 'right': {'kind': 'literal', 'val': 1}}, 'incexp': [{'kind': 'asing', 'name': 'i', 'val': {'kind': 'binexp', 'op': '+', 'left': {'kind': 'identifier', 'name': 'i'}, 'right': {'kind': 'literal', 'val': 1}}}], 'body': [{'kind': 'asing', 'name': 'x', 'val': {'kind': 'binexp', 'op': '+', 'left': {'kind': 'Identifier', 'name': 'x'}, 'right': {'kind': 'literal', 'val': 1}}}]}]
nptr = [{'kind': 'letinit', 'var_type': 'n8', 'name': 'num', 'val': {'kind': 'literal', 'val': 2}}, {'kind': 'letinit', 'var_type': 'n8~', 'name': 'ptr', 'val': {'kind': 'refrence', 'name': 'num'}}, {'kind': 'letinit', 'var_type': 'n32', 'name': 'refnum', 'val': {'kind': 'binexp', 'op': '+', 'left': {'kind': 'derefrence', 'name': 'ptr'}, 'right': {'kind': 'literal', 'val': 1}}}]
narr = [{'var_type': 'n32[]', 'name': 'ncm', 'kind': 'letdec',"size": 2},{'var_type': 'n32', 'name': 'num', 'kind': 'letdec'}, {'kind': 'asing', 'name': 'ncm', 'pos': {'kind': 'literal', 'val': 2}, 'val': {'kind': 'literal', 'val': 2}}]
out = gen(narr,{})
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




