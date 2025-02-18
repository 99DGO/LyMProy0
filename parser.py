import tokens as tk
import traceback 
 
procedures=[]
variables_globales=[]
variables_locales=dict()

def parserMain(lstTokens)-> bool:
    correcta=True
    token=lstTokens[0]
    
    try:
        if token[0]==tk.TK_VAR_DIV:
            checkTK_VAR_DIV(lstTokens)
                
        while len(lstTokens)!=0:
            token=lstTokens[0]
                
            if token[0]==tk.TK_PROC:
                procName_sublistTokens=checkTK_PROC(lstTokens)
                proc_name=procName_sublistTokens[0]
                sublistTokens=procName_sublistTokens[1]

                if not len(sublistTokens)==0:
                    token=sublistTokens[0];
                    
                    if token[0]==tk.TK_VAR_DIV:
                        checkTK_VAR_DIV(sublistTokens, proc_name)
                        
                    while len(sublistTokens)!=0: 
                        token=sublistTokens[0];
                        boolInst=opcionesInstrucciones(sublistTokens, proc_name)
                        
                        if not len(sublistTokens)==0:
                            token=sublistTokens[0];
                            boolIf=opcionesIfLoopFor(sublistTokens, proc_name)
                            
                            if token[0]==tk.TK_NAME:
                                checkTK_NAME(sublistTokens, proc_name)
                            elif not boolIf and not boolInst:
                                raise Exception("menu parser")

                    
            elif token[0]==tk.TK_CODEBLOCK_DIVLEFT:
                sublistTokens=[]
                sublistTokens=checkNestedBrackets(lstTokens, sublistTokens)
                
                while len(sublistTokens)!=0: 
                    token=sublistTokens[0];
                    boolInst=opcionesInstrucciones(sublistTokens)

                    if not len(sublistTokens)==0:
                        token=sublistTokens[0];
                        boolIf=opcionesIfLoopFor(sublistTokens)
                        if token[0]==tk.TK_NAME:
                            checkTK_NAME(sublistTokens)
                        elif not boolIf and not boolInst:
                            raise Exception("menu parser")
            else:
                raise Exception("menu parser")          
    except Exception as e:
        correcta=False
        #traceback.print_exc()
    
    return correcta
    
def opcionesInstrucciones(lstTokens, nombreProc=""):
    if not len(lstTokens)==0:
        token = lstTokens[0]
        
        if token[0]==tk.TK_GOTO:
            checkTK_GOTO(lstTokens, nombreProc)
            return True
        elif token[0]==tk.TK_PICK:
            checkTK_PICK(lstTokens, nombreProc)
            return True
        elif token[0]==tk.TK_MOVE:
            checkTK_MOVE(lstTokens,nombreProc)
            return True
        elif token[0]==tk.TK_TURN:
            checkTK_TURN(lstTokens,nombreProc)
            return True
        elif token[0]==tk.TK_FACE:
            checkTK_FACE(lstTokens,nombreProc)
            return True
        elif token[0]==tk.TK_PUT:
            checkTK_PUT(lstTokens,nombreProc)
            return True
        elif token[0]==tk.TK_JUMP:
            checkTK_JUMP(lstTokens,nombreProc)
            return True
        elif token[0]==tk.TK_NOP:
            checkTK_NOP(lstTokens)
            return True
        else:
            return False
    else:
        return True


def opcionesIfLoopFor(lstTokens, nombreProc=""):
    if not len(lstTokens)==0:
        token = lstTokens[0]

        if token[0]==tk.TK_IF:
            checkTK_IF(lstTokens, nombreProc)
            return True
        elif token[0]==tk.TK_WHILE:
            checkTK_WHILE(lstTokens, nombreProc)
            return True
        elif token[0]==tk.TK_FOR:
            checkTK_FOR(lstTokens, nombreProc)
            return True
        else:
            return False
    else:
        return True

# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤
# funcs para chequear tipos de nombres y números
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤

