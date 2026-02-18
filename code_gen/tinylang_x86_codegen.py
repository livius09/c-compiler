import code_gen.kind_hadel as kh
import code_gen.utils_stuff as ut
import json



global global_vars, functions, data
global_vars = {}        #"x":{"type":"n8", "size":1, }    contains the var name as key and type as value
functions :dict[str,list[str]]= {}          #"print":["char[]","n64"]    contains the function name as key and the value is the types of the parameter in order

data:list[str] = []         #data section of asm

#test 
def get_data():
    return data

def formulate_math(node:dict, loc_conx:ut.contextc, mcontext:str="asing",): #asing, cond
    nodetype = str(node['kind'])
    
    if nodetype == "identifier":
        return [f"mov rax, {ut.var_mem_asm(node['name'],loc_conx)}"]
    
    if nodetype == "literal":
        return [f"mov rax, {node['val']}"]

    if nodetype == "refrence":
        return [f"lea rax, {ut.var_mem_asm(node['name'],loc_conx)}"]
    
    if nodetype == "derefrence":
       return [f"mov rax, {ut.var_mem_asm(node['name'],loc_conx)}",  # rax = address of pointee
                "mov rax, [rax]"]             # rax = value at that address
    
    if nodetype == "Fcall":
        return formulate_fcals(node,loc_conx)

    if nodetype == "binexp":
        code :list[str]= []
        cmpops: list[str]=["==","!=","<",">","<=",">="]

        code += formulate_math(node['left'], loc_conx, mcontext)
        code.append("push rax")
        code += formulate_math(node['right'], loc_conx, mcontext)
        code.append("pop rbx")

        op = str( node['op'])
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
        elif op == "&":
            code.append("and rax, rbx")
        elif op == "|":
            code.append("or rax, rbx")
        elif op == "^":
            code.append("xor rax, rbx")
        elif op in cmpops:
            code.append("cmp rax, rbx")
            if mcontext == "asing":
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
    else:
        raise SyntaxError("invalid math: " + str(nodetype))

def formulate_fcals(node:dict,conx:ut.contextc) -> list[str]:    #genertate code for function calls and checking the parameter types
    code:list[str]=[]
    fname = str(node['name'])
    if fname in functions.keys():
        params = list(node['para'])
        dectypes: list[str] = functions[fname]
        
        for i in range(len(params)):

            curtype :str= str(params[i]['kind'])

            if curtype == "binexp":
                code.extend(formulate_math(params[i]["val"], conx))
                code.append(f"mov {ut.fregs[i]}, rax")
            elif curtype == "identifier":
                
                varname = str(params[i]['name'])
                vartype: str = ut.get_var_type(varname, conx)

                if dectypes[i] == vartype:
                    code.append(f"mov {ut.fregs[i]}, [{varname}]")

                else:
                    raise TypeError(f"expected type {dectypes[i]} but got {vartype} on arg {i} of function call {fname}")

            elif curtype == "literal":
                code.append(f"mov {ut.fregs[i]} {params[i]['val']}")

        code.append(f"call .{fname}")
        
        return code

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



def gen(a:list[dict],contex:ut.contextc)-> list[str]:   #local or global is in contex  #local_vars {x:{type:n32, ofs:2, size:4}, arr:{type:n16[], osf:10,len:4,size:8}}
    text:list[str]=[]         #text section so the actual executed asm

    
    
    for node in a:
        #print("cur node:")
        #print(node)

    
        if not isinstance(node, dict):
            raise TypeError(f"gc.gen() got unexpected type: {type(node)} {node!r}")
    

        match node['kind']:
            
            case "letinit":    #if its a let decl add the name and type to the vars dict if theyr already in there from and eror and generate the code for putting the value in
                text.extend(kh.handle_letinit(node,contex))
                #print("data: " + str(data))

            case "letdec":
                kh.handle_let_dec(node,contex)

            case "asing":    #genreate code for the normal "x = y+1" statements
                text.extend(kh.handle_asing(node,contex))

            case "fcall":    
                text.extend(formulate_fcals(node, contex))

  
            case "func_dec":
                text.extend(kh.handle_func_def(node,contex))

            case "struct_dec":
                kh.handel_struct_dec(node,contex)
                
            
            case "if":
                text.extend(kh.handle_if(node,contex))
        

            case "while":
                text.extend(kh.handle_while(node,contex))


            case "for":
                text.extend(kh.handle_for(node,contex))


            case "ret":
                text.extend(formulate_math(node["val"],contex))
            

            case _:
                raise SyntaxError("AST Defective: "+str(node['kind']))
            
        #print("end of loop:")

        #print("data: "+str(data))
        #print(text)

    return text




             
