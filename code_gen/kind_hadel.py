from tinylang_x86_codegen import global_vars
import utils_stuff as ut

#the handels functs that are now cases should be there
#letinit and dec and stuff
# tomorow in school

def handel_letinit(node,):
    var_name = node['name']
    vartype  = node['var_type']

    if var_decl(var_name):
        raise SyntaxError(f"variable: {var_name} has already been declared")

    tmp={}
    tmp["type"]=vartype

    size = None
    

    if ut.ut.is_arr_type(vartype):
        tmp["type"] = vartype
        arrlen = node['len']
        arrsize = arrlen * ut.size_lookup(vartype)
        
        tmp['size'] = arrsize
        tmp['len'] = arrlen

        data.append(f"{var_name}:")
        data.append(f"\t.zero\t{arrsize}")


    if contex.is_global:
        global_vars[var_name] = tmp
    else:
        ofset+=size
        tmp['ofs'] = ofset
        contex.local_vars[var_name] = tmp

    if  not ut.ut.is_arr_type(vartype):
        val_type = node['val']['kind']
    else:
        val_type = ""

    if val_type == "literal":
        data.append(f"{var_name} dq {node['val']['val']}")

    elif val_type == "identifier":
        data.append(f"{var_name} dq 0")

        text.append(f"mov rax , {ut.var_mem_asm(node['val']['name'])}")
        text.append(f"mov {ut.var_mem_asm(var_name)} , rax")

    elif val_type == "binexp":
        data.append(f"{var_name} dq 0")
        
        text.extend(formulate_math(node['val'],contex.local_vars))
        text.append(f"mov {ut.var_mem_asm(var_name)}, rax")

    elif val_type == "refrence":
        data.append(f"{var_name} dq 0")

        text.append(f"lea rax, {ut.var_mem_asm(node['val']['name'])}")
        text.append(f"mov [{var_name}], rax")

    elif val_type == "derefrence":
        data.append(f"{var_name} dq 0")
        text.append(f"mov rax, {ut.var_mem_asm(node['name'])}")  # rax = address of pointee
        text.append("mov rax, [rax]")              # rax = value at that address
        text.append(f"mov {ut.var_mem_asm(node['name'])}, rax")

    elif ut.ut.is_arr_type(vartype):
        vars[var_name] = vartype
        if ut.ut.is_arr_type(vartype):
            data.append(var_name+":")
            for nana in node['val']:
                if nana["kind"] == "literal":
                    size = ut.size_lookup(vartype[:-2])
                    directive = {1: '.byte', 2: '.word', 4: '.long', 8: '.quad'}[size]
                    data.append(f"\t{directive} \t{nana['val']}")

