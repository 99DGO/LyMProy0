import tokens as tk

#Retorna una lista que contiene tuplas adentro.
#Primer elemento de la tupla es el tipo de token, segundo elemento es mas para los nombres de cosas
# como variables y procedimientos

def tokenize(inputString) -> list:
    lstTokens=[]
    
    lstSplit=inputString.split(" ")
    
    for uncleanSubString in lstSplit:
        #Chequeo si es algun token normal
        subString=uncleanSubString.replace("\n", "")
        token=checkIfToken(subString)
        
        if len(token[0])!=0:
            lstTokens.append(token)
        else:
            #Chequeo si es algun simbolo pegado a otra cosa
            #En caso de que este una variable pegada, se convierten en TK_UNKNOWN        
            i=0
            while i<len(subString):
                if subString[i]=="[":
                    lstTokens.append((tk.TK_CODEBLOCK_DIVLEFT, ""))

                elif subString[i]=="]":
                    lstTokens.append((tk.TK_CODEBLOCK_DIVRIGHT, ""))

                elif subString[i]==".":
                    lstTokens.append((tk.TK_PUNTO, ""))
                    
                elif subString[i]=="|":
                    lstTokens.append((tk.TK_VAR_DIV, ""))
                        
                elif subString[i]==":=":
                    lstTokens.append((tk.TK_VAR_ASSIGN, ""))
    
                else:
                    if subString[i]==subString[-1]:
                        lstTokens.append((tk.TK_UNKNOWN_END, subString[i]))
                    else:
                        lstTokens.append((tk.TK_UNKNOWN, subString[i]))
                    
                i+=1                     
     
    return cleanUnknowns(lstTokens)

def cleanUnknowns(unkLstTokens):
    
    #Recorrer toda la lista de tokens
    #Si hay un unknown, chequear si hay otros unknowns después
    #Juntarlos para crear un token name, un token numero, o un token namepuntos y reemplazarlo los 
    #token unknown por el nuevo token. 
    cleanedLstTokens=[]
    
    i1=0;
    while i1<len(unkLstTokens):
        if unkLstTokens[i1][0]!= tk.TK_UNKNOWN and unkLstTokens[i1][0]!= tk.TK_UNKNOWN_END :
            cleanedLstTokens.append(unkLstTokens[i1])
        else:
            unknown=unkLstTokens[i1][1]
            i2=i1+1
            continua=True
            
            #Añado los unknownTokens a unknown
            while i2<len(unkLstTokens) and continua:
                if unkLstTokens[i2-1][0]!=tk.TK_UNKNOWN_END:
                    if unkLstTokens[i2][0]==tk.TK_UNKNOWN or unkLstTokens[i2][0]==tk.TK_UNKNOWN_END:
                        unknown+=unkLstTokens[i2][1]
                        i1=i2
                        i2+=1
                    else:
                        continua=False
                    """ 
                    elif unkLstTokens[i2][0]==tk.TK_UNKNOWN_END:
                        unknown+=unkLstTokens[i2][1]
                        i1=i2
                        break
                    """
                else:
                    break
            
            #Chequeo que es unknown y lo añado
            token=checkIfToken(unknown)
        
            if len(token[0])!=0:
                cleanedLstTokens.append(token)
            elif unknown[-1]==":":
                cleanedLstTokens.append((tk.TK_NAMEPUNTOS, unknown[:-1]))
            elif unknown.isdigit():
                cleanedLstTokens.append((tk.TK_NUMERO, unknown))
            else:
                if unknown[-1]==",":
                    cleanedLstTokens.append((tk.TK_NAME, unknown[:-1]))
                else:
                    cleanedLstTokens.append((tk.TK_NAME, unknown))
        
        i1+=1
        
    return cleanedLstTokens

    
