#parser
[
  {
    "type": "LetDeclaration",
    "var_type": "n32",
    "name": "x",
    "value": {
      "type": "Literal",
      "value": 5
    }
  },
  {
    "type": "ReturnStatement",
    "value": {
      "type": "Identifier",
      "name": "x"
    }
  }
]

#[['Let', 'TYPE>n64', 'IDENTIFIER>x', '=', 'INTEGER>1'], 
# ['Let', 'TYPE>n64', 'IDENTIFIER>x2', '=', 'INTEGER>6', '+', 'IDENTIFIER>x'], 
# ['Func', 'IDENTIFIER>plus', 'TYPE>n64', 'IDENTIFIER>a'], 
# '{', 
# ['Return', 'IDENTIFIER>a'], 
# '}']

with open("tokenize/output.txt","r") as raw:
    read = raw.read()

def parse(line):
  perations=["+","-","*","/","="]
  out = []
  i=1
  tmp = {}
  while (i < len(line)):
    
    
    match line[i]:
        
       
      case "let":
        
        tmp["type"] = "letdec"
        tmp["var_type"] = line[i][1].split(">")[1]
        tmp["name"] = line[i][2].split(">")[1]

        value={}
        math_part=line.split("=")[1]

        if len(math_part) == 1:
          if math_part[0].startswith("IDENTIFIER>"):
            value["type"] = "IDENTIFIER"
            value["name"] = math_part[0].split(">")[1]

          elif  math_part[0].startswith("INTEGER>"):
            value["type"] = "INTEGER"
            value["val"] = int(math_part[0].split(">")[1])
          
          tmp["val"] = value
        else:
          value["type"] = "BINARY_EXP"
          value["op"] = math_part[1]
          value["left"] = math_part[0].split(">")[1]
          value["right"] = math_part[2].split(">")[1]
          tmp["val"] = value
    i+=1
  return tmp
  
          
lal=[['Let', 'TYPE>n64', 'IDENTIFIER>x', '=', 'INTEGER>1']]       
        
print(parse(lal))              
            
     
    
      










def evaluator(a:list) -> list:
    print(a)
    brakets= None
    high_p = None
    prio = ["*", "/"]
    
    
    for i in range(len(a)):         #werer is a braket in the equation
        if(isinstance(a[i],list)):
            a[i] = evaluator(a[i])[0]
            return evaluator(a)
    
    for i in range(len(a)):     #find a * or /
        if(a[i] in prio):
            high_p = i
            break

    if high_p != None:          #solve that * or /
        if a[high_p]=="*":
            v= a[high_p+1] * a[high_p-1]
        elif (a[high_p]=="/"):
                v= a[high_p+1] / a[high_p-1]
        else:
            raise ArithmeticError
        a.pop(high_p+1)
        a[high_p] = v
        a.pop(high_p-1)
    else:                       #if no * or / is found search for an + or -
        for i in range(len(a)):
            if a[i] == "+":
                a[i] = a[i+1] + a[i-1]

                a.pop(i+1)
                a.pop(i-1)
                break

            elif a[i] == "-":
                a[i] = a[i+1] - a[i-1]

                a.pop(i+1)
                a.pop(i-1)
                break
    print(a)
    try:
        if len(a) == 1:
            return a
    except:
        return a
    
    print(a)
    evaluator(a)