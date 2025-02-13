import tokens as tk


def parserMain(lstTokens)-> bool:
    correcta=True
    
    try:
        while len(lstTokens)!=0:
            token=lstTokens[0]
            
            if token[0]==tk.TK_Name:
                checkTK_NAME(lstTokens)
            elif token[0]==tk.TK_VAR_DIV:
                checkTK_VAR_DIV(lstTokens)
            elif token[0]==tk.TK_VAR_ASSIGN:
                checkTK_VAR_ASSIGN(lstTokens)
            elif token[0]==tk.TK_PROC:
                proc_name=checkTK_PROC(lstTokens)
                opcionesInstrucciones(lstTokens, proc_name)
                opcionesIfLoopFor(lstTokens, proc_name)
            elif token[0]==tk.TK_CODEBLOCK_DIVLEFT:
                checkTK_CODEBLOCK_DIVLEFT(lstTokens)
                opcionesInstrucciones(lstTokens)
                opcionesIfLoopFor(lstTokens)
            #elif token[0]==tk.TK_CODEBLOCK_DIVRIGHT:
                #checkTK_CODEBLOCK_DIVRIGHT(lstTokens)
            elif token[0]==tk.TK_LEFT:
                checkTK_LEFT(lstTokens)
            elif token[0]==tk.TK_RIGHT:
                checkTK_RIGHT(lstTokens)
            elif token[0]==tk.TK_AROUND:
                checkTK_AROUND(lstTokens)
            elif token[0]==tk.TK_BACK:
                checkTK_BACK(lstTokens)
            elif token[0]==tk.TK_FRONT:
                checkTK_FRONT(lstTokens)
            elif token[0]==tk.TK_NORTH:
                checkTK_NORTH(lstTokens)
            elif token[0]==tk.TK_SOUTH:
                checkTK_SOUTH(lstTokens)
            elif token[0]==tk.TK_WEST:
                checkTK_WEST(lstTokens)
            elif token[0]==tk.TK_EAST:
                checkTK_EAST(lstTokens)
            elif token[0]==tk.TK_BALLOONS:
                checkTK_BALLOONS(lstTokens)
            elif token[0]==tk.TK_CHIPS:
                checkTK_CHIPS(lstTokens)
            elif token[0]==tk.TK_TOTHE:
                checkTK_TOTHE(lstTokens)
            elif token[0]==tk.TK_INDIR:
                checkTK_INDIR(lstTokens)
            elif token[0]==tk.TK_NOP:
                checkTK_NOP(lstTokens)
            elif token[0]==tk.TK_PUNTO:
                checkTK_PUNTO(lstTokens)
            elif token[0]==tk.TK_NUMERO:
                checkTK_NUMERO(lstTokens)
            elif token[0]==tk.TK_NAMEPUNTOS:
                checkTK_NAMEPUNTOS(lstTokens)
            else:
                checkTK_Name(lstTokens)
                
            """ elif token[0]==tk.TK_THEN:
                checkTK_THEN(lstTokens)
            elif token[0]==tk.TK_ELSE:
                checkTK_ELSE(lstTokens)
            elif token[0]==tk.TK_DO:
                checkTK_DO(lstTokens)
            elif token[0]==tk.TK_REPEAT:
                checkTK_REPEAT(lstTokens)
            elif token[0]==tk.TK_WITH:
                checkTK_WITH(lstTokens)
            elif token[0]==tk.TK_FACING:
                checkTK_FACING(lstTokens)
            elif token[0]==tk.TK_CANPUT:
                checkTK_CANPUT(lstTokens)
            elif token[0]==tk.TK_CANPICK:
                checkTK_CANPICK(lstTokens)
            elif token[0]==tk.TK_CANMOVE:
                checkTK_CANMOVE(lstTokens)
            elif token[0]==tk.TK_CANJUMP:
                checkTK_CANJUMP(lstTokens)
            elif token[0]==tk.TK_NOT:
                checkTK_NOT(lstTokens)
            """
    except:
        correcta=False
    
    return correcta
    
