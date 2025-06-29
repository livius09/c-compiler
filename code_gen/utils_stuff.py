from tinylang_x86_codegen import global_vars

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

var_types=["n8","n16","n32","n64","un8","un16","un32","un64","n8~","n16~","n32~","n64~","un8~","un16~","un32~","un64~"]


def size_lookup(lok_type:str):
    types={"n8":1,"n16":2,"n32":4,"n64":8,"un8":1,"un16":2,"un32":4,"un64":8,   "n8~":8,"n16~":8,"n32~":8,"n64~":8,"un8~":8,"un16~":8,"un32~":8,"un64~":8}
    if lok_type in types.keys() or (lok_type.endswith("[]") and lok_type[:-2] in types):
        if (lok_type.endswith("[]")):
            return types[lok_type[:-2]]
        else:
            return types[lok_type]
    else:
        raise SyntaxError(f"var type {lok_type} doese not exist")


def is_arr_type(test:str):
    return test.endswith("[]") and (test[:-2] in var_types )

def is_ptr_type(test:str):
    return test.endswith("~") and (test in var_types )

def is_n_type(test:str):
    return  test in var_types[:8]

def get_mov_size(var_type:str)->str:
        #   0       1           2       3       4        5    6   7      8
    return ["", "BYTE PTR", "WORD PTR", "", "DWORD PTR", "", "", "", "QWORD PTR"][size_lookup(var_type)]    

def label_generator():
    num = 0
    while True:
        yield num
        num+=1 

label_gen = label_generator()

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
    

class contextc():
    def __init__(self, is_global=False, parent=None):
        self.locals = parent.locals if parent else None
        self.is_global = is_global
        self.offset = 0 if is_global else (parent.offset if parent else 0)
        self.parent = parent
        self.ret_type= parent.ret_type if parent else None
        self.expoint = parent.ret_type if parent else None

    def declare_var(self, name, vartype, size):
        if self.is_global:
            global_vars[name] = {"type": vartype, "size": size}
        else:
            self.offset += size
            self.locals[name] = {"type": vartype, "size": size, "ofs": self.offset}




