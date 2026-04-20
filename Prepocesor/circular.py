class node:
    def __init__(self,name:str,child:list) -> None:
        self.file:str = name
        self.children:list[node]=child
    def __repr__(self) -> str:
        return self.file + ":" + str(self.children)
    

def find_circular(node:node,prev:list) -> bool:
    
    if(node.file in prev):
        return True

    prev.append(node.file)

    for child in node.children:
        if find_circular(child,list(prev)):
            return True
        
    return False


        

tree =  node("A",[node("B",[node("A",[])])])
print(tree)
print(find_circular(tree,[]))