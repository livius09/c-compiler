from colorama import *
import utils_stuff as ut
import kind_hadel as kh

def formulate_math(node:dict, local_var:dict, mcontext="asing",): #asing, cond
    nodetype = node['kind']
    
    if nodetype == "identifier":
        return [f"mov rax, {ut.var_mem_asm(node['name'],local_var)}"]
    
    if nodetype == "literal":
        return [f"mov rax, {node['val']}"]

    if nodetype == "refrence":
        return [f"lea rax, {ut.var_mem_asm(node['name'],local_var)}"]
    
    if nodetype == "derefrence":
       return [f"mov rax, {ut.var_mem_asm(node['name'],local_var)}",  # rax = address of pointee
                "mov rax, [rax]"]             # rax = value at that address
    
    if nodetype == "Fcall":
        return formulate_fcals(node)

    if nodetype == "binexp":
        code = []
        cmpops=["==","!=","<",">","<=",">="]

        code += formulate_math(node['left'], local_var, mcontext)
        code.append("push rax")
        code += formulate_math(node['right'], local_var, mcontext)
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

def formulate_fcals(node:dict,conx):    #genertate code for function calls and checking the parameter types
    code=[]
    fname = node['name']
    if fname in functions.keys():
        params = node['para']
        dectypes = functions[fname]
        
        for i in range(len(params)):

            curtype = params[i]['kind']

            if curtype == "binexp":
                code.extend(formulate_math(params[i]["val"], conx.local_vars))
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



def gen(a:list[dict],contex:ut.contextc):   #true is global false is local  #local_vars {x:{type:n32, ofs:2, size:4}, arr:{type:n16[], osf:10,len:4,size:8}}
    text=[]         #text section so the actual executed asm

    
    
    for node in a:
        print(node)
        match node['kind']:
            
            case "letinit":    #if its a let decl add the name and type to the vars dict if theyr already in there from and eror and generate the code for putting the value in
                text.extend(kh.handle_letinit(node,contex))

            case "letdec":
                text.extend(kh.handle_let_dec(node,contex))

            case "asing":    #genreate code for the normal "x = y+1" statements
                text.extend(kh.handle_asing(node,contex))

            case "fcall":    
                text.extend(formulate_fcals(node, contex.locals))

  
            case "func_dec":
                text.extend(kh.handle_func_def(node,contex))
                
            
            case "if":
                text.extend(kh.handle_if(node,contex))
                

            case "if_else":
                text.extend(kh.handle_if_else(node,contex))


            case "while":
                text.extend(kh.handle_while(node,contex))


            case "for":
                text.extend(kh.handle_for(node,contex))


            case "ret":
                text.extend(formulate_math(node['val']))
            

            case _:
                raise SyntaxError("AST Defective: "+str(node['kind']))

    return text




             
inir = [{'kind': 'asing', 'name': 'y', 'val': {'kind': 'binexp', 'op': '+', 'left': {'kind': 'Identifier', 'name': 'y'}, 'right': {'kind': 'literal', 'val': 1}}}]   
nif  = [{'kind': 'if', 'exp': {'kind': 'binexp', 'op': '==', 'left': {'kind': 'Identifier', 'name': 'x'}, 'right': {'kind': 'literal', 'val': 2}}, 'body': [{'kind': 'asing', 'name': 'x', 'val': {'kind': 'literal', 'val': 2}}]}]      
nfor = [{'kind': 'for', 'init': {'kind': 'letinit', 'name': 'i', 'var_type': 'n8', 'val': {'kind': 'literal', 'val': 0}}, 'exp': {'kind': 'binexp', 'op': '==', 'left': {'kind': 'Identifier', 'name': 'i'}, 'right': {'kind': 'literal', 'val': 1}}, 'incexp': [{'kind': 'asing', 'name': 'i', 'val': {'kind': 'binexp', 'op': '+', 'left': {'kind': 'identifier', 'name': 'i'}, 'right': {'kind': 'literal', 'val': 1}}}], 'body': [{'kind': 'asing', 'name': 'x', 'val': {'kind': 'binexp', 'op': '+', 'left': {'kind': 'Identifier', 'name': 'x'}, 'right': {'kind': 'literal', 'val': 1}}}]}]
nptr = [{'kind': 'letinit', 'var_type': 'n8', 'name': 'num', 'val': {'kind': 'literal', 'val': 2}}, {'kind': 'letinit', 'var_type': 'n8~', 'name': 'ptr', 'val': {'kind': 'refrence', 'name': 'num'}}, {'kind': 'letinit', 'var_type': 'n32', 'name': 'refnum', 'val': {'kind': 'binexp', 'op': '+', 'left': {'kind': 'derefrence', 'name': 'ptr'}, 'right': {'kind': 'literal', 'val': 1}}}]
narr = [{'var_type': 'n32[]', 'name': 'ncm', 'kind': 'letdec',"size": 2},{'var_type': 'n32', 'name': 'num', 'kind': 'letdec'}, {'kind': 'asing', 'name': 'ncm', 'pos': {'kind': 'literal', 'val': 2}, 'val': {'kind': 'literal', 'val': 2}}]

test= [{'var_type': 'n64', 'name': 'global', 'kind': 'letinit', 'val': {'kind': 'literal', 'val': 3}}, {'kind': 'func_dec', 'name': 'Main', 'ret_type': 'void', 'param': [], 'body': [{'var_type': 'n64', 'name': 'local', 'kind': 'letinit', 'val': {'kind': 'literal', 'val': 2}}, {'kind': 'asing', 'name': 'local', 'val': {'kind': 'binexp', 'op': '+', 'left': {'kind': 'identifier', 'name': 'global'}, 'right': {'kind': 'literal', 'val': 1}}}]}, {'kind': 'asing', 'name': 'local', 'val': {'kind': 'binexp', 'op': '+', 'left': {'kind': 'identifier', 'name': 'global'}, 'right': {'kind': 'literal', 'val': 1}}}]

if __name__ == "__main__":
    start_contx = ut.contextc(is_global=True)
    out = gen(test, start_contx)
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

#test 123