def opcionesInstrucciones(lstTokens, nombreProc=""):
    if token[0]==tk.TK_GOTO:
        checkTK_GOTO(lstTokens, nombreProc)
    elif token[0]==tk.TK_PICK:
        checkTK_PICK(lstTokens, nombreProc)
    elif token[0]==tk.TK_MOVE:
        checkTK_MOVE(lstTokens,nombreProc)
    elif token[0]==tk.TK_TURN:
        checkTK_TURN(lstTokens,nombreProc)
    elif token[0]==tk.TK_FACE:
        checkTK_FACE(lstTokens,nombreProc)
    elif token[0]==tk.TK_MOVE:
        checkTK_MOVE(lstTokens,nombreProc)
    elif token[0]==tk.TK_PUT:
        checkTK_PUT(lstTokens,nombreProc)
    elif token[0]==tk.TK_JUMP:
        checkTK_JUMP(lstTokens,nombreProc)


def opcionesIfLoopFor(lstTokens, nombreProc=""):
    if token[0]==tk.TK_IF:
        checkTK_IF(lstTokens, nombreProc)
    elif token[0]==tk.TK_WHILE:
        checkTK_WHILE(lstTokens, nombreProc)
    elif token[0]==tk.TK_FOR:
        checkTK_FOR(lstTokens, nombreProc)

# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤
# funcs para chequear tipos de nombres y números
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤

def checkTK_NAME(lstTokens):
    """
    Verifica si el token actual es un nombre válido.
    Si es un nombre suelto, eliminar comas innecesarias y determinar si es un nombre o número.
    """
    token_type, token_value = lstTokens[0]
    if token_type == tk.TK_UNKNOWN:
        if token_value.replace('.', '', 1).isdigit():
            lstTokens[0] = (tk.TK_NUMERO, token_value)
        elif ':' in token_value:
            lstTokens[0] = (tk.TK_NAMEPUNTOS, token_value)
        else:
            lstTokens[0] = (tk.TK_NAME, token_value)
    return lstTokens

def checkTK_NUMERO(lstTokens):
    """
    Verifica si un token es un número y lo clasifica correctamente.
    """
    token_type, token_value = lstTokens[0]
    if token_type == tk.TK_UNKNOWN and token_value.replace('.', '', 1).isdigit():
        lstTokens[0] = (tk.TK_NUMERO, token_value)
    return lstTokens

def checkTK_NAMEPUNTOS(lstTokens):
    """
    Verifica si un token representa un nombre con puntos (:), como nombres de procedimientos.
    """
    token_type, token_value = lstTokens[0]
    if token_type == tk.TK_UNKNOWN and ':' in token_value:
        lstTokens[0] = (tk.TK_NAMEPUNTOS, token_value)
    return lstTokens

# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤
# funcs para control structures (IF, WHILE, REPEAT, FOR, ELSE, THEN)
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤

def checkTK_IF(lstTokens):
    """
    Verifica la estructura del condicional IF asegurando que tenga condición y bloques válidos,
    permitiendo anidamiento de corchetes y verificando que se cierren correctamente.
    """
    if lstTokens and lstTokens[0][0] == tk.TK_IF:
        lstTokens.pop(0)
        if lstTokens and lstTokens[0][0] in [tk.TK_FACING, tk.TK_CANMOVE, tk.TK_CANJUMP, tk.TK_NOT]:
            lstTokens.pop(0)
            if lstTokens and lstTokens[0][0] == tk.TK_THEN:
                lstTokens.pop(0)
                return checkNestedBrackets(lstTokens)
    return lstTokens  # error en la estructura de IF

