

class preprocesor:
    
    def __init__(self, raw:list[str]) -> None:
        self.raw: list[str] = raw;
        self.imports = []

    def preproces(self):
        i=0
        while(i<len(self.raw)):
            if (self.raw[i].startswith("##")): #preprocesor directive
                directive: str = self.raw[i][2:]
                cmd: str = directive.split(" ")[0]
                args: str = " ".join(directive.split(" ")[1:])
                self.raw.pop(i)

                match cmd:
                    case "import":
                        pass
                    case "warning":
                        print("WARNING:")
                        print(args)

                pass
            elif(self.raw[i].startswith("#")): #comment
                self.raw.pop(i)
            else:
                i+=1

            

        return "".join(self.raw)