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


def gen(a:list[dict]):
    vars={}         #x:n8    contains the var name as key and type as value
    functions={}    #print:[char[],n64]    contains the function name as key and the value is the types of the parameter in order
    data=[]         #data section of asm
    text=[]         #text section so the actual executed asm
    regs= ["edi","esi","edx","ecx","r8d","r9d"]    #the regs for giving over function arguments

    for node in a:
        match node["type"]:
            
            case "letdec":    #if its a let decl add the name and type to the vars dict if theyr already in there from and eror and generate the code for putting the value in
                identify =node["name"]
                vartype = node["vartype"]
                if identify in vars.keys():
                    raise SyntaxError("variable has already been declared")
                else:
                    vars[identify] = vartype


                if node["val"]["type"] == "Literal":
                    data.append(f"{node["name"]} dq {node["val"]["val"]}")

            case "asing":    #genreate code for the normal "x=y+1" statements
                name = node["name"]
                if name in vars.keys():
                    if node["val"]["type"] == "Literal":
                        text.append(f"mov [{name}] {node["val"]["val"]}")


                else:
                    raise SyntaxError("variable has not been declared")

            case "fcall":    #genertate code for function calls and checking the parameter types
                fname = node["name"]
                if fname in functions.keys():
                    params = node["para"]
                    dectypes = functions[fname]
                    
                    for i in range(len(params)):

                        curtype = params[i]["type"]

                        if curtype == "BinaryExpression":
                            pass
                        elif curtype == "Identifier":
                            
                            varname = params[i]["name"]
                            vartype = vars[varname]

                            if dectypes[i] == vartype:
                                text.append(f"mov {regs[i]} [{varname}]")

                            else:
                                raise TypeError(f"expected type {dectypes[i]} but got {vartype} on arg {i} of function call {fname}")

                        elif curtype == "Literal":
                            text.append(f"mov {regs[i]} {params[i]["val"]}")




                else:
                    raise SyntaxError(f"functions {fname} has not been declared")
                
            case "function_dec":    

                if len(params) > len(regs):
                    raise SyntaxError("to many args")
            

            



def formulate_math(a:dict):
    pass
