import tokens as tk

# -------------------------------
# funcs para chequear tipos de nombres y números
# -------------------------------
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

# -------------------------------
# funcs para control structures (IF, WHILE, REPEAT, FOR, ELSE, THEN)
# -------------------------------
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

# -------------------------------
# funcs para proc calls 
# -------------------------------
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
