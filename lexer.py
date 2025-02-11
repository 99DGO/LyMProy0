import tokens as tk

#Retorna una lista que contiene tuplas adentro.
#Primer elemento de la tupla es el tipo de token, segundo elemento es mas para los nombres de cosas
# como variables y procedimientos
#En el caso de nombres sueltos, hay que asegurarse de eliminar comas en funciones futuras 
# y chequear si es un string de numero o un nombre nombre
def tokenize(inputString) -> list:
    lstTokens=[]
    
    lstSplit=inputString.split(" ")
    
    for subString in lstSplit:
        #Chequeo si es algun token normal
        token=checkIfToken(subString)
        
        if token[0].length()!="":
            lstTokens.append(token)
        else:
            #Chequeo si es algun simbolo pegado a otra cosa
            #En caso de que este una variable pegada, se convierten en TK_UNKNOWN        
            i=0
            while i<subString.length():
                if subString[i]=="[":
                    lstTokens.append((tk.TK_CODEBLOCK_DIVLEFT, ""))

                elif subString[i]=="]":
                    lstTokens.append((tk.TK_CODEBLOCK_DIVRIGHT, ""))

                elif subString[i]==".":
                    lstTokens.append((tk.TK_PUNTO, ""))
                    
                elif subString[i]=="|":
                    lstTokens.append((tk.TK_VAR_DIV, ""))
                        
                elif subString[i]==":=":
                    lstTokens.append(tk.TK_VAR_ASSIGN, "")
    
                else:
                    lstTokens.append(tk.TK_UNKNOWN, subString[i])
                    
                i+=1                     
            
    return cleanUnknowns(lstTokens, lstNombresPuntos, lstNombresSueltos)
    
    
        
TK_NAME
TK_NUMERO
TK_NAMEPUNTOS

def cleanUnknowns(unkLstTokens):
    
    #Recorrer toda la lista de tokens
    #Si hay un unknown, chequear si hay otros unknowns después
    #Juntarlos para crear un token name, un token numero, o un token namepuntos y reemplazarlo los 
    #token unknown por el nuevo token. 
    cleanedLstTokens=[]
    
    i1=0;
    while i1<unkLstTokens.size():
        a
        
    return cleanedLstTokens

    
def checkIfToken(subString)-> str:
    if subString==tk.TK_PROC:
        return (tk.TK_PROC.clone(), "")
    elif subString==tk.TK_CODEBLOCK_DIVLEFT:
        return (tk.TK_CODEBLOCK_DIVLEFT.clone(), "")
    elif subString==tk.TK_CODEBLOCK_DIVRIGHT:
        return (tk.TK_CODEBLOCK_DIVRIGHT.clone(), "")
    elif subString==tk.TK_VAR_DIV:
        return (tk.TK_VAR_DIV.clone(), "")
    elif subString==tk.TK_VAR_ASSIGN:
        return (tk.TK_VAR_ASSIGN.clone(), "")
    elif subString==tk.TK_GOTO:
        return (tk.TK_GOTO.clone(), "")
    elif subString==tk.TK_WITH:
        return (tk.TK_WITH.clone(), "")
    elif subString==tk.TK_MOVE:
        return (tk.TK_MOVE.clone(), "")
    elif subString==tk.TK_TURN:
        return (tk.TK_TURN.clone(), "")
    elif subString==tk.TK_LEFT:
        return (tk.TK_LEFT.clone(), "")
    elif subString==tk.TK_RIGHT:
        return (tk.TK_RIGHT.clone(), "")
    elif subString==tk.TK_AROUND:
        return (tk.TK_AROUND.clone(), "")
    elif subString==tk.TK_FACE:
        return (tk.TK_FACE.clone(), "")
    elif subString==tk.TK_NORTH:
        return (tk.TK_NORTH.clone(), "")
    elif subString==tk.TK_SOUTH:
        return (tk.TK_SOUTH.clone(), "")
    elif subString==tk.TK_WEST:
        return (tk.TK_WEST.clone(), "")
    elif subString==tk.TK_EAST:
        return (tk.TK_EAST.clone(), "")
    elif subString==tk.TK_PUT:
        return (tk.TK_PUT.clone(), "")
    elif subString==tk.TK_BALLOONS:
        return (tk.TK_BALLOONS.clone(), "")
    elif subString==tk.TK_CHIPS:
        return (tk.TK_CHIPS.clone(), "")
    elif subString==tk.TK_PICK:
        return (tk.TK_PICK.clone(), "")
    elif subString==tk.TK_MOVE:
        return (tk.TK_MOVE.clone(), "")
    elif subString==tk.TK_TOTHE:
        return (tk.TK_TOTHE.clone(), "")
    elif subString==tk.TK_INDIR:
        return (tk.TK_INDIR.clone(), "")
    elif subString==tk.TK_NOP:
        return (tk.TK_NOP.clone(), "")
    elif subString==tk.TK_BACK:
        return (tk.TK_BACK.clone(), "")
    elif subString==tk.TK_FRONT:
        return (tk.TK_FRONT.clone(), "")
    elif subString==tk.TK_IF:
        return (tk.TK_IF.clone(), "")
    elif subString==tk.TK_THEN:
        return (tk.TK_THEN.clone(), "")
    elif subString==tk.TK_ELSE:
        return (tk.TK_ELSE.clone(), "")
    elif subString==tk.TK_WHILE:
        return (tk.TK_WHILE.clone(), "")
    elif subString==tk.TK_DO:
        return (tk.TK_DO.clone(), "")
    elif subString==tk.TK_FOR:
        return (tk.TK_FOR.clone(), "")
    elif subString==tk.TK_REPEAT:
        return (tk.TK_REPEAT.clone(), "")
    elif subString==tk.TK_FACING:
        return (tk.TK_FACING.clone(), "")
    elif subString==tk.TK_CANPUT:
        return (tk.TK_CANPUT.clone(), "")
    elif subString==tk.TK_OFTYPE:
        return (tk.TK_OFTYPE.clone(), "")
    elif subString==tk.TK_CANPICK:
        return (tk.TK_CANPICK.clone(), "")
    elif subString==tk.TK_CANMOVE:
        return (tk.TK_CANMOVE.clone(), "")
    elif subString==tk.TK_CANJUMP:
        return (tk.TK_CANJUMP.clone(), "")
    elif subString==tk.TK_NOT:
        return (tk.TK_NOT.clone(), "")
    elif subString==tk.TK_PUNTO:
        return (tk.TK_PUNTO.clone(), "")
    else:
        return ("","")