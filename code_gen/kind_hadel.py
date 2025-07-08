import tinylang_x86_codegen as gc
import utils_stuff as ut


def handle_letinit(node:dict,contex:ut.contextc):
    text = []
    var_name = node['name']
    vartype  = node['var_type']

    if ut.var_decl(var_name,contex):
        raise SyntaxError(f"variable: {var_name} has already been declared")

    tmp={}
    tmp["type"] = vartype

    size = None
    varlen = 1


    if ut.is_arr_type(vartype):
        
        varlen = node['len']
        arrsize = varlen * ut.size_lookup(vartype)
        
        tmp['size'] = arrsize
        tmp['len'] = varlen

        gc.data.append(f"{var_name}:")
        
        

    if contex.is_global:
        gc.global_vars[var_name] = tmp
        
    else:
       
        tmp['ofs'] = ut.alingment_gen(vartype, contex, varlen)
        contex.locals[var_name] = tmp


    if  ut.is_n_type(vartype):
        val_type = node['val']['kind']
    else:
        val_type = ""

    print("val type: "+str(val_type))

    if val_type == "literal":
        print("get here")
        if contex.is_global:
            gc.data.append(f"{var_name}: \n\t {ut.init_size(vartype)} \t {node['val']['val']}")
        else:
            text.append(f"mov {ut.var_mem_asm(var_name, contex)}, {node['val']['val']}")

        print(gc.data)

    elif val_type == "identifier":
        if contex.is_global:
            gc.data.append(f"{var_name}: \n\t {ut.init_size(vartype)} \n 0")
            
        text.append(f"mov rax , {ut.var_mem_asm(node['val']['name'], contex)}")
        text.append(f"mov {ut.var_mem_asm(var_name, contex.locals)} , rax")

    elif val_type == "binexp":
        if contex.is_global:
            gc.data.append(f"{var_name}: \n\t {ut.init_size(vartype)} \n 0")

        text.extend(gc.formulate_math(node['val'],contex))
        text.append(f"mov {ut.var_mem_asm(var_name, contex)}, rax")

    elif val_type == "refrence":
        if contex.is_global:
            gc.data.append(f"{var_name}: \n\t {ut.init_size(vartype)} \n 0")

        text.append(f"lea rax, {ut.var_mem_asm(node['val']['name'], contex)}")
        text.append(f"mov {ut.var_mem_asm(var_name, contex)}, rax")

    elif val_type == "derefrence":
        if contex.is_global:
            gc.data.append(f"{var_name}: \n\t {ut.init_size(vartype)} \n 0")

        text.append(f"mov rax, {ut.var_mem_asm(node['name'], contex)}")  # rax = address of pointee
        text.append("mov rax, [rax]")                                    # rax = value at that address
        text.append(f"mov {ut.var_mem_asm(var_name,contex)}, rax")       #

    elif ut.is_arr_type(vartype):
        ut.get_var_dict(var_name,contex)['type'] = vartype
        if ut.is_arr_type(vartype):
            gc.data.append(var_name+":")
            for nana in node['val']:
                if nana["kind"] == "literal":
                    size = ut.size_lookup(vartype)
                    gc.data.append(f"\t{ ut.init_sized[size]} \t{nana['val']}")

    return text



def handle_let_dec(node:dict,contex:ut.contextc):
    var_name =node['name']
    vartype = node['var_type']

    if (ut.var_decl(var_name,contex)):
        raise SyntaxError(f"variable: {var_name} has already been declared")
    else:

        
        tmp={}
        size = None
        tmp['type'] = vartype
        varlen = 1

        if ut.is_arr_type(vartype):
            tmp["type"] = vartype
            varlen = node['len']
            size = varlen * ut.size_lookup(vartype)
            
            tmp['len'] = varlen

            gc.data.append(f"{var_name}:")
            gc.data.append(f"\t.zero\t{size}")



        else:
            size = ut.size_lookup(vartype)
    
        
        tmp['size'] = size
 

        if contex.is_global:
            gc.global_vars[var_name] = tmp
        else:
            
            tmp['ofs'] = ut.alingment_gen(vartype, contex,varlen)

            contex.locals[var_name] = tmp

