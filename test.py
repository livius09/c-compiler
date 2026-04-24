import tokenize_tiny.tinylang_tokenizer as ttok
import parse_tiny.tinylang_parser as tlpars
import code_gen.tinylang_x86_codegen as tcod
from code_gen.utils_stuff import contextc
from Prepocesor.preprocesor import preprocesor, find_circular, node

import json
import datetime

with open(f"Zin/stdt.txt","r") as rawf:
    raw: str = rawf.read()


Tokenize = ttok.Tokenizerc(raw)
Tokenize.Tokenize()


tokens = Tokenize.tokens

print(f"tokenized: s")
print(tokens)

Pparser = tlpars.parserc(tokens) # type: ignore # yeah it works so idk why it yaps


parsed = Pparser.parse()

print(f"parsed:  s")
print(json.dumps(parsed,indent=4))