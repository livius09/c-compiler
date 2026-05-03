#pipeline pattern

#get the input
#call the lexer
#call the parser
#call codegen
#link asm ?
#use nasm to compile asm
#run or/and output the elf binary

import tokenize_tiny.tinylang_tokenizer as ttok
import parse_tiny.tinylang_parser as tlpars
import code_gen.tinylang_x86_codegen as tcod
from code_gen.utils_stuff import contextc
from Prepocesor.preprocesor import preprocesor, find_circular, node

import json
import datetime




def compile(file:str):
    print(f"started compiling {file}")

    tok_start: datetime.datetime = datetime.datetime.now()

    with open(f"Zin/{file}.txt","r") as rawf:
        raw: str = rawf.read()


    Tokenize = ttok.Tokenizerc(raw)
    Tokenize.Tokenize()

    tok_end: datetime.datetime = datetime.datetime.now()
    tokens = Tokenize.tokens

    print(f"tokenized:  {tok_end-tok_start} s")
    print(tokens)

    par_start = datetime.datetime.now()

    Pparser = tlpars.parserc(tokens) # type: ignore # yeah it works so idk why it yaps


    parsed = Pparser.parse()

    par_end = datetime.datetime.now()

    print(f"parsed: {par_end-par_start} s")
    print(json.dumps(parsed,indent=4))

    comp_start: datetime.datetime = datetime.datetime.now()

    start_contx = contextc(is_global=True)
    compiled = tcod.gen(parsed, start_contx)

    exports: dict[str, dict[str, str | list[str]]] = tcod.functions

    comp_end: datetime.datetime = datetime.datetime.now()

    print(f"\ncode gen:  {comp_end-comp_start} s")
    print("data: \n")
    for line in tcod.data:
        print(line)

    print("\ntext:\n")

    for line in compiled:
        print(line)



    with open(f"Zout/{file}.asm","w") as fileOut:
        fileOut.write("data:\n")
        for b in tcod.data:
            fileOut.write("\t"+b+"\n")
        fileOut.write("text:\n")
        for a in compiled:
            fileOut.write("\t"+a+"\n")
        fileOut.close

    return exports



def compile_down_up(nedo:node):
    if(nedo.children!=[]):
        colect = {}
        for node in nedo.children:
            colect.update(compile_down_up(node))
    
    try:
        export =  compile(nedo.file) 
    except Exception as e:
        e.add_note(" in "+nedo.file+".txt")
        raise

    return export


preprocesor = preprocesor("Main")
print("Preprocesing: ")
print("imports: ")
imports : node = preprocesor.preproces()
print(imports)

if find_circular(imports):
    raise ImportError("")

compile_down_up(imports)