def handle_asing(node:dict,contex:ut.contextc):
    text=[]
    write_name = node['name']
    val_type = node['val']['kind']


    if ut.var_decl(write_name,contex):
        if val_type == "literal":
            text.append(f"mov rax, {ut.var_mem_asm(node['val']['val'], contex)}")

        elif val_type == "binexp":
            text.extend(gc.formulate_math(node['val'],contex))

        elif val_type == "identifier":
            text.append(f"mov rax, {ut.var_mem_asm(node['val']['name'], contex)}")

        elif val_type == "Fcall":
            text.extend(gc.formulate_fcals(node['val'], contex))

        elif val_type == "refrence":
            text.append(f"lea rax, {ut.var_mem_asm(node['val']['name'], contex)}")

        elif val_type == "derefrence":
            text.append(f"mov rdx, {ut.var_mem_asm(node['val']['name'], contex)}")
            text.append(f"mov rax, {ut.var_mem_asm(node['val']['name'], contex)['type']} [rdx]")

        elif val_type=="arrac":
            
            #{'kind': 'asing', 'name': 'num', 'val': {'kind': 'arrac', 'name': 'ncm', 'pos': {'kind': 'literal', 'val': 1}}}
            arr_ac_kind=node["val"]["pos"]["kind"]
            if arr_ac_kind == "literal":
                read_name = node["val"]['name']
                pos = node["val"]["pos"]["val"]
                pos*=ut.size_lookup(ut.get_var_type(read_name,contex))
                text.append(f"mov rax, {read_name}[rip+{pos}]")

            elif  arr_ac_kind == "identifier":
                #mov eax, lala[0+rax*4]
                read_name = node["val"]['name']
                size = ut.size_lookup(ut.get_var_type(node["val"]["name"],contex))
                text.append(f"mov rax, {ut.var_mem_asm(node['val']['pos']['name'], contex)}")
                text.append(f"mov rax, {read_name}[0+rax*{size}]")
                
            else:
                raise("array aces indicies can only be vars or literals not: " + str(arr_ac_kind))
        
        write_type = ut.get_var_dict(write_name,contex)['type']

        if ut.is_arr_type(write_type):

            if write_name in gc.global_vars.keys():
                if node["pos"]["kind"] == "literal":
                    
                    pos = node["pos"]["val"]
                    pos*=ut.size_lookup(gc.global_vars[write_name]['type'])
                    
                    text.append(f"mov  [rip+{pos}], rax")

                elif  node["pos"]["kind"] == "identifier":
                    #mov eax, lala[0+rax*4]
                    read_name = node["val"]['name']
                    size = ut.size_lookup(gc.global_vars[node["val"]["name"]]["type"])
                    text.append(f"mov rdx, {ut.var_mem_asm(node['val']['pos']['name'] , contex)}")
                    text.append(f"mov {write_name}[0+rdx*{size}], rax")

            elif write_name in contex.locals.keys():
                if node["pos"]["kind"] == "literal":
                    #ofs - i*size
                    
                    pos = node["pos"]["val"]
                    pos*=ut.size_lookup(contex.locals[write_name]['type'])
                    pos-= (contex.locals[write_name]['ofs'])
                    text.append(f"mov {ut.get_mov_size(write_type)} [rbp-{pos}], rax")

                elif node["pos"]["kind"] == "identifier":
                    #[rbp-ofs+rax*size]
                    ofs = contex.locals[write_name]['ofs']
                    read_name = node["val"]['name']
                    size = ut.size_lookup(ut.get_var_type(node["val"]["name"],contex))
                    text.append(f"mov rdx, {ut.var_mem_asm(node['val']['pos']['name'], contex)}")
                    text.append(f"mov {ut.var_mem_asm(write_name, contex)} [rbp-{ofs}+rdx*{size}], rax")

            else:
                raise SyntaxError(f"variable {write_name} has never been declared")

        
        elif ut.is_ptr_type(write_type):
            text.append(f"mov rdx, {ut.var_mem_asm(write_name, contex)}")
            text.append(f"mov [rdx], rax ")
            

        elif ut.is_n_type(write_type):
            text.append(f"mov {ut.var_mem_asm(write_name, contex)}, rax")



        return text
    else:
        raise SyntaxError(f"variable: {write_name} has not been declared")
    

