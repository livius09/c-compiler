class node:
    def __init__(self,name:str,child:list) -> None:
        self.file:str = name
        self.children:list[node]=child
    def __repr__(self) -> str:
        return self.file + ":" + str(self.children)
    

def find_circular(node:node,prev:list=[]) -> bool:
    
    if(node.file in prev):
        return True

    prev.append(node.file)

    for child in node.children:
        return find_circular(child,list(prev))
        
    return False

class preprocesor:
    
    def __init__(self, start_file:str) -> None:
        self.start=start_file
        self.raw: list[str] = []
        self.imports :node = node(start_file,[])

    def preproces(self) -> node:

        try:
            with open(f"Zin/{self.start}.txt","r") as rawf:
                self.raw = rawf.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"{self.start}.txt cant be imported because it was not found")

        i=0
        while(i<len(self.raw)):
            if (self.raw[i].startswith("##")): #preprocesor directive
                directive: str = self.raw[i][2:].strip()
                cmd: str = directive.split(" ")[0]
                args: str = " ".join(directive.split(" ")[1:])
                self.raw.pop(i)

                match cmd:
                    case "import":
                        file: str = args 

                        pre = preprocesor(file)
                        
                        self.imports.children.append(pre.preproces())
                    

                        
                    case "warning":
                        print("WARNING:")
                        print(args)

                pass
            elif(self.raw[i].startswith("#")): #comment
                self.raw.pop(i)
            else:
                i+=1

            

        return self.imports