inir = [{'kind': 'asing', 'name': 'y', 'val': {'kind': 'binexp', 'op': '+', 'left': {'kind': 'identifier', 'name': 'y'}, 'right': {'kind': 'literal', 'val': 1}}}]   
nif  = [{'kind': 'if', 'exp': {'kind': 'binexp', 'op': '==', 'left': {'kind': 'identifier', 'name': 'x'}, 'right': {'kind': 'literal', 'val': 2}}, 'body': [{'kind': 'asing', 'name': 'x', 'val': {'kind': 'literal', 'val': 2}}]}]      
nfor = [{'kind': 'for', 'init': {'kind': 'letinit', 'name': 'i', 'var_type': 'n8', 'val': {'kind': 'literal', 'val': 0}}, 'exp': {'kind': 'binexp', 'op': '==', 'left': {'kind': 'identifier', 'name': 'i'}, 'right': {'kind': 'literal', 'val': 1}}, 'incexp': [{'kind': 'asing', 'name': 'i', 'val': {'kind': 'binexp', 'op': '+', 'left': {'kind': 'identifier', 'name': 'i'}, 'right': {'kind': 'literal', 'val': 1}}}], 'body': [{'kind': 'asing', 'name': 'x', 'val': {'kind': 'binexp', 'op': '+', 'left': {'kind': 'identifier', 'name': 'x'}, 'right': {'kind': 'literal', 'val': 1}}}]}]
nptr = [{'kind': 'letinit', 'var_type': 'n8', 'name': 'num', 'val': {'kind': 'literal', 'val': 2}}, {'kind': 'letinit', 'var_type': 'n8~', 'name': 'ptr', 'val': {'kind': 'refrence', 'name': 'num'}}, {'kind': 'letinit', 'var_type': 'n32', 'name': 'refnum', 'val': {'kind': 'binexp', 'op': '+', 'left': {'kind': 'derefrence', 'name': 'ptr'}, 'right': {'kind': 'literal', 'val': 1}}}]
narr = [{'var_type': 'n32[]', 'name': 'ncm', 'kind': 'letdec',"size": 2},{'var_type': 'n32', 'name': 'num', 'kind': 'letdec'}, {'kind': 'asing', 'name': 'ncm', 'pos': {'kind': 'literal', 'val': 2}, 'val': {'kind': 'literal', 'val': 2}}]
cost = [{'var_type': 'n8', 'name': 'thing', 'kind': 'letinit', 'val': {'kind': 'literal', 'val': 4}}]

test = [{'var_type': 'n64', 'name': 'global', 'kind': 'letinit', 'val': {'kind': 'literal', 'val': 3}}, {'kind': 'func_dec', 'name': 'Main', 'ret_type': 'void', 'param': [], 'body': [{'var_type': 'n64', 'name': 'local', 'kind': 'letinit', 'val': {'kind': 'literal', 'val': 2}}, {'kind': 'asing', 'name': 'local', 'val': {'kind': 'binexp', 'op': '+', 'left': {'kind': 'identifier', 'name': 'global'}, 'right': {'kind': 'literal', 'val': 1}}}]}]

if __name__ == "__main__":
    start_contx = ut.contextc(is_global=True)
    out: list[str] = gen(cost, start_contx)
    
    print("globals: "+str(global_vars))
    print("Data: "+ str(data))
    print("asm: "+str(out))

    with open("./code_gen/readout.txt","w") as file:
        file.write("data:\n")
        for b in data:
            file.write("\t"+b+"\n")
        file.write("text:\n")
        for a in out:
            file.write("\t"+a+"\n")
        file.close

