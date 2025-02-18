import tokens as tk
import traceback 
 
procedures=[]
variables_globales=[]
variables_locales=dict()

def parserMain(lstTokens):
    try:
        # Procesar declaraciones de variables globales si existen
        if lstTokens and lstTokens[0][0] == tk.TK_VAR_DIV:
            checkTK_VAR_DIV(lstTokens)
            
        # Procesar cada procedimiento o instrucción
        while lstTokens:
            token = lstTokens[0]
            
            if token[0] == tk.TK_PROC:
                result = checkTK_PROC(lstTokens)
                if isinstance(result, list):
                    proc_name, proc_tokens = result
                    # Procesar el cuerpo del procedimiento
                    while proc_tokens:
                        if not process_instruction(proc_tokens, proc_name):
                            return False
                else:
                    lstTokens = result
            else:
                if not process_instruction(lstTokens):
                    return False
                    
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def process_instruction(lstTokens, nombreProc=""):
    if not lstTokens:
        return True
        
    token = lstTokens[0]
    
    # Procesar declaraciones de variables locales
    if token[0] == tk.TK_VAR_DIV:
        checkTK_VAR_DIV(lstTokens, nombreProc)
        return True
        
    # Procesar estructuras de control
    elif token[0] == tk.TK_IF:
        lstTokens = checkTK_IF(lstTokens, nombreProc)
        return True
    elif token[0] == tk.TK_WHILE:
        lstTokens = checkTK_WHILE(lstTokens, nombreProc)
        return True
    elif token[0] == tk.TK_REPEAT:
        lstTokens = checkTK_REPEAT(lstTokens, nombreProc)
        return True
    elif token[0] == tk.TK_FOR:
        lstTokens = checkTK_FOR(lstTokens, nombreProc)
        return True
        
    # Procesar instrucciones simples
    elif token[0] == tk.TK_MOVE:
        checkTK_MOVE(lstTokens, nombreProc)
        return True
    elif token[0] == tk.TK_TURN:
        checkTK_TURN(lstTokens, nombreProc)
        return True
    elif token[0] == tk.TK_FACE:
        checkTK_FACE(lstTokens, nombreProc)
        return True
    elif token[0] == tk.TK_PUT:
        checkTK_PUT(lstTokens, nombreProc)
        return True
    elif token[0] == tk.TK_PICK:
        checkTK_PICK(lstTokens, nombreProc)
        return True
    elif token[0] == tk.TK_JUMP:
        checkTK_JUMP(lstTokens, nombreProc)
        return True
    elif token[0] == tk.TK_NOP:
        checkTK_NOP(lstTokens, nombreProc)
        return True
    elif token[0] == tk.TK_GOTO:
        checkTK_GOTO(lstTokens, nombreProc)
        return True
    elif token[0] == tk.TK_NAME:
        # Podría ser una asignación o llamada a procedimiento
        if len(lstTokens) > 1 and lstTokens[1][0] == tk.TK_VAR_ASSIGN:
            checkTK_VAR_ASSIGN(lstTokens, nombreProc)
        else:
            checkTK_PROCCALL(lstTokens)
        return True
        
    return False

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
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◢◢◤◢◤◢◤

