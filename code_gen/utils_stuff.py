import code_gen.tinylang_x86_codegen as cg


fregs: list[str] = ["edi","esi","edx","ecx","r8d","r9d"]    #the regs for giving over function arguments


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

#var_types: list[str]=["n8","n16","n32","n64","un8","un16","un32","un64","n8~","n16~","n32~","n64~","un8~","un16~","un32~","un64~"]

init_sized: dict[int, str] = {1: '.byte', 2: '.word', 4: '.long', 8: '.quad'}

mov_sizes: dict[int, str] = {1:"BYTE PTR", 2:"WORD PTR", 4:"DWORD PTR", 8:"QWORD PTR"}

types: dict[str, int]={"n8":1,"n16":2,"n32":4,"n64":8,"un8":1,"un16":2,"un32":4,"un64":8,   "n8~":8,"n16~":8,"n32~":8,"n64~":8,"un8~":8,"un16~":8,"un32~":8,"un64~":8}

structs = {}

def size_lookup(lok_type:str) -> int:
    
    if lok_type in types.keys() or (lok_type.endswith("[]") and lok_type[:-2] in types):
        if (lok_type.endswith("[]")):
            return types[lok_type[:-2]]
        else:
            return types[lok_type]
        
    elif lok_type in structs.keys():
        return int(structs[lok_type]["size"])
    else:
        raise SyntaxError(f"var type {lok_type} doese not exist")
    
    
def  init_size(var_t:str) -> str:
    return init_sized[size_lookup(var_t)]


def is_arr_type(test:str) -> bool:
    return test.endswith("[]") and (test[:-2] in types.keys() )

def is_ptr_type(test:str) -> bool:
    return test.endswith("~") and (test in types.keys() )

def is_n_type(test:str) -> bool:
    return  test in {"n8":1,"n16":2,"n32":4,"n64":8,"un8":1,"un16":2,"un32":4,"un64":8}


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
        self.locals: dict[str,dict[str,str|int]] = {}
        self.is_global: bool = is_global
        self.offset:int = 0
        self.ret_type = "void"
        self.expoint = None

    def declare_var(self, name:str, vartype:str, var_len:int=1 ) -> None:
        size: int = size_lookup(vartype) * var_len

        if self.is_global:
            cg.global_vars[name] = {"type": vartype, "size": size}
            if is_arr_type(vartype):
                cg.global_vars[name]['len'] = var_len
        else:
            self.offset += self.alingment_gen(vartype,  var_len)
            self.locals[name] = {"type": vartype, "size": size, "ofs": self.offset}
            if is_arr_type(vartype):
                self.locals[name]['len'] = var_len

    def is_var_decl(self, var_n:str) -> bool:      #checks if a var has already been declared
        if var_n in self.locals.keys():
            return True
        elif var_n in cg.global_vars.keys():
            return True
        else:
            return False

    def get_var_type(self,var_n:str) -> str:
        return self.get_var_dict(var_n)['type']
    

    def get_var_dict(self, var_n:str) -> dict:

        if var_n in self.locals.keys():     #locals first if a var is in "both" 
            return self.locals[var_n]
        elif var_n in cg.global_vars.keys():
            return cg.global_vars[var_n]
        else:
            raise SyntaxError(f"var {var_n} doese not exist") 

    def alingment_gen(self, var_type:str, dlen:int=1)->int:
        size: int = size_lookup(var_type)
        if self.offset % size != 0:
            self.offset += size - (self.offset % size)

        self.offset += size * dlen

        return self.offset  
    
    def var_mem_asm(self,var_n:str) -> str:
        if var_n in self.locals.keys():
            var_type = str(self.locals[var_n]['type'])
            if is_n_type(var_type):
                return f"{get_mov_size(var_type)} [rbp-{self.locals[var_n]['ofs']}]"
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
        
    


    def form_get_acces(self, node:dict) -> list[str]:
        text :list[str] = []
        ofs :int = 0
        ofs, lasttype =  self.walk_offset(node)

        text.append(f"mov rax, {get_mov_size(lasttype)} PTR [rbp-{ofs}]")

        return text


    def form_set_acces(self, node:dict) -> list[str]:
        text :list[str] = []
        ofs :int = 0
        ofs, lasttype =  self.walk_offset(node)

        text.append(f"mov {get_mov_size(lasttype)} PTR [rbp-{ofs}] , rax")

        return text

    #TODO improve make dinamic posible
    #TODO needs refactor
    def walk_offset(self,node:dict) :
        ofs :int = 0

        curtype :str = self.get_var_type(node["base"])

        for x in node["access"]:
            kind= x["kind"]

            if kind == "field":
                field :str = x["name"]
                try:
                    ofs += structs[curtype]["members"][field]["ofs"]
                    curtype = structs[curtype]["members"][field]["type"]
                except KeyError as e:
                    raise SyntaxError(f"field: {field} does not exist in struct: {curtype}")
                
            #TODO very bad
            elif kind == "index":
                if x["expr"]["kind"] == "literal":
                    ofs += x["expr"]["val"] * size_lookup(curtype)

                
            elif kind == "fcall":
                raise NotImplementedError("struct methods are not jet implemented ")
            
            else:
                raise SyntaxError(f"defective access: {x}")
            


        return (ofs , curtype)




def get_pointer_mov_size(vartype:str) -> str:
    if is_ptr_type(vartype):
        return get_mov_size(vartype[:-1])
    else:
        raise SyntaxError("get pointer mov size got a non pointer vartype: " + str(vartype))





#84680937534851968313
    
    