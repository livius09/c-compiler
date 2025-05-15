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

#FunctionDeclaration(
#    name = "plus",
#    parameters = [
#        Parameter(type="n64", name="a"),
#        Parameter(type="n64", name="b")
#    ],
#    body = [
#        ReturnStatement(
#            value = BinaryExpression(
#                left = Identifier("a"),
#                operator = "+",
#                right = Identifier("b")
#            )
#        )
#    ]
#)


#[['Let', 'TYPE>n64', 'IDENTIFIER>x', '=', 'INTEGER>1'], 
# ['Let', 'TYPE>n64', 'IDENTIFIER>x2', '=', 'INTEGER>6', '+', 'IDENTIFIER>x'], 
# ['Func', 'IDENTIFIER>plus', 'TYPE>n64', 'IDENTIFIER>a'], 
# '{', 
# ['Return', 'IDENTIFIER>a'], 
# '}']

#with open("tokenize/output.txt","r") as raw:
#    read = raw.read()

def parse(line):
  operations=["+","-","*","/","="]
  out = []
  i=1
  
  while (i < len(line)):
    
    tmp = {}
    match line[i][1]:
        
      case "}":
        break
       
      
      case "let":
        
        tmp["type"] = "letdec"
        tmp["var_type"] = line[i][1].split(">")[1]
        tmp["name"] = line[i][2].split(">")[1]

        value={}
        math_part = line.split("=")[1]

        if len(math_part) == 1:
          if math_part[0].startswith("IDENTIFIER>"):
            value["type"] = "IDENTIFIER"
            value["name"] = math_part[0].split(">")[1]

          elif  math_part[0].startswith("INTEGER>"):
            value["type"] = "INTEGER"
            value["val"] = int(math_part[0].split(">")[1])
          
          tmp["val"] = value
        else:
          tmp["val"]=par(math_part)
        
      case "func":
        
        tmp["type"] = "function_dec"
        tmp["name"] = line[i][2]
        tmp["parameter"]=[]
        for a in range(1,int(len(line[i])-2),2):
          tmp["parameter"].append({"type":line[i][a].split(">")[1],"name":line[i][a+1].split("")[1]})

        tmp["body"] = parse(line[i+1:])

      case "return":
        tmp["type"]="return"
        tmp["val"] = par(line[i][2:])

      case "if":
          
          

       

    out.append(tmp)   
    i+=1
  return out
  
          
lal=[['Let', 'TYPE>n64', 'IDENTIFIER>x', '=', 'INTEGER>1'],['Let', 'TYPE>n64', 'IDENTIFIER>y', '=', 'INTEGER>1']]       
        
print(parse(lal))              
            
     
    
      

def par(a:list):
  pass
   









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
