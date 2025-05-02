#evaluates math expresions recursively

prio=["*","/"]

1+2*2+(10/2)
1+2*2+5
1+4+5
5+5
10

def evaluator(a:list):
    brakets= None
    high_p = None
    try:
        if len(a) == 1:
            return
    except:
        return
    
    for i in range(len(a)):
        if(len(a[i])!=1):
            brakets=i
            break
    if brakets == None:
        for i in range(len(a)):
            if(a[i] in prio):
                high_p = i
                break

    if high_p != None:
        if a[high_p]=="*":
            v= a[high_p+1] * a[high_p-1]
        elif:
