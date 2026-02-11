import code_gen.tinylang_x86_codegen as cg


regs: list[str] = ["edi","esi","edx","ecx","r8d","r9d"]    #the regs for giving over function arguments


iflockup: dict[str, str]={
        "==": "jne",
        "!=": "je" ,
        "<" : "jle",
        ">" : "jg" ,
        }

looplockup: dict[str, str] = {
            "==": "je",
            "!=": "jne",
            "<":  "jg",
            ">":  "jle"
            }

var_types: list[str]=["n8","n16","n32","n64","un8","un16","un32","un64","n8~","n16~","n32~","n64~","un8~","un16~","un32~","un64~"]

init_sized: dict[int, str] = {1: '.byte', 2: '.word', 4: '.long', 8: '.quad'}

mov_sizes: dict[int, str] = {1:"BYTE PTR", 2:"WORD PTR", 4:"DWORD PTR", 8:"QWORD PTR"}

def size_lookup(lok_type:str) -> int:
    types: dict[str, int]={"n8":1,"n16":2,"n32":4,"n64":8,"un8":1,"un16":2,"un32":4,"un64":8,   "n8~":8,"n16~":8,"n32~":8,"n64~":8,"un8~":8,"un16~":8,"un32~":8,"un64~":8}
    if lok_type in types.keys() or (lok_type.endswith("[]") and lok_type[:-2] in types):
        if (lok_type.endswith("[]")):
            return types[lok_type[:-2]]
        else:
            return types[lok_type]
    else:
        raise SyntaxError(f"var type {lok_type} doese not exist")
    
def  init_size(var_t:str) -> str:
    return init_sized[size_lookup(var_t)]


def is_arr_type(test:str) -> bool:
    return test.endswith("[]") and (test[:-2] in var_types )

def is_ptr_type(test:str) -> bool:
    return test.endswith("~") and (test in var_types )

def is_n_type(test:str) -> bool:
    return  test in var_types[:8]


def get_mov_size(var_type:str)->str:
    return mov_sizes[size_lookup(var_type)]    

def label_generator():
    num = 0
    while True:
        yield num
        num+=1 

label_gen = label_generator()




class contextc():
    def __init__(self, is_global:bool=False):
        self.locals = {}
        self.is_global: bool = is_global
        self.offset = 0
        self.ret_type= "void"
        self.expoint = None

    def declare_var(self, name:str, vartype:str, var_len:int=1) -> None:
        size: int = size_lookup(vartype) * var_len

        if self.is_global:
            cg.global_vars[name] = {"type": vartype, "size": size}
            if is_arr_type(vartype):
                cg.global_vars[name]['len'] = var_len
        else:
            self.offset += alingment_gen(vartype,self,var_len)
            self.locals[name] = {"type": vartype, "size": size, "ofs": self.offset}
            if is_arr_type(vartype):
                self.locals[name]['len'] = var_len

def alingment_gen(var_type:str, cur_conx:contextc, dlen:int=1)->int:
    size: int = size_lookup(var_type)
    if cur_conx.offset % size != 0:
        cur_conx.offset += size - (cur_conx.offset % size)

    cur_conx.offset += size * dlen

    return cur_conx.offset  

def var_decl(var_n:str, loc_conx:contextc) -> bool:      #checks if a var has already been declared
    if var_n in loc_conx.locals.keys():
        return True
    elif var_n in cg.global_vars.keys():
        return True
    else:
        return False

def get_var_dict(var_n:str,contex:contextc) -> dict:
    if var_n in contex.locals.keys():
        return contex.locals[var_n]
    elif var_n in cg.global_vars.keys():
        return cg.global_vars[var_n]
    else:
        raise SyntaxError(f"var {var_n} doese not exist")
    
def get_var_type(var_n:str,contex:contextc) -> str:
    return get_var_dict(var_n,contex)['type']

def get_pointer_mov_size(vartype:str) -> str:
    if is_ptr_type(vartype):
        return get_mov_size(vartype[:-1])
    else:
        raise SyntaxError("get pointer mov size got a non pointer vartype: " + str(vartype))


def var_mem_asm(var_n:str,imp_contx:contextc) -> str:
    if var_n in imp_contx.locals.keys():
        var_type = str(imp_contx.locals[var_n]['type'])
        if is_n_type(var_type):
            return f"{get_mov_size(var_type)} [rbp-{imp_contx.locals[var_n]['ofs']}]"
        else:
            raise SyntaxError(str(var_type)+"not implemented")
        
    elif var_n in cg.global_vars.keys():
        var_type = str(cg.global_vars[var_n]['type'])
        if is_n_type(var_type):
            return f"{get_mov_size(var_type)} [{var_n}]"
        else:
            raise SyntaxError(str(var_type)+"not implemented")
        
    else:
        raise SyntaxError(f"var {var_n} has never been declared")
    

def form_acces(node:dict,contx:contextc) -> list[str]:
    text :list[str] = []




    return text


#84680937534851968313
    
    