def checkTK_WHILE(lstTokens):
    """
    Verifica la estructura del loop WHILE asegurándose de que tenga condición y bloque válido,
    permitiendo anidamiento de corchetes y verificando que se cierren correctamente.
    """
    if lstTokens and lstTokens[0][0] == tk.TK_WHILE:
        lstTokens.pop(0)
        if lstTokens and lstTokens[0][0] in [tk.TK_FACING, tk.TK_CANMOVE, tk.TK_CANJUMP, tk.TK_NOT]:
            lstTokens.pop(0)
            if lstTokens and lstTokens[0][0] == tk.TK_DO:
                lstTokens.pop(0)
                return checkNestedBrackets(lstTokens)
    return lstTokens  # error en la estructura de WHILE

def checkTK_REPEAT(lstTokens):
    """
    Verifica la estructura del loop REPEAT asegurando que tenga
    un número de repeticiones válido y un bloque de código.
    """
    if lstTokens and lstTokens[0][0] == tk.TK_REPEAT:
        lstTokens.pop(0)
        if lstTokens and lstTokens[0][0] in [tk.TK_NUMERO, tk.TK_NAME]:
            lstTokens.pop(0)
            return checkNestedBrackets(lstTokens)
    return lstTokens  # error en la estructura de REPEAT

def checkTK_FOR(lstTokens):
    """
    Verifica la estructura del loop FOR asegurando que tenga una variable,
    un rango válido y un bloque de código.
    """
    if lstTokens and lstTokens[0][0] == tk.TK_FOR:
        lstTokens.pop(0)
        if lstTokens and lstTokens[0][0] == tk.TK_NAME:  # variable del for
            lstTokens.pop(0)
            if lstTokens and lstTokens[0][0] in [tk.TK_NUMERO, tk.TK_NAME]:  # inicio del rango
                lstTokens.pop(0)
                if lstTokens and lstTokens[0][0] in [tk.TK_NUMERO, tk.TK_NAME]:  # fin del rango
                    lstTokens.pop(0)
                    return checkNestedBrackets(lstTokens)
    return lstTokens  # error en la estructura de FOR

def checkTK_ELSE(lstTokens):
    """
    Verifica la estructura del bloque ELSE asegurando que tenga
    un bloque de código válido.
    """
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

def checkNestedBrackets(lstTokens):
    """
    Función auxiliar que verifica anidamiento de corchetes.
    """
    if lstTokens and lstTokens[0][0] == tk.TK_CODEBLOCK_DIVLEFT:
        lstTokens.pop(0)
        nested_count = 1
        while lstTokens and nested_count > 0:
            if lstTokens[0][0] == tk.TK_CODEBLOCK_DIVLEFT:
                nested_count += 1
            elif lstTokens[0][0] == tk.TK_CODEBLOCK_DIVRIGHT:
                nested_count -= 1
            lstTokens.pop(0)
        return lstTokens if nested_count == 0 else []  #chequea que todos los bloques se cerraron 
    return lstTokens  # si hay error en la estructura

# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤
# funcs para proc calls 
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤

def checkTK_PROC(lstTokens):
    """
    Verifica la estructura de una declaración de procedimiento,
    asegurando que tenga un nombre válido y un bloque correctamente cerrado.
    """
    if lstTokens and lstTokens[0][0] == tk.TK_PROC:
        lstTokens.pop(0)
        if lstTokens and lstTokens[0][0] == tk.TK_NAMEPUNTOS:
            lstTokens.pop(0)
            return checkNestedBrackets(lstTokens)
    return lstTokens  #no es un proc, continua 

def checkTK_VAR_ASSIGN(lstTokens):
    """
    Verifica la estructura de una asignación de variable asegurando que tenga un valor válido.
    """
    if lstTokens and lstTokens[0][0] == tk.TK_NAME:
        lstTokens.pop(0)
        if lstTokens and lstTokens[0][0] == tk.TK_VAR_ASSIGN:
            lstTokens.pop(0)
            if lstTokens and lstTokens[0][0] in [tk.TK_NUMERO, tk.TK_NAME]:
                lstTokens.pop(0)
                return lstTokens  #completada
    return lstTokens  # no es una asign de variable, continua 

