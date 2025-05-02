#evaluates math expresions recursively

#idea:
#1+2*2+(10/2)
#1+2*2+5
#1+4+5
#5+5
#10

def evaluator(a:list) -> list:
    print(a)
    brakets= None
    high_p = None
    
    
    for i in range(len(a)):         #werer is a braket in the equation
        if(isinstance(a[i],list)):
            brakets=i
            break

    if brakets != None:
        a[brakets] = evaluator(a[brakets])[0]  #solve the braket 
    
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


u=[1,"+",2,"*",2,"+",[1,"+",1]]
print(evaluator(u))