def checkTK_NAME(lstTokens, nombreProc=""):
    if lstTokens and lstTokens[0][0] == tk.TK_NAME:
        return checkTK_VAR_ASSIGN(lstTokens, nombreProc)
    return lstTokens

def checkTK_NUMERO(lstTokens):
    
    token_type, token_value = lstTokens[0]
    if token_type == tk.TK_UNKNOWN and token_value.replace('.', '', 1).isdigit():
        lstTokens[0] = (tk.TK_NUMERO, token_value)
    return lstTokens

def checkTK_NAMEPUNTOS(lstTokens):
    
    token_type, token_value = lstTokens[0]
    if token_type == tk.TK_UNKNOWN and ':' in token_value:
        lstTokens[0] = (tk.TK_NAMEPUNTOS, token_value)
    return lstTokens

# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◢◤◢◤◢◤
# funcs para control structures (IF, WHILE, REPEAT, FOR, ELSE, THEN)
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤

def checkTK_IF(lstTokens, nombreProc=""):
    sublistTokens = []
    if lstTokens and lstTokens[0][0] == tk.TK_IF:
        lstTokens.pop(0)
        if lstTokens and lstTokens[0][0] in [tk.TK_FACING, tk.TK_CANMOVE, tk.TK_CANJUMP, tk.TK_NOT, tk.TK_CANPUT, tk.TK_CANPICK]:
            token_type = lstTokens[0][0]
            lstTokens.pop(0)
            
            # para CANPUT, CANPICK, CANMOVE necesitamos chequear n
            if token_type in [tk.TK_CANPUT, tk.TK_CANPICK, tk.TK_CANMOVE]:
                if lstTokens[0][0] == tk.TK_NUMERO:
                    lstTokens.pop(0)
                elif check_ValidVariable(lstTokens, nombreProc):
                    lstTokens.pop(0)
                else:
                    raise Exception("Se esperaba número o variable válida")
                
                # para CANPUT y CANPICK chequear tipo
                if token_type in [tk.TK_CANPUT, tk.TK_CANPICK]:
                    if lstTokens[0][0] not in [tk.TK_BALLOONS, tk.TK_CHIPS]:
                        raise Exception("Se esperaba balloons o chips")
                    lstTokens.pop(0)
            
            if lstTokens and lstTokens[0][0] == tk.TK_THEN:
                lstTokens.pop(0)
                return checkNestedBrackets(lstTokens, sublistTokens)
    return lstTokens

def checkTK_WHILE(lstTokens, nombreProc=""):
    sublistTokens = []
    if lstTokens and lstTokens[0][0] == tk.TK_WHILE:
        lstTokens.pop(0)
        if lstTokens and lstTokens[0][0] in [tk.TK_FACING, tk.TK_CANMOVE, tk.TK_CANJUMP, tk.TK_NOT, tk.TK_CANPUT, tk.TK_CANPICK]:
            token_type = lstTokens[0][0]
            lstTokens.pop(0)
            
            # para CANPUT, CANPICK, CANMOVE necesitamos  chequear n
            if token_type in [tk.TK_CANPUT, tk.TK_CANPICK, tk.TK_CANMOVE]:
                if lstTokens[0][0] == tk.TK_NUMERO:
                    lstTokens.pop(0)
                elif check_ValidVariable(lstTokens, nombreProc):
                    lstTokens.pop(0)
                else:
                    raise Exception("Se esperaba número o variable válida")
                
                #para CANPUT y CANPICK chequear tipo
                if token_type in [tk.TK_CANPUT, tk.TK_CANPICK]:
                    if lstTokens[0][0] not in [tk.TK_BALLOONS, tk.TK_CHIPS]:
                        raise Exception("Se esperaba balloons o chips")
                    lstTokens.pop(0)
            
            if lstTokens and lstTokens[0][0] == tk.TK_DO:
                lstTokens.pop(0)
                return checkNestedBrackets(lstTokens, sublistTokens)
    return lstTokens