def checkIfToken(subString)-> str:
    if subString==tk.TK_PROC:
        return (tk.TK_PROC, "")
    elif subString==tk.TK_CODEBLOCK_DIVLEFT:
        return (tk.TK_CODEBLOCK_DIVLEFT, "")
    elif subString==tk.TK_CODEBLOCK_DIVRIGHT:
        return (tk.TK_CODEBLOCK_DIVRIGHT, "")
    elif subString==tk.TK_VAR_DIV:
        return (tk.TK_VAR_DIV, "")
    elif subString==tk.TK_VAR_ASSIGN:
        return (tk.TK_VAR_ASSIGN, "")
    elif subString==tk.TK_GOTO:
        return (tk.TK_GOTO, "")
    elif subString==tk.TK_WITH:
        return (tk.TK_WITH, "")
    elif subString==tk.TK_MOVE:
        return (tk.TK_MOVE, "")
    elif subString==tk.TK_JUMP:
        return (tk.TK_JUMP, "")
    elif subString==tk.TK_TURN:
        return (tk.TK_TURN, "")
    elif subString==tk.TK_LEFT:
        return (tk.TK_LEFT, "")
    elif subString==tk.TK_RIGHT:
        return (tk.TK_RIGHT, "")
    elif subString==tk.TK_AROUND:
        return (tk.TK_AROUND, "")
    elif subString==tk.TK_FACE:
        return (tk.TK_FACE, "")
    elif subString==tk.TK_NORTH:
        return (tk.TK_NORTH, "")
    elif subString==tk.TK_SOUTH:
        return (tk.TK_SOUTH, "")
    elif subString==tk.TK_WEST:
        return (tk.TK_WEST, "")
    elif subString==tk.TK_EAST:
        return (tk.TK_EAST, "")
    elif subString==tk.TK_PUT:
        return (tk.TK_PUT, "")
    elif subString==tk.TK_BALLOONS:
        return (tk.TK_BALLOONS, "")
    elif subString==tk.TK_CHIPS:
        return (tk.TK_CHIPS, "")
    elif subString==tk.TK_PICK:
        return (tk.TK_PICK, "")
    elif subString==tk.TK_MOVE:
        return (tk.TK_MOVE, "")
    elif subString==tk.TK_TOTHE:
        return (tk.TK_TOTHE, "")
    elif subString==tk.TK_INDIR:
        return (tk.TK_INDIR, "")
    elif subString==tk.TK_NOP:
        return (tk.TK_NOP, "")
    elif subString==tk.TK_BACK:
        return (tk.TK_BACK, "")
    elif subString==tk.TK_FRONT:
        return (tk.TK_FRONT, "")
    elif subString==tk.TK_IF:
        return (tk.TK_IF, "")
    elif subString==tk.TK_THEN:
        return (tk.TK_THEN, "")
    elif subString==tk.TK_ELSE:
        return (tk.TK_ELSE, "")
    elif subString==tk.TK_WHILE:
        return (tk.TK_WHILE, "")
    elif subString==tk.TK_DO:
        return (tk.TK_DO, "")
    elif subString==tk.TK_FOR:
        return (tk.TK_FOR, "")
    elif subString==tk.TK_REPEAT:
        return (tk.TK_REPEAT, "")
    elif subString==tk.TK_FACING:
        return (tk.TK_FACING, "")
    elif subString==tk.TK_CANPUT:
        return (tk.TK_CANPUT, "")
    elif subString==tk.TK_OFTYPE:
        return (tk.TK_OFTYPE, "")
    elif subString==tk.TK_CANPICK:
        return (tk.TK_CANPICK, "")
    elif subString==tk.TK_CANMOVE:
        return (tk.TK_CANMOVE, "")
    elif subString==tk.TK_CANJUMP:
        return (tk.TK_CANJUMP, "")
    elif subString==tk.TK_NOT:
        return (tk.TK_NOT, "")
    elif subString==tk.TK_PUNTO:
        return (tk.TK_PUNTO, "")
    else:
        return ("","")