def checkTK_PROCCALL(lstTokens):
    """
    chequea que los procedures definidos sean llamados correctamente.
    Una llamada debe terminar con . (goNorth.). Si tiene parámetros, 
    se revisa que se pasen en la cantidad y formato correctos.
    """
    if not lstTokens:
        return lstTokens
        
    token_type, token_value = lstTokens[0]
    if token_type != tk.TK_NAME and token_type != tk.TK_NAMEPUNTOS:
        return lstTokens
    
    lstTokens.pop(0)  #nombre del proc
    
    #chequea parametros si existen
    while lstTokens and lstTokens[0][0] in [tk.TK_NUMERO, tk.TK_NAME]:
        lstTokens.pop(0)
        
    # miro que termine con punto
    if not lstTokens or lstTokens[0][0] != tk.TK_PUNTO:
        return lstTokens
        
    lstTokens.pop(0)  # el punto
    return lstTokens

def checkTK_INSTRUCCION(lstTokens):
    """
    Revisa que una instrucción básica esté correctamente formada.
    Instrucciones como: move, turn, face, put, pick, jump, etc.
    """
    if not lstTokens:
        return lstTokens
        
    token_type = lstTokens[0][0]
    valid_instructions = [
        tk.TK_MOVE, tk.TK_TURN, tk.TK_FACE, tk.TK_PUT, 
        tk.TK_PICK, tk.TK_JUMP, tk.TK_NOP, tk.TK_GOTO,
        tk.TK_WITH, tk.TK_TOTHE, tk.TK_INDIR
    ]
    
    if token_type not in valid_instructions:
        return lstTokens
        
    lstTokens.pop(0)
    
    #chequea cositass especificas segun el tipo de instrucción
    if token_type in [tk.TK_TURN, tk.TK_FACE]:
        if not lstTokens or lstTokens[0][0] not in [tk.TK_NORTH, tk.TK_SOUTH, tk.TK_EAST, tk.TK_WEST,
                                            tk.TK_LEFT, tk.TK_RIGHT, tk.TK_AROUND, tk.TK_BACK, tk.TK_FRONT]:
            return lstTokens
        lstTokens.pop(0)
    elif token_type in [tk.TK_PUT, tk.TK_PICK]:
        if not lstTokens or lstTokens[0][0] not in [tk.TK_BALLOONS, tk.TK_CHIPS]:
            return lstTokens
        lstTokens.pop(0)
    
    # miro que termine con punto
    if not lstTokens or lstTokens[0][0] != tk.TK_PUNTO:
        return lstTokens
        
    lstTokens.pop(0)
    return lstTokens

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

def checkTK_MOVE(lstTokens, nombreProc=""):
    lstTokens.pop(0)
    
    if lstTokens[0][0]==tk.TK_NUMERO or check_ValidVariable(lstTokens, nombreProc):
        lstTokens.pop(0)
        
        if lstTokens[0][0]==tk.TK_PUNTO:
            lstTokens.pop(0) 
        else:
            raise Exception("token turn")
        
    else:
        raise Exception("token move")

def check_TK_TURN(lstTokens, nombreProc=""):
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
                    raise Exception("token pick")        
            else:
                raise Exception("token pick")
        else:
            raise Exception("token pick")
    else:
        raise Exception("token pick")
    
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤
# funcs de auxiliares
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤ 

#Chequea si el token es una variable valida de tipo TK_NAME
def check_ValidVariable(lstTokens, nombreProc="")->bool:
    nombreVar=lstTokens[0][1]
    
    if lstTokens[0][0]==tk.TK_NAME:
        if variables_globales.count(nombreVar)>0:
            return True
        elif variables_locales.get(nombreProc) is not None:
            return True
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
    elif lstTokens[0][0]==tk.TK_RIGHT:
        return True
    else:
        return False

# type: ignore
 
 
procedures=[]
variables_globales=[]
variables_locales=dict()