def checkTK_IF(lstTokens, nombreProc=""):
    sublistTokens = []
    if lstTokens and lstTokens[0][0] == tk.TK_IF:
        lstTokens.pop(0)
        
        # Verificar si hay dos puntos después del if (opcional)
        if lstTokens and lstTokens[0][0] == tk.TK_NAMEPUNTOS:
            lstTokens.pop(0)
            
        # Debugging: imprimir los próximos tokens
        print("Próximos tokens después de if:")
        for i in range(min(3, len(lstTokens))):
            print(f"Token {i}: tipo={lstTokens[0][0]}, valor={lstTokens[0][1]}")
            
        # Aquí está el cambio principal - usar las constantes de tokens.py
        valid_conditions = [
            "facing:",      # tk.TK_FACING
            "canMove:",     # tk.TK_CANMOVE
            "canJump:",     # tk.TK_CANJUMP
            "not:",        # tk.TK_NOT
            "canPut:",     # tk.TK_CANPUT
            "canPick:"     # tk.TK_CANPICK
        ]
        
        if lstTokens and (lstTokens[0][0] in valid_conditions):
            token_type = lstTokens[0][0]
            lstTokens.pop(0)
            
            # Procesar la condición
            if token_type == "facing:":  # tk.TK_FACING
                if not lstTokens:
                    raise Exception("Se esperaba dirección NESW")
                if not check_Direction_NESW(lstTokens):
                    raise Exception("Se esperaba dirección NESW")
                lstTokens.pop(0)
                
            elif token_type == "not:":  # tk.TK_NOT
                # Verificar que sigue una condición válida
                if not lstTokens or lstTokens[0][0] not in [tk.TK_FACING, tk.TK_CANMOVE, tk.TK_CANJUMP, tk.TK_CANPUT, tk.TK_CANPICK]:
                    raise Exception("Se esperaba una condición válida después de not")
                
                # Procesar la condición que sigue al not
                next_token_type = lstTokens[0][0]
                lstTokens.pop(0)
                
                if next_token_type == tk.TK_FACING:
                    if not lstTokens:
                        raise Exception("Se esperaba dirección NESW")
                    if not check_Direction_NESW(lstTokens):
                        raise Exception("Se esperaba dirección NESW")
                    lstTokens.pop(0)
                    
                elif next_token_type in [tk.TK_CANMOVE, tk.TK_CANJUMP]:
                    # Verificar n
                    if not lstTokens:
                        raise Exception("Se esperaba número o variable válida")
                    if lstTokens[0][0] == tk.TK_NUMERO:
                        lstTokens.pop(0)
                    elif check_ValidVariable(lstTokens, nombreProc):
                        lstTokens.pop(0)
                    else:
                        raise Exception("Se esperaba número o variable válida")
                        
                elif next_token_type in [tk.TK_CANPUT, tk.TK_CANPICK]:
                    # Verificar n
                    if not lstTokens:
                        raise Exception("Se esperaba número o variable válida")
                    if lstTokens[0][0] == tk.TK_NUMERO:
                        lstTokens.pop(0)
                    elif check_ValidVariable(lstTokens, nombreProc):
                        lstTokens.pop(0)
                    else:
                        raise Exception("Se esperaba número o variable válida")
                    
                    # Verificar ofType
                    if not lstTokens or lstTokens[0][0] != tk.TK_OFTYPE:
                        raise Exception("Se esperaba ofType")
                    lstTokens.pop(0)
                    
                    if not lstTokens or lstTokens[0][0] not in [tk.TK_BALLOONS, tk.TK_CHIPS]:
                        raise Exception("Se esperaba balloons o chips")
                    lstTokens.pop(0)
            
            elif token_type in [tk.TK_CANMOVE, tk.TK_CANJUMP, tk.TK_CANPUT, tk.TK_CANPICK]:
                # Verificar n
                if not lstTokens:
                    raise Exception("Se esperaba número o variable válida")
                if lstTokens[0][0] == tk.TK_NUMERO:
                    lstTokens.pop(0)
                elif check_ValidVariable(lstTokens, nombreProc):
                    lstTokens.pop(0)
                else:
                    raise Exception("Se esperaba número o variable válida")
                
                # Si es CANPUT o CANPICK, verificar ofType y tipo
                if token_type in [tk.TK_CANPUT, tk.TK_CANPICK]:
                    if not lstTokens or lstTokens[0][0] != tk.TK_OFTYPE:
                        raise Exception("Se esperaba ofType")
                    lstTokens.pop(0)
                    
                    if not lstTokens or lstTokens[0][0] not in [tk.TK_BALLOONS, tk.TK_CHIPS]:
                        raise Exception("Se esperaba balloons o chips")
                    lstTokens.pop(0)
            
            # Verificar then o then:
            if not lstTokens:
                raise Exception("Falta then")
            
            if (lstTokens[0][0] == tk.TK_THEN or 
                (lstTokens[0][0] == tk.TK_NAME and lstTokens[0][1] == "then")):
                lstTokens.pop(0)
                
                # Si hay dos puntos después del then, consumirlos
                if lstTokens and lstTokens[0][0] == tk.TK_NAMEPUNTOS:
                    lstTokens.pop(0)
                elif lstTokens and lstTokens[0][0] == tk.TK_THEN:
                    lstTokens.pop(0)
                    
                return checkNestedBrackets(lstTokens, sublistTokens)
            else:
                raise Exception(f"Falta then (token actual: {lstTokens[0][0]}, valor: {lstTokens[0][1]})")
        else:
            print("Tokens esperados:", [tk.TK_FACING, tk.TK_CANMOVE, tk.TK_CANJUMP, tk.TK_NOT, tk.TK_CANPUT, tk.TK_CANPICK])
            raise Exception(f"Se esperaba una condición válida. Token encontrado: tipo={lstTokens[0][0]}, valor={lstTokens[0][1]}")
    return lstTokens