def checkTK_REPEAT(lstTokens, nombreProc=""):
    sublistTokens = []
    if lstTokens and lstTokens[0][0] == tk.TK_REPEAT:
        lstTokens.pop(0)
        if lstTokens[0][0] == tk.TK_NUMERO:
            lstTokens.pop(0)
        elif check_ValidVariable(lstTokens, nombreProc):
            lstTokens.pop(0)
        else:
            raise Exception("Se esperaba número o variable válida")
        return checkNestedBrackets(lstTokens, sublistTokens)
    return lstTokens

def checkTK_FOR(lstTokens, nombreProc=""):
    sublistTokens = []
    if lstTokens and lstTokens[0][0] == tk.TK_FOR:
        lstTokens.pop(0)
        if lstTokens and lstTokens[0][0] == tk.TK_NAME:  # variable del for
            lstTokens.pop(0)
            #chequeo inicio y fin del rango
            for _ in range(2):  
                if lstTokens[0][0] == tk.TK_NUMERO:
                    lstTokens.pop(0)
                elif check_ValidVariable(lstTokens, nombreProc):
                    lstTokens.pop(0)
                else:
                    raise Exception("Se esperaba número o variable válida")
            return checkNestedBrackets(lstTokens, sublistTokens)
    return lstTokens

def checkTK_ELSE(lstTokens):
    
    if lstTokens and lstTokens[0][0] == tk.TK_ELSE:
        lstTokens.pop(0)
        return checkNestedBrackets(lstTokens)
    return lstTokens  # no es un else, continua

def checkTK_THEN(lstTokens):
    """
    Verifica la estructura del bloque THEN asegurando que tenga
    un bloque de código válido.
    """
    if lstTokens and lstTokens[0][0] == tk.TK_THEN:
        lstTokens.pop(0)
        return checkNestedBrackets(lstTokens)
    return lstTokens  # no es un then, continua

def checkNestedBrackets(lstTokens, sublistTokens):
    if lstTokens and lstTokens[0][0] == tk.TK_CODEBLOCK_DIVLEFT:
        lstTokens.pop(0)
        nested_count = 1
        
        while lstTokens and nested_count > 0:
            if not lstTokens:  # Si se acaban los tokens y nested_count > 0
                raise Exception("Falta corchete de cierre ']'")
                
            token = lstTokens[0]
            
            if token[0] == tk.TK_CODEBLOCK_DIVLEFT:
                nested_count += 1
                lstTokens.pop(0)
            elif token[0] == tk.TK_CODEBLOCK_DIVRIGHT:
                nested_count -= 1
                lstTokens.pop(0)
            else:
                # si no es un corchete, agregar a la sublista de parserMain
                sublistTokens.append(lstTokens.pop(0))
        
        if nested_count > 0:  # Si terminamos los tokens pero aún faltan corchetes por cerrar
            raise Exception("Falta corchete de cierre ']'")
            
        return sublistTokens if nested_count == 0 else []
    return lstTokens

# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤
# funcs para proc calls 
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤


def checkTK_PROC(lstTokens):
    sublistTokens = []
    if lstTokens and lstTokens[0][0] == tk.TK_PROC:
        lstTokens.pop(0)
        
        # chequea si es un nombre simple o con parámetros
        if lstTokens and lstTokens[0][0] == tk.TK_NAME:  # caso sin parámetros
            proc_name = lstTokens[0][1]
            procedures.append(proc_name)
            variables_locales[proc_name] = []  # proc sin parámetros
            lstTokens.pop(0)
            return [proc_name, checkNestedBrackets(lstTokens, sublistTokens)]
            
        elif lstTokens and lstTokens[0][0] == tk.TK_NAMEPUNTOS:  # caso con parámetros
            proc_name = lstTokens[0][1].rstrip(':')  # quito los : del nombre
            procedures.append(proc_name)
            variables_locales[proc_name] = []  #lista de params
            lstTokens.pop(0)
            
            # procesar parametros hasta encontrar '['
            while lstTokens and lstTokens[0][0] == tk.TK_NAME:
                param_name = lstTokens[0][1]
                variables_locales[proc_name].append(param_name)  # agrego param a la lista del proc
                lstTokens.pop(0)
                
                # si hay mas parámetros, debe venir ':'
                if lstTokens and lstTokens[0][0] != tk.TK_CODEBLOCK_DIVLEFT:
                    if lstTokens[0][0] == tk.TK_NAMEPUNTOS:
                        lstTokens.pop(0)
                        # luego de ':' debe venir otro nombre
                        if not (lstTokens and lstTokens[0][0] == tk.TK_NAME):
                            raise Exception("se esperaba un nombre después de ':'")
                    else:
                        raise Exception("se esperaba ':' o '[' después del parámetro")
            
            return [proc_name, checkNestedBrackets(lstTokens, sublistTokens)]
            
    return lstTokens  # no es un proc, continua


def checkTK_VAR_ASSIGN(lstTokens, nombreProc=""):
    if lstTokens and lstTokens[0][0] == tk.TK_NAME:
        nombre = lstTokens[0][1]
        if not (nombre in variables_globales or nombre in variables_locales.get(nombreProc, [])):
            raise Exception(f"Variable {nombre} no declarada")
        lstTokens.pop(0)
        
        if lstTokens and lstTokens[0][0] == tk.TK_VAR_ASSIGN:
            lstTokens.pop(0)
            if lstTokens and lstTokens[0][0] in [tk.TK_NUMERO, tk.TK_NAME]:
                if lstTokens[0][0] == tk.TK_NAME:
                    var_nombre = lstTokens[0][1]
                    if not (var_nombre in variables_globales or var_nombre in variables_locales.get(nombreProc, [])):
                        raise Exception(f"Variable {var_nombre} no declarada")
                lstTokens.pop(0)
                if lstTokens and lstTokens[0][0] == tk.TK_PUNTO:
                    lstTokens.pop(0)
                    return lstTokens
                else:
                    raise Exception("Falta punto después de la asignación")
            else:
                raise Exception("Se esperaba número o nombre después de :=")
        else:
            raise Exception("Se esperaba := después del nombre")
    return lstTokens

def checkTK_PROCCALL(lstTokens):
    
    if not lstTokens:
        return lstTokens
        
    token_type, token_value = lstTokens[0]
    if token_type != tk.TK_NAME and token_type != tk.TK_NAMEPUNTOS:
        return lstTokens
    
    #verifico que el procedimiento existe
    proc_name = token_value.rstrip(':')  # quitar los : si los hay
    if variables_locales.get(proc_name) is None:
        raise Exception(f"Procedimiento '{proc_name}' no está definido")
    
    lstTokens.pop(0)  #nombre del proc
    
    #chequea parametros si existen
    while lstTokens and lstTokens[0][0] in [tk.TK_NUMERO, tk.TK_NAME]:
        lstTokens.pop(0)
        
    # miro que termine con punto
    if not lstTokens or lstTokens[0][0] != tk.TK_PUNTO:
        return lstTokens
        
    lstTokens.pop(0)  # el punto
    return lstTokens



# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤
# funcs de variable declarations
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤
 
def checkTK_VAR_DIV(lstTokens, nombreProc=""):
    lstTokens.pop(0) 
    
    boolVarDivReached=False
    
    while not boolVarDivReached:
        if lstTokens[0][0]==tk.TK_NAME:
            varName=lstTokens[0][1]
            lstTokens.pop(0)
            if nombreProc=="":
                variables_globales.append(varName)
            else:
                lstVar=variables_locales.get(nombreProc)
                lstVar.append(varName)
        elif lstTokens[0][0]==tk.TK_VAR_DIV:
            lstTokens.pop(0)
            boolVarDivReached=True
        else:
            raise Exception()
 
 
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤
# funcs de instrucciones
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤
 
