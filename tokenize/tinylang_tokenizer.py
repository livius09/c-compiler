#better
#tokenizer
out=[]
operations=["+", "-", "*", "/", "=", "<",">", "==", "!=", "!", "<<", ">>", "&", "|", "^"]
comands = ["let", "return","for","while","break","if","else","func"]

types = ["n8","n16","n32","n64","un8","un16","un32","un64", "void",     
         "n8~","n16~","n32~","n64~","un8~","un16~","un32~","un64~"]

with open("tokenize/input.txt","r") as raw:
    read = raw.read()


def tokenize(line:str):
    i=0
    tokenln=[]
    while i < len(line):
        
        if(line[i].isspace()):
            i+=1
            continue
        
        if(line[i] == "#"):
            i+=1
            while line[i] != "#":
                i+=1
            i+=1
            continue 

        if(line[i] == ","):
            i+=1
            tokenln.append(",")
            continue

        if line[i] == ";":
            if tokenln != []:
                out.append(tokenln)
            tokenln=[]
            i+=1
            continue

        if line[i] == "(":
            tokenln.append("(")
            i+=1
            continue
        
        if line[i] == ")":
            while (line[i+1].isspace()):
                i+=1
            if line[i+1] != "{":
                tokenln.append(")")
            i+=1
            continue
        
        if line[i] =="{":
            if tokenln != []:
                out.append(tokenln)
            out.append("{")
            tokenln=[]
            i+=1
            continue

        if line[i] =="}":
            if tokenln != []:
                out.append(tokenln)
            out.append("}")
            tokenln=[]
            i+=1
            continue

        if line[i] == '"':  #strings will just be turned into char arrs

            if tokenln != []:
                out.append(tokenln)
            tokenln=[]
                
            out.append("{")

            s = ""
            i+=1
            while(i < len(line)) and line[i] != '"':
                s += line[i]
                i+=1

            i+=1

            for ch in s:
                tokenln.append(f"INTEGER>{ord(ch)}")
                tokenln.append(",")

            tokenln.append(f"INTEGER>10")

            out.append(tokenln)
            tokenln = []
            out.append("}")


            continue

        if line[i] == "'":
            if line[i+2] == "'":
                tokenln.append(f"INTEGER>{ord(line[i+1])}")
            else:
                raise SyntaxError(f"chars can only be one char long and need to be closed {line[i+1]}")
            
            i+=3
            continue
                
            
            


            
            
        
        if(line[i].isalpha()):
            s=""
            while(line[i].isalnum() and i < len(line)):
                s+= line[i]
                i+=1

            if line[i]=="+" and line[i+1] == "+":
                i+=2
                #for da i++
                #'IDENTIFIER>i', '=','IDENTIFIER>i','+','INTEGER>1'
                tokenln.append(f"IDENTIFIER>{s}")
                tokenln.append("=")
                tokenln.append(f"IDENTIFIER>{s}")
                tokenln.append("+")
                tokenln.append("INTEGER>1")
                continue

            elif line[i]=="-" and line[i+1] == "-":
                i+=2
                #for da i--
                #'IDENTIFIER>i', '=','IDENTIFIER>i','-','INTEGER>1'
                tokenln.append(f"IDENTIFIER>{s}")
                tokenln.append("=")
                tokenln.append(f"IDENTIFIER>{s}")
                tokenln.append("-")
                tokenln.append("INTEGER>1")
                continue

            if s == "for":
                tokenln.append("for")
                i+=1
                out.append(tokenln)
                tokenln=[]
                continue

            if s == "if":
                tokenln.append("if")
                i+=1
                continue

            if s == "while":
                tokenln.append("if")
                i+=1
                continue
                   

            if(s in comands):
                tokenln.append(s.capitalize())
                continue

            if (s in types):
                if line[i] =="[":
                    tokenln.append(f"TYPE>{s}[]")
                    i+=1
                    si=""
                    while(line[i].isdigit() and i < len(line)):
                        si+=line[i]
                        i+=1
                    if si != "":
                        tokenln.append(f"len>{si}")
                    i+=1
                        
                elif line[i] =="~":
                    tokenln.append(f"TYPE>{s}~")
                else:
                    tokenln.append(f"TYPE>{s}")
                continue
            
            if line[i] =="[":
                i+=1
                pos=""
                while(line[i].isalnum() and i < len(line)):
                    pos+=line[i]
                    i+=1

                tokenln.append(f"ARR>{s}>{pos}")

                continue
                

            if line[i] == "(":
                i+=1
                tokenln.append(f"FUNCT>{s}")
                tokenln.append("(")
                continue

            if line[i-len(s)-1] == "~":
                tokenln.append(f"DEREFRENCE>{s}")
            elif line[i-len(s)-1] == "$":
                tokenln.append(f"REFRENCE>{s}")
            else:
                tokenln.append(f"IDENTIFIER>{s}")

            continue

        if (line[i].isdigit()):
            num=""
            while(line[i].isdigit() and i < len(line)):
                num= num+line[i]
                i+=1
            tokenln.append(f"INTEGER>{num}")
            continue

        if (line[i] in operations):
            if  line[i+1] == line[i] and line[i+1] in operations:   #for the ==, <<, !=, <= and so on 
                tokenln.append(str(line[i]) + str(line[i+1]))
                i+=1
            else:    
                tokenln.append(line[i])
        
        


        i+=1

    return out
    
            


lig = tokenize(read)
with open("tokenize/output.txt", "w") as file:
    file.write(str(lig))

with open("tokenize/readable_out.txt", "w") as file:
    for line in lig:
        file.write(str(line)+"\n")