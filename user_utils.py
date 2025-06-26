from code_gen.utils_stuff import *

ofset_table = []

# ANSI escape background colors
bg_colors = [
    '\033[35m',  # Purple
    '\033[42m',  # Green
    '\033[43m',  # Yellow
    '\033[44m',  # Blue
    '\033[45m',  # Magenta
    '\033[46m',  # Cyan
    '\033[47m',  # White
    '\033[100m', # Grey
]
RESET = '\033[0m'

#'\033[41m' red
def add_ofset_table(var_type, var_name, var_len=1):
    if var_type != "pading":

        type_size = size_lookup(var_type)
        if is_arr_type(var_type):
            for i in range(var_len-1,-1,-1):
                for k in range(type_size):
                    ofset_table.append(f"{var_name}[{i}] byte:{k}")
        else:
            for j in range(type_size):
                ofset_table.append(f"{var_name} byte:{j}")
    else:
        for i in range(var_len):
            ofset_table.append("PADING")

def print_ofst():
    color_map = {}
    color_index = 0
    index=0

    for entry in ofset_table:
        index-=1
        if entry != "PADING":
            # Extract the array/group prefix (like a[0], a[1], or just a)
            if '[' in entry:
                prefix = entry.split('[')[0]  # Get the base name like 'arr' from 'arr[0] byte:1'
            else:
                prefix = entry.split(' ')[0]  # Just the variable name

            # Assign a background color for the entire array or var
            if prefix not in color_map:
                color_map[prefix] = bg_colors[color_index % len(bg_colors)]
                color_index += 1

            color = color_map[prefix]
            print("[rbp"+str(index)+"]" + "\t" + color + entry + RESET)
        else:
            print('\033[41m'+"PADDING"+RESET)   #show pading red

    print(f"using: {len(ofset_table)} bytes")
    pading_bytes=0
    for thing in ofset_table:
        if thing == "PADING":
            pading_bytes+=1
    
    print(f"{pading_bytes} of them being \033[41m PADING \033[0m")



add_ofset_table("n16[]", "gaga", 3)
add_ofset_table("n8", "nu")
print_ofst()