def checkTK_GOTO(lstTokens, nombreProc=""):
    #Quito el goto 
    lstTokens.pop(0)
    if (lstTokens[0][0]==tk.TK_NUMERO) or (check_ValidVariable(lstTokens, nombreProc)):
        #Quito el numero 
        lstTokens.pop(0)
        
        if lstTokens[0][0]==tk.TK_WITH:
            #Quito el with
            lstTokens.pop(0)
            
            if  check_ValidVariable(lstTokens, nombreProc) or lstTokens[0][0]==tk.TK_NUMERO:
                lstTokens.pop(0)
                
                if lstTokens[0][0]==tk.TK_PUNTO:
                    lstTokens.pop(0) 
                else:
                    raise Exception("token goto")        
            else:
                raise Exception("token goto")
        else:
            raise Exception("token goto")
    else:
        raise Exception("token goto")

def checkTK_TURN(lstTokens, nombreProc=""):
    lstTokens.pop(0)
    
    if lstTokens[0][0]==tk.TK_LEFT or lstTokens[0][0]==tk.TK_RIGHT or lstTokens[0][0]==tk.TK_AROUND:
        lstTokens.pop(0)
        
        if lstTokens[0][0]==tk.TK_PUNTO:
            lstTokens.pop(0) 
        else:
            raise Exception("token turn")
    
    else: 
        raise Exception("token turn")
    
def checkTK_FACE(lstTokens, nombreProc=""):
    lstTokens.pop(0)
    
    if check_Direction_NESW(lstTokens):
        lstTokens.pop(0)
        
        if lstTokens[0][0]==tk.TK_PUNTO:
            lstTokens.pop(0) 
        else:
            raise Exception("token face")
        
    else:
        raise Exception("token face")
 
 
def checkTK_PUT(lstTokens, nombreProc=""):
    #Quito el goto 
    lstTokens.pop(0)
    if (lstTokens[0][0]==tk.TK_NUMERO) or (check_ValidVariable(lstTokens, nombreProc)):
        #Quito el numero 
        lstTokens.pop(0)
        
        if lstTokens[0][0]==tk.TK_OFTYPE:
            #Quito el of type
            lstTokens.pop(0)
            
            if  lstTokens[0][0]==tk.TK_BALLOONS or lstTokens[0][0]==tk.TK_CHIPS:
                lstTokens.pop(0)
                
                if lstTokens[0][0]==tk.TK_PUNTO:
                    lstTokens.pop(0) 
                else:
                    raise Exception("token put")        
            else:
                raise Exception("token put")
        else:
            raise Exception("token put")
    else:
        raise Exception("token put")

def checkTK_PICK(lstTokens, nombreProc=""):
    #Quito el goto 
    lstTokens.pop(0)
    if (lstTokens[0][0]==tk.TK_NUMERO) or (check_ValidVariable(lstTokens, nombreProc)):
        #Quito el numero 
        lstTokens.pop(0)
        
        if lstTokens[0][0]==tk.TK_OFTYPE:
            #Quito el of type
            lstTokens.pop(0)
            
            if  lstTokens[0][0]==tk.TK_BALLOONS or lstTokens[0][0]==tk.TK_CHIPS:
                lstTokens.pop(0)
                
                if lstTokens[0][0]==tk.TK_PUNTO:
                    lstTokens.pop(0) 
                else:
                    raise Exception("token pick")        
            else:
                raise Exception("token pick")
        else:
            raise Exception("token pick")
    else:
        raise Exception("token pick")
  
