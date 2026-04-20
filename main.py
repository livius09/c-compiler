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
from Prepocesor.preprocesor import preprocesor;
import json
import datetime

with open("Zin/inpats.txt","r") as rawf:
    raw: list[str] = rawf.readlines()


preprocesor= preprocesor(raw)
preporaw = preprocesor.preproces()

tok_start: datetime.datetime = datetime.datetime.now()

Tokenize = ttok.Tokenizerc(preporaw)
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

comp_end: datetime.datetime = datetime.datetime.now()

print(f"\ncode gen:  {comp_end-comp_start} s")
print("data: \n")
for line in tcod.data:
    print(line)

print("\ntext:\n")

for line in compiled:
    print(line)



with open("Zout/Main.asm","w") as file:
    file.write("data:\n")
    for b in tcod.data:
        file.write("\t"+b+"\n")
    file.write("text:\n")
    for a in compiled:
        file.write("\t"+a+"\n")
    file.close