def checkTK_WHILE(lstTokens, nombreProc=""):
    sublistTokens = []
    if lstTokens and lstTokens[0][0] == tk.TK_WHILE:
        lstTokens.pop(0)
        
        # Verificar si hay dos puntos después del while (opcional)
        if lstTokens and lstTokens[0][0] == tk.TK_NAMEPUNTOS:
            lstTokens.pop(0)
            
        if lstTokens and lstTokens[0][0] in [tk.TK_FACING, tk.TK_CANMOVE, tk.TK_CANJUMP, tk.TK_NOT, tk.TK_CANPUT, tk.TK_CANPICK]:
            token_type = lstTokens[0][0]
            lstTokens.pop(0)
            
            if token_type == tk.TK_FACING:
                if not lstTokens:
                    raise Exception("Se esperaba dirección NESW")
                if not check_Direction_NESW(lstTokens):
                    raise Exception("Se esperaba dirección NESW")
                lstTokens.pop(0)
                
            elif token_type == tk.TK_NOT:
                if not lstTokens:
                    raise Exception("Se esperaba una condición después de not")
                    
                # Verificar que sigue una condición válida
                if lstTokens[0][0] not in [tk.TK_FACING, tk.TK_CANMOVE, tk.TK_CANJUMP, tk.TK_CANPUT, tk.TK_CANPICK]:
                    raise Exception("Se esperaba una condición válida después de not")
                    
                # Procesar la condición que sigue al not
                token_type = lstTokens[0][0]
                lstTokens.pop(0)
                
                if token_type == tk.TK_FACING:
                    if not lstTokens:
                        raise Exception("Se esperaba dirección NESW")
                    if not check_Direction_NESW(lstTokens):
                        raise Exception("Se esperaba dirección NESW")
                    lstTokens.pop(0)
                    
                elif token_type in [tk.TK_CANPUT, tk.TK_CANPICK]:
                    # Verificar n
                    if not lstTokens:
                        raise Exception("Se esperaba número o variable válida")
                    if lstTokens[0][0] == tk.TK_NUMERO:
                        lstTokens.pop(0)
                    elif check_ValidVariable(lstTokens, nombreProc):
                        lstTokens.pop(0)
                    else:
                        raise Exception("Se esperaba número o variable válida")
                    
                    # Verificar ofType
                    if not lstTokens:
                        raise Exception("Se esperaba ofType")
                    if lstTokens[0][0] != tk.TK_OFTYPE:
                        raise Exception("Se esperaba ofType")
                    lstTokens.pop(0)
                    
                    # Verificar tipo (balloons o chips)
                    if not lstTokens:
                        raise Exception("Se esperaba balloons o chips")
                    if lstTokens[0][0] not in [tk.TK_BALLOONS, tk.TK_CHIPS]:
                        raise Exception("Se esperaba balloons o chips")
                    lstTokens.pop(0)
                    
                elif token_type in [tk.TK_CANMOVE, tk.TK_CANJUMP]:
                    # Verificar n
                    if not lstTokens:
                        raise Exception("Se esperaba número o variable válida")
                    if lstTokens[0][0] == tk.TK_NUMERO:
                        lstTokens.pop(0)
                    elif check_ValidVariable(lstTokens, nombreProc):
                        lstTokens.pop(0)
                    else:
                        raise Exception("Se esperaba número o variable válida")
                        
                    # Verificar inDir o toThe
                    if not lstTokens:
                        raise Exception("Se esperaba inDir o toThe")
                    if lstTokens[0][0] not in [tk.TK_INDIR, tk.TK_TOTHE]:
                        raise Exception("Se esperaba inDir o toThe")
                    direction_type = lstTokens[0][0]
                    lstTokens.pop(0)
                    
                    # Verificar dirección según el tipo
                    if not lstTokens:
                        raise Exception("Se esperaba dirección")
                    if direction_type == tk.TK_INDIR:
                        if not check_Direction_NESW(lstTokens):
                            raise Exception("Se esperaba dirección NESW")
                        lstTokens.pop(0)
                    else:  # tk.TK_TOTHE
                        if not check_Direction_FBLR(lstTokens):
                            raise Exception("Se esperaba dirección FBLR")
                        lstTokens.pop(0)
            
            if not lstTokens:
                raise Exception("Falta do")
            if lstTokens[0][0] == tk.TK_DO or lstTokens[0][0] == tk.TK_NAMEPUNTOS:
                lstTokens.pop(0)
                return checkNestedBrackets(lstTokens, sublistTokens)
            else:
                raise Exception("Falta do")
        else:
            raise Exception("Se esperaba una condición válida")
    return lstTokens

