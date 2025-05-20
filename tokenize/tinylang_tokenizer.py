#better
#tokenizer
out=[]
operations=["+","-","*","/","=","<",">"]
comands = ["let", "return","for","while","if"]
types = ["n8","n16","n32","n64","un8","un16","un32","un64"]

with open("tokenize/input.txt","r") as raw:
    read = raw.read()


def tokenize(line):
    i=0
    tokenln=[]
    while i < len(line):
        
        if(line[i].isspace()):
            i+=1
            continue

        if(line[i] == ","):
            i+=1
            tokenln.append(",")
            continue

        if line[i] == ";":
            out.append(tokenln)
            tokenln=[]
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
            
            
        
        if(line[i].isalpha()):
            s=""
            while(line[i].isalnum() and i < len(line)):
                s+= line[i]
                i+=1
                
            if s == "func":
                i+=1
                tokenln.append(s.capitalize())
                b=""
                while(line[i].isalnum() and i < len(line)):
                    b+= line[i]
                    i+=1

                tokenln.append(f"NAME>{b}")
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
                    tokenln.append(f"SIZE>{si}")

                tokenln.append(f"TYPE>{s}")
                continue

            if line[i+1] == "(":
                i+=1
                tokenln.append(f"FUNCT>{s}")
                continue

                
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
            tokenln.append(line[i])
        
        


        i+=1

    return out
    
            




with open("tokenize/output.txt", "w") as file:
    file.write(str(tokenize(read)))