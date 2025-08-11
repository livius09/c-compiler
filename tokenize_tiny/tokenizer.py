#better
#tokenizer
out=[]
operations=["+","-","*","/","=",";"]
comands = ["let", "return"]

with open("input.txt","r") as raw:
    lines = raw.readlines()

tokenln=[]

for line in lines:
    i=0
    tokenln=[]
    while i < len(line):
        
        if(line[i].isspace()):
            i+=1
            continue

        if (line[i].isdigit()):
            num=""
            while(line[i].isdigit() and i < len(line)):
                num= num+line[i]
                i+=1
            tokenln.append(f"INTEGER({num})")
            continue

        if (line[i] in operations):
            tokenln.append(line[i])
        
        if(line[i].isalpha()):
            s=""
            while(line[i].isalnum() and i < len(line)):
                s+= line[i]
                i+=1

            if(s in comands):
                tokenln.append(s.capitalize())
                continue
            
            tokenln.append(f"IDENTIFIER({s})")

            continue


        i+=1

    out.append(tokenln)
            




with open("output.txt", "w") as file:
    file.write(str(out))