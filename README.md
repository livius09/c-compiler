# compiler
a small project to understand compilers (i know its shity)

more about the lang in zOrga tinylang.txt
##### probably someone thats defenitly not chat gpt:
  This is some very mature compiler design work — a proper recursive descent generator for assembly. It’s seriously impressive. If you want, I can help refine any part of it, or even help you design your AST documentation tomorrow. Just let me know! 🚀🔥

## Changes
### v(major release).(new feature).(bug fixes and small stuff)

#### v01.0.7:
  fixed a long standing bug were global inits never wrote to data
  codegen now registers structs and initializes them corectly
  updated docs for a new struct description that is used in codegen to acces members and keep tract of structs
  
#### v01.0.6:
  updated main.py to use the new lexer and parser

#### v01.0.5:
  uppdated the parser to handle struct related things also removed REF DEREF as they are now operations.
  uppdated the doc to include a AST-Node for structs
  also solved a bug in the tokenizer telling wrong lines (allways sayign zero)

#### v01.0.4:
  rewrote the parser whit a class but still being recursive and producing the same AST

#### v01.0.3:
  rewrote the tokenizer made it shorter and well better

#### v01.0.2:
  implemented the ability to use variables and literals like true in the if/for/while expresions

#### v01.0.1:
  yeah fine and nice litle commit.
  fixe if up a bit
  unified if and if_else into one handeler and one ast kind
  made if(1){} posible


#### v01.0.0:
  wow we made it.
  who is we idk but yeah.
  well i did.
  made a unified interface in main.py just write you code in input.txt press run in main.py and the asm should apear in out.txt
  also made a lot of fixes to fuction_dec and how parameter are given over to functions

#### v0.9.0:
  added suport for constanst in form of constexpr they dont need types but they suport math if it can be simplyfied at compile time

#### v0.8.0:
  big uppdate moved all the handles to an extra fille, implemented context obj, enabled coments by #...# some fixes to functions and returs to

#### v0.7.0:
  BIG BOMBOCLAT added:  local vs global vars, read write suport for that, fixed some stuff, added mem read size like WORD PTR big step towards actuly runing that stuff,
  took an fucking eternity
  also cleaned up a bit moved helper functions to utils_stuff.py 
  created user_utils.py for recurses for debuging and seeing what going on for now only a memory table printer (more planed or sth)

  main:
    mov computer, code
    mov "human", food
    mov computer, code
    mov "human", food
    mov sleep, 2 am
  jmp main
  

#### v0.6.0:
  added arrays you now can read and write from/to arrays 

#### v0.5.0:
  added refrencing, derefrencing and pointer var types also beter naming and consistensi of var names also created the ast documentation

#### v0.4.0:
  did a lot of stuff including fixing some naming of keys in the dict but mainly writing code gen for loops 

#### v0.3.2:
  finished tokenizing and parsing while and for loops 

#### v0.3.1:
  fixed some problems whit tokenizing the bracets on ifs and loops

#### v0.3:
  started on logic for loops and finished for ifs and logic epx

#### v0.2:
  started versioning here
  added: if and else and enabled logic expresions

#### before:
  variables types math declaration 
  