def handle_func_def(node:dict,contex:ut.contextc):
    text=[]
    fname = node['name']
    if contex.is_global:
        params = node["param"]

        if len(params) > len(ut.regs):
            raise SyntaxError("to many args in function: " + fname)
        else:
            gc.functions[fname]= params
            return_type = node["ret_type"]


            text.append(f".{fname}:")
            text.append("push rbp")         #seting up new stack frame
            text.append("mov rbp, rsp")


            loc_para = {}
            loc_cont = ut.contextc()
            loc_cont.ret_type = return_type

            #unpacking locals
            for i in range(len(params)):  
                cur_type = params[i]['type']
                cur_name = params[i]['name']

                cur_size = ut.size_lookup(cur_type)

                
                cur_ofs = ut.alingment_gen(cur_type,1,loc_cont)


                loc_para[cur_name] = {'type':cur_type, "size": cur_size, "ofs":cur_ofs} 

                text.append(f"mov {ut.var_mem_asm(params[i]['type'],loc_para)}, {ut.regs[i]}")

            
            
            
            text.extend(gc.gen(node["body"],loc_cont)) #gen a new funct whit its own locals

            text.extend(["pop   rbp","ret"])

            return text
    else:
        raise SyntaxError("only global gc.functions are alowed: " + str(fname))
    
def handle_if(node:dict,contex:ut.contextc):
    text=[]
    text.extend(gc.formulate_math(node["exp"],contex.locals,"cond"))

    endl = next(ut.lable_gen)
    

    text.append(f'{ut.iflockup[node["exp"]["op"]]} .L{endl}')      #jne .L1
    
    text.extend(gc.functions(node["body"],contex))
    
    text.append(f".L{endl}:")

    return text

def handle_if_else(node:dict,contex:ut.contextc):
    text=[]
    text.extend(gc.formulate_math(node["exp"], contex.locals, "cond"))
    endl = next(ut.lable_gen)
    
    elsel= next(ut.lable_gen)

    text.append(f'{ut.iflockup[node["exp"]["op"]]} .L{elsel}')      #jne .L1

    text.extend(gc.functions(node["body"],contex))

    text.append(f"jmp .L{endl}")

    text.append(f".L{elsel}:")
    
    text.extend(gc.functions(node["else_body"], contex))

    text.append(f".L{endl}:")

    return text

def handle_while(node:dict,contex:ut.contextc):
    text=[]
    endla = next(ut.lable_gen)
    startla =next(ut.lable_gen)
    text.append(f"jmp .L{endla}")
    text.append(f".L{startla}")
    
    text.extend(gc.functions(node["body"], contex))
    text.append(f".L{endla}")
    text.extend(gc.formulate_math(node["exp"], contex.locals, "cond"))
    text.append(f'{ut.looplockup[node["exp"]["op"]]} .L{startla}')

    return text

def handle_for(node:dict,contex:ut.contextc):
    text=[]
    endla = next(ut.lable_gen)
    startla =next(ut.lable_gen)

    text.extend(gc.functions(node["init"], contex))

    text.append(f"jmp .L{endla}")
    text.append(f".L{startla}")

    text.extend(gc.functions(node["body"], contex))

    text.extend(gc.functions(node["incexp"], contex))

    text.append(f".L{endla}")
    text.extend(gc.formulate_math(node["exp"], contex))
    text.append(f'{ut.looplockup[node["exp"]["op"]]} .L{startla}')

    return text