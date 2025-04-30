#tokenizer
out=[]
operations=["+","-","*","/"]

with open("input.txt","r") as raw:
    lines = raw.readlines()

for i in range(len(lines)):
    words = lines[i].split(" ")
    tokenln = []

    if (words[0]=="let" and words[2]=="="):
        tokenln.append("LET")
        tokenln.append(f"IDENTIFIER({words[1]})")
        tokenln.append("=")

        math = lines[i].split("=")[1].split(" ")
        
        for word in math:
            if(word==";" or word==";\n"):
                tokenln.append(";")
                break

            if(word in operations):
                tokenln.append(word)
                continue

            if(word.isdigit()):
                tokenln.append(f"INTEGER({word})")
                continue

            tokenln.append(f"IDENTIFIER({words[1]})")
    
    if (words[0]=="return"):
        tokenln.append("RETURN")
        if(word[1].isdigit):
            tokenln.append(f"INTEGER({word})")
        else:
            tokenln.append(f"IDENTIFIER({words[1]})")

    
    out.append(tokenln)

with open("output.txt", "w") as file:
    file.write(str(out))
    