def checkTK_MOVE(lstTokens, nombreProc=""):
    #Quito el goto 
    lstTokens.pop(0)
    if (lstTokens[0][0]==tk.TK_NUMERO) or (check_ValidVariable(lstTokens, nombreProc)):
        #Quito el numero 
        lstTokens.pop(0)
        
        if lstTokens[0][0]==tk.TK_TOTHE:
            lstTokens.pop(0)
            
            if  check_Direction_FBLR(lstTokens):
                lstTokens.pop(0)
                
                if lstTokens[0][0]==tk.TK_PUNTO:
                    lstTokens.pop(0) 
                else:
                    raise Exception("token MOVE")        
            else:
                raise Exception("token MOVE")
            
        elif lstTokens[0][0]==tk.TK_INDIR:
            lstTokens.pop(0)
            
            if  check_Direction_NESW(lstTokens):
                lstTokens.pop(0)
                
                if lstTokens[0][0]==tk.TK_PUNTO:
                    lstTokens.pop(0) 
                else:
                    raise Exception("token MOVE")        
            else:
                raise Exception("token MOVE")
            
        elif lstTokens[0][0]==tk.TK_PUNTO:
            lstTokens.pop(0)
        
        else: 
            raise Exception("token MOVE")
    else:
        raise Exception("token MOVE")

def checkTK_JUMP(lstTokens, nombreProc=""):
    #Quito el goto 
    lstTokens.pop(0)
    if (lstTokens[0][0]==tk.TK_NUMERO) or (check_ValidVariable(lstTokens, nombreProc)):
        #Quito el numero 
        lstTokens.pop(0)
        
        if lstTokens[0][0]==tk.TK_TOTHE:
            lstTokens.pop(0)
            
            if  check_Direction_FBLR(lstTokens):
                lstTokens.pop(0)
                
                if lstTokens[0][0]==tk.TK_PUNTO:
                    lstTokens.pop(0) 
                else:
                    raise Exception("token JUMP")        
            else:
                raise Exception("token JUMP")
            
        elif lstTokens[0][0]==tk.TK_INDIR:
            lstTokens.pop(0)
            
            if  check_Direction_NESW(lstTokens):
                lstTokens.pop(0)
                
                if lstTokens[0][0]==tk.TK_PUNTO:
                    lstTokens.pop(0) 
                else:
                    raise Exception("token JUMP")        
            else:
                raise Exception("token JUMP")
        
        elif lstTokens[0][0]==tk.TK_PUNTO:
            lstTokens.pop(0)
        
        else: 
            raise Exception("token JUMP")
    else:
        raise Exception("token JUMP")

def checkTK_NOP(lstTokens, nombreProc=""):
    lstTokens.pop(0)    
    if lstTokens[0][0]==tk.TK_PUNTO:
        lstTokens.pop(0) 
    else:
        raise Exception("token nop")  
    
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◢◤◢◤◢◤
# funcs de auxiliares
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤

#Chequea si el token es una variable valida de tipo TK_NAME
def check_ValidVariable(lstTokens, nombreProc="")->bool:
    nombreVar=lstTokens[0][1]
    
    if lstTokens[0][0]==tk.TK_NAME:
        if variables_globales.count(nombreVar)>0:
            return True
        elif variables_locales.get(nombreProc) is not None:
            lstVar=variables_locales.get(nombreProc)
            if nombreVar in lstVar:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def check_Direction_NESW(lstTokens)->bool:
    if lstTokens[0][0]==tk.TK_EAST:
        return True
    elif lstTokens[0][0]==tk.TK_NORTH:
        return True
    elif lstTokens[0][0]==tk.TK_SOUTH:
        return True
    elif lstTokens[0][0]==tk.TK_WEST:
        return True
    else:
        return False
    
def check_Direction_FBLR(lstTokens)->bool:
    if lstTokens[0][0]==tk.TK_FRONT:
        return True
    elif lstTokens[0][0]==tk.TK_RIGHT:
        return True
    elif lstTokens[0][0]==tk.TK_BACK:
        return True
    elif lstTokens[0][0]==tk.TK_LEFT:
        return True
    else:
        return False

# type: ignore
 

