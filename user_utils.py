from code_gen.utils_stuff import *

ofset_table = []

# ANSI escape background colors
bg_colors = [
    '\033[41m',  # Red
    '\033[42m',  # Green
    '\033[43m',  # Yellow
    '\033[44m',  # Blue
    '\033[45m',  # Magenta
    '\033[46m',  # Cyan
    '\033[47m',  # White
    '\033[100m', # Grey
]
RESET = '\033[0m'

def add_ofset_table(node: dict):
    var_type = node['var_type']
    var_name = node['var_name']
    type_size = size_lookup(var_type)
    if is_arr_type(var_type):
        var_len = node['len']
        for i in range(var_len-1,-1,-1):
            for k in range(type_size):
                ofset_table.append(f"{var_name}[{i}] byte:{k}")
    else:
        for j in range(type_size):
            ofset_table.append(f"{var_name} byte:{j}")

def print_ofst():
    color_map = {}
    color_index = 0
    index=0

    for entry in ofset_table:
        index-=1
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
        print(str(index)+"\t" + color + entry + RESET)

add_ofset_table({'var_type':"n16[]", 'var_name':"gaga", "len":3 })
add_ofset_table({'var_type':"n8", 'var_name':"nu"})
print_ofst()