def checkTK_REPEAT(lstTokens, nombreProc=""):
    sublistTokens = []
    if lstTokens and lstTokens[0][0] == tk.TK_REPEAT:
        lstTokens.pop(0)
        
        # Verificar si hay dos puntos después del repeat (opcional)
        if lstTokens and lstTokens[0][0] == tk.TK_NAMEPUNTOS:
            lstTokens.pop(0)
            
        if not lstTokens:
            raise Exception("Se esperaba número o variable válida")
            
        if lstTokens[0][0] == tk.TK_NUMERO:
            lstTokens.pop(0)
        elif check_ValidVariable(lstTokens, nombreProc):
            lstTokens.pop(0)
        else:
            raise Exception("Se esperaba número o variable válida")
            
        # Verificar punto después del número/variable
        if not lstTokens or lstTokens[0][0] != tk.TK_PUNTO:
            raise Exception("Falta punto después del número/variable")
        lstTokens.pop(0)
            
        return checkNestedBrackets(lstTokens, sublistTokens)
    return lstTokens

def checkTK_FOR(lstTokens, nombreProc=""):
    sublistTokens = []
    if lstTokens and lstTokens[0][0] == tk.TK_FOR:
        lstTokens.pop(0)
        
        # Verificar si hay dos puntos después del for (opcional)
        if lstTokens and lstTokens[0][0] == tk.TK_NAMEPUNTOS:
            lstTokens.pop(0)
            
        # Primer valor (variable de iteración)
        if not lstTokens:
            raise Exception("Se esperaba variable de iteración")
        if not check_ValidVariable(lstTokens, nombreProc):
            raise Exception("Se esperaba variable válida")
        lstTokens.pop(0)
        
        # Segundo valor (inicio)
        if not lstTokens:
            raise Exception("Se esperaba valor de inicio")
        if not (lstTokens[0][0] == tk.TK_NUMERO or check_ValidVariable(lstTokens, nombreProc)):
            raise Exception("Se esperaba número o variable válida")
        lstTokens.pop(0)
        
        # Tercer valor (fin)
        if not lstTokens:
            raise Exception("Se esperaba valor de fin")
        if not (lstTokens[0][0] == tk.TK_NUMERO or check_ValidVariable(lstTokens, nombreProc)):
            raise Exception("Se esperaba número o variable válida")
        lstTokens.pop(0)
        
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
        lstTokens.pop(0)  # quitar [
        nested_count = 1
        
        while lstTokens and nested_count > 0:
            token = lstTokens[0]
            
            if token[0] == tk.TK_CODEBLOCK_DIVLEFT:
                nested_count += 1
                sublistTokens.append(lstTokens.pop(0))
            elif token[0] == tk.TK_CODEBLOCK_DIVRIGHT:
                nested_count -= 1
                if nested_count > 0:
                    sublistTokens.append(lstTokens.pop(0))
                else:
                    lstTokens.pop(0)  # Quitar el corchete final sin agregarlo
            else:
                sublistTokens.append(lstTokens.pop(0))
        
        if nested_count > 0:
            raise Exception("Falta corchete de cierre ']'")
            
        return sublistTokens
    return lstTokens

# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◢◤◢◤◢◤
# funcs para proc calls 
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◢◤◢◤◢◤


def checkTK_PROC(lstTokens):
    sublistTokens = []
    if lstTokens and lstTokens[0][0] == tk.TK_PROC:
        lstTokens.pop(0)
        
        if not lstTokens:
            raise Exception("Se esperaba un nombre de procedimiento")
            
        # chequea si es un nombre simple o con parámetros
        if lstTokens[0][0] == tk.TK_NAME:  # caso sin parámetros
            proc_name = lstTokens[0][1]
            if proc_name in procedures:
                raise Exception(f"Procedimiento {proc_name} ya definido")
            procedures.append(proc_name)
            variables_locales[proc_name] = []  # proc sin parámetros
            lstTokens.pop(0)
            return [proc_name, checkNestedBrackets(lstTokens, sublistTokens)]
            
        elif lstTokens[0][0] == tk.TK_NAMEPUNTOS:  # caso con parámetros
            proc_name = lstTokens[0][1].rstrip(':')  # quito los : del nombre
            if proc_name in procedures:
                raise Exception(f"Procedimiento {proc_name} ya definido")
            procedures.append(proc_name)
            variables_locales[proc_name] = []  #lista de params
            lstTokens.pop(0)
            
            # procesar parametros y palabras clave hasta encontrar '['
            while lstTokens and lstTokens[0][0] != tk.TK_CODEBLOCK_DIVLEFT:
                if lstTokens[0][0] == tk.TK_NAME:
                    param_name = lstTokens[0][1]
                    # Si no es una palabra clave (como "and"), agregar como parámetro
                    if not param_name in ['and']:
                        variables_locales[proc_name].append(param_name)
                    lstTokens.pop(0)
                    
                    if lstTokens and lstTokens[0][0] == tk.TK_NAMEPUNTOS:
                        lstTokens.pop(0)
                else:
                    raise Exception("se esperaba un nombre o '['")
            
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
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◢◤◢◤◢◤
 
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
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◢◤
 
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
    
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◢◤◢◤◢◤
# funcs de auxiliares
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◢◤◢◤◢◤

#Chequea si el token es una variable valida de tipo TK_NAME
def check_ValidVariable(lstTokens, nombreProc="")->bool:
    nombreVar=lstTokens[0][1]
    
    if lstTokens[0][0]==tk.TK_NAME:
        # Variables de iteración
        if nombreVar in ['x', 'y', 'z']:
            return True
        # Variables globales
        if variables_globales.count(nombreVar)>0:
            return True
        # Variables locales
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
 

