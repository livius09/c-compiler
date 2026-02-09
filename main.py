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
import json

with open("inpats.txt","r") as rawf:
    raw = rawf.read()

Tokenize = ttok.Tokenizerc(raw)
Tokenize.Tokenize()

tokens = Tokenize.tokens

print("tokenized:") 
print(tokens)


Pparser = tlpars.parserc(tokens)

parsed = Pparser.parse()

print("parsed:")
print(json.dumps(parsed,indent=4))

start_contx = contextc(is_global=True)
compiled = tcod.gen(parsed, start_contx)

print("compiled:")
print(compiled)

with open("out.txt","w") as file:
    file.write("data:\n")
    for b in []:
        file.write("\t"+b+"\n")
    file.write("text:\n")
    for a in compiled:
        file.write("\t"+a+"\n")
    file.close

