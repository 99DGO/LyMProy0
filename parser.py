import tokens as tk
import traceback 
 
procedures=[]
variables_globales=[]
variables_locales=dict()

def parserMain(lstTokens) -> bool:
    correcta = True

    try:
        print("\n🔍 **Tokens iniciales:**", lstTokens)  # VER LOS TOKENS INICIALES
        
        if lstTokens and lstTokens[0][0] == tk.TK_VAR_DIV:
            print("📌 Encontrado bloque de variables globales")
            checkTK_VAR_DIV(lstTokens)

        while lstTokens:
            token = lstTokens[0]
            print("\n➡️ Procesando token:", token)

            if token[0] == tk.TK_PROC:
                print("📌 Encontrado procedimiento")
                procName_sublistTokens = checkTK_PROC(lstTokens)
                proc_name = procName_sublistTokens[0]
                sublistTokens = procName_sublistTokens[1]

                print(f"📂 Procedimiento: {proc_name}, Tokens restantes: {sublistTokens}")

                if sublistTokens:
                    if sublistTokens[0][0] == tk.TK_VAR_DIV:
                        checkTK_VAR_DIV(sublistTokens, proc_name)

                    while sublistTokens:
                        token = sublistTokens[0]
                        print("\n➡️ Dentro del procedimiento:", proc_name, "Procesando token:", token)

                        boolInst = opcionesInstrucciones(sublistTokens, proc_name)
                        if sublistTokens:
                            token = sublistTokens[0]
                            boolIf = opcionesIfLoopFor(sublistTokens, proc_name)

                            if token[0] == tk.TK_NAME:
                                checkTK_NAME(sublistTokens, proc_name)
                            elif not boolIf and not boolInst:
                                raise Exception(f"❌ Error en la sintaxis del procedimiento '{proc_name}'")

            elif token[0] == tk.TK_CODEBLOCK_DIVLEFT:
                print("📌 Encontrado bloque de código anidado")
                sublistTokens = checkNestedBrackets(lstTokens, [])
                
                while sublistTokens:
                    token = sublistTokens[0]
                    print("\n➡️ Procesando token dentro del bloque de código:", token)

                    boolInst = opcionesInstrucciones(sublistTokens)
                    if sublistTokens:
                        token = sublistTokens[0]
                        boolIf = opcionesIfLoopFor(sublistTokens)

                        if token[0] == tk.TK_NAME:
                            checkTK_NAME(sublistTokens)
                        elif not boolIf and not boolInst:
                            raise Exception("❌ Error en la sintaxis dentro del bloque de código")

            else:
                raise Exception("❌ Error en la estructura del código principal")
    
    except Exception as e:
        correcta = False
        print("🚨 **Error detectado:**")
        traceback.print_exc()

    return correcta


"""def parserMain(lstTokens)-> bool:
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
    """
    
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


"""def opcionesIfLoopFor(lstTokens, nombreProc=""):
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
        return True"""


def opcionesIfLoopFor(lstTokens, nombreProc=""):
    if not lstTokens:
        return lstTokens

    token = lstTokens.pop(0)  # ⚠️ Asegurar que consumimos el token

    if token[1] == "if":
        print("✅ Procesando estructura de control: if")
        
        # Verifica si hay una condición válida después de `if`
        if not lstTokens or lstTokens[0][0] not in ["facing:", "canMove:", "canPut", "canPick:", "canJump:", "not:"]:
            raise Exception("❌ Error: falta condición después de 'if'")
        
        condicion = lstTokens.pop(0)  # Consumimos la condición
        print(f"🔹 Condición detectada: {condicion}")

        # Buscar `then:`
        if not lstTokens or lstTokens[0][0] != "then:":
            raise Exception("❌ Error: falta 'then:' después de la condición en 'if'")

        lstTokens.pop(0)  # Eliminamos `then:`
        print("✅ 'then:' encontrado")

        # Procesar el bloque del if
        if not lstTokens or lstTokens[0][0] != "[":
            raise Exception("❌ Error: falta '[' para abrir el bloque del 'if'")
        
        lstTokens.pop(0)  # Eliminamos `[`

        # Recorrer el cuerpo del if
        while lstTokens and lstTokens[0][0] != "]":
            token_interno = lstTokens.pop(0)
            print(f"🔹 Procesando dentro del 'if': {token_interno}")

        if not lstTokens:
            raise Exception("❌ Error: falta ']' para cerrar el bloque del 'if'")

        lstTokens.pop(0)  # Eliminamos `]`
        print("✅ Fin de bloque 'if'")

    elif token[1] == "while":
        print("✅ Procesando estructura de control: while")
        
        # Verifica si hay una condición válida después de `while`
        if not lstTokens or lstTokens[0][0] not in ["facing:", "canMove:", "not:"]:
            raise Exception("❌ Error: falta condición después de 'while'")
        
        condicion = lstTokens.pop(0)  # Consumimos la condición
        print(f"🔹 Condición detectada: {condicion}")

        # Buscar `do:`
        if not lstTokens or lstTokens[0][0] != "do:":
            raise Exception("❌ Error: falta 'do:' después de la condición en 'while'")

        lstTokens.pop(0)  # Eliminamos `do:`
        print("✅ 'do:' encontrado")

        # Procesar el bloque del while
        if not lstTokens or lstTokens[0][0] != "[":
            raise Exception("❌ Error: falta '[' para abrir el bloque del 'while'")

        lstTokens.pop(0)  # Eliminamos `[`

        # Recorrer el cuerpo del while
        while lstTokens and lstTokens[0][0] != "]":
            token_interno = lstTokens.pop(0)
            print(f"🔹 Procesando dentro del 'while': {token_interno}")

        if not lstTokens:
            raise Exception("❌ Error: falta ']' para cerrar el bloque del 'while'")

        lstTokens.pop(0)  # Eliminamos `]`
        print("✅ Fin de bloque 'while'")

    return lstTokens  # ✅ Retorna la lista actualizada de tokens


    

# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤
# funcs para chequear tipos de nombres y números
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤

def limpiar_comentarios(lstTokens):
    """
    Elimina comentarios de la lista de tokens.
    Un comentario empieza con '#' y termina en el siguiente salto de línea.
    """
    tokens_limpios = []
    ignorar = False

    for token in lstTokens:
        if token[0] == "name" and token[1].startswith("#"):
            ignorar = True  # Comenzamos a ignorar
        elif ignorar and token[0] == "name":
            ignorar = False  # Termina el comentario

        if not ignorar:
            tokens_limpios.append(token)

    return tokens_limpios

def checkTK_NAME(lstTokens, nombreProc=""):
    if not lstTokens:
        return lstTokens

    token = lstTokens[0]  # Tomamos el primer token

    # 🔹 Ignorar comentarios correctamente
    if token[1].startswith("#"):
        print(f"🟡 Ignorando comentario desde: {token}")
        lstTokens.pop(0)  # Eliminamos el `#`
        
        # 🔹 Eliminamos solo palabras que sean parte del comentario
        while lstTokens and lstTokens[0][0] == 'name' and lstTokens[0][1] not in ["if", "while", "for", "repeat"]:
            lstTokens.pop(0)

        print("✅ Comentario eliminado correctamente")
        return lstTokens  # Continuamos con el siguiente token válido

    # 🔹 Detectar palabras clave antes de tratarlas como variables
    if token[1] in ["if", "while", "for", "repeat"]:
        print(f"🔹 Detectado estructura de control: {token[1]}")
        return opcionesIfLoopFor(lstTokens, nombreProc)

    # Si no es una palabra clave, es una variable
    print(f"🔹 Detectado identificador: {token[1]}")
    return checkTK_VAR_ASSIGN(lstTokens, nombreProc)





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
    if not lstTokens or lstTokens[0][0] != "if":
        return lstTokens

    lstTokens.pop(0)  # Quitamos `IF`

    if not lstTokens:
        raise Exception("❌ Se esperaba una condición después de 'IF'")

    token = lstTokens.pop(0)

    if token[0] not in ["facing:", "canMove:", "canJump:", "not:", "canput:", "canPick:"]:
        raise Exception("❌ Se esperaba una condición válida después de 'IF'")

    if token[0] in ["canMove:", "canput:", "canPick:"]:
        if not lstTokens:
            raise Exception("❌ Se esperaba un número o variable después de la condición")
        lstTokens.pop(0)  # Quitamos el número o variable

    if lstTokens and lstTokens[0][0] == "then:":
        lstTokens.pop(0)
        return checkNestedBrackets(lstTokens, [])
    else:
        raise Exception("❌ Falta 'THEN' en la estructura del IF")


def checkTK_WHILE(lstTokens, nombreProc=""):
    if not lstTokens or lstTokens[0][0] != "while:":
        return lstTokens

    lstTokens.pop(0)  # Quitamos `WHILE`

    if not lstTokens:
        raise Exception("❌ Se esperaba una condición después de 'WHILE'")

    token = lstTokens.pop(0)

    if token[0] not in ["facing:", "canMove:", "canJump:", "not:", "canput:", "canPick:"]:
        raise Exception("❌ Se esperaba una condición válida después de 'WHILE'")

    if token[0] in ["canMove:", "canput:", "canPick:"]:
        if not lstTokens:
            raise Exception("❌ Se esperaba un número o variable después de la condición")
        lstTokens.pop(0)

    if lstTokens and lstTokens[0][0] == "do:":
        lstTokens.pop(0)
        return checkNestedBrackets(lstTokens, [])
    else:
        raise Exception("❌ Falta 'DO' en la estructura del WHILE")



def checkTK_REPEAT(lstTokens, nombreProc=""):
    sublistTokens = []
    if lstTokens and lstTokens[0][0] == tk.TK_REPEAT:
        lstTokens.pop(0)
        
        # Verificar si hay dos puntos después del repeat (opcional)
        if lstTokens and lstTokens[0][0] == tk.TK_NAMEPUNTOS:
            lstTokens.pop(0)
            
        if not lstTokens:
            raise Exception("Se esperaba número o variable válida después del repeat")
            
        if lstTokens[0][0] == tk.TK_NUMERO:
            lstTokens.pop(0)
        elif check_ValidVariable(lstTokens, nombreProc):
            lstTokens.pop(0)
        else:
            raise Exception("Se esperaba número o variable válida")
            
        if not lstTokens:
            raise Exception("Falta el cuerpo del repeat")
            
        return checkNestedBrackets(lstTokens, sublistTokens)
    return lstTokens

def checkTK_FOR(lstTokens, nombreProc=""):
    if not lstTokens or lstTokens[0][0] != tk.TK_FOR:
        return lstTokens

    lstTokens.pop(0)  # Quitamos `FOR`

    if not lstTokens or lstTokens[0][0] != tk.TK_NAME:
        raise Exception(" Se esperaba una variable después de 'FOR'")

    lstTokens.pop(0)  # Quitamos la variable

    for _ in range(2):  # Se esperan dos valores (inicio y fin del rango)
        if not lstTokens or lstTokens[0][0] not in [tk.TK_NUMERO, tk.TK_NAME]:
            raise Exception(" Se esperaba un número o variable en el rango del 'FOR'")
        lstTokens.pop(0)

    if not lstTokens or lstTokens[0][0] != tk.TK_CODEBLOCK_DIVLEFT:
        raise Exception(" Falta el bloque de código después del 'FOR'")

    return checkNestedBrackets(lstTokens, [])


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
    print(f" Procesando corchetes: {lstTokens}")
    
    if not lstTokens or lstTokens[0][0] != "[":
        return lstTokens  # No hay bloque de código

    lstTokens.pop(0)  # Quitamos '['
    nested_count = 1

    while lstTokens and nested_count > 0:
        token = lstTokens.pop(0)

        if token[0] == "[":
            nested_count += 1
            sublistTokens.append(token)
        elif token[0] == "]":
            nested_count -= 1
            if nested_count == 0:
                break  # Cerramos el bloque correctamente
        else:
            sublistTokens.append(token)

    if nested_count > 0:
        raise Exception("❌ Falta corchete de cierre ']' en un bloque de código")

    print(f"Bloque de código procesado: {sublistTokens}")
    return sublistTokens




# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◢◤◢◤◢◤
# funcs para proc calls 
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤

def checkTK_PROC(lstTokens):
    sublistTokens = []
    if lstTokens and lstTokens[0][0] == tk.TK_PROC:
        lstTokens.pop(0)  # Quitamos "proc"

        if not lstTokens:
            raise Exception("❌ Se esperaba un nombre de procedimiento")

        # Caso con nombre y posibles parámetros
        if lstTokens[0][0] == tk.TK_NAMEPUNTOS:  # Nombre con ':'
            proc_name = lstTokens[0][1].rstrip(':')  # Quita los ':'
        elif lstTokens[0][0] == tk.TK_NAME:  # Nombre sin ':'
            proc_name = lstTokens[0][1]
        else:
            raise Exception("❌ Se esperaba un nombre de procedimiento después de 'proc'")

        lstTokens.pop(0)

        if proc_name in procedures:
            raise Exception(f"❌ Procedimiento '{proc_name}' ya definido")

        procedures.append(proc_name)
        variables_locales[proc_name] = []

        # Ahora verificamos si hay parámetros
        while lstTokens and lstTokens[0][0] == tk.TK_NAME:
            param_name = lstTokens.pop(0)[1]  # Sacamos el parámetro
            if param_name in variables_locales[proc_name]:
                raise Exception(f"❌ Parámetro '{param_name}' duplicado en '{proc_name}'")
            variables_locales[proc_name].append(param_name)

        # Verificamos que después de los parámetros haya un bloque `[`
        if not lstTokens or lstTokens[0][0] != tk.TK_CODEBLOCK_DIVLEFT:
            raise Exception(f"❌ Se esperaba '[' después de los parámetros en '{proc_name}'")

        return [proc_name, checkNestedBrackets(lstTokens, sublistTokens)]

    return lstTokens  # Si no es un procedimiento, devolver sin cambios

"""
def checkTK_VAR_ASSIGN(lstTokens, nombreProc=""):
    if lstTokens and lstTokens[0][1].startswith("#"):  # Ignorar comentarios
        print(f"🟡 Ignorando comentario en asignación: {lstTokens[0]}")
        lstTokens.pop(0)
        return lstTokens

    if lstTokens and lstTokens[0][0] == "name":
        nombre = lstTokens[0][1]
        if not (nombre in variables_globales or nombre in variables_locales.get(nombreProc, [])):
            raise Exception(f"❌ Variable {nombre} no declarada")
        lstTokens.pop(0)

        if lstTokens and lstTokens[0][0] == ":=":
            lstTokens.pop(0)
            if lstTokens and lstTokens[0][0] in ["numero", "name"]:
                lstTokens.pop(0)
                if lstTokens and lstTokens[0][0] == ".":
                    lstTokens.pop(0)
                    return lstTokens
                else:
                    raise Exception("❌ Falta punto después de la asignación")
            else:
                raise Exception("❌ Se esperaba número o nombre después de ':='")
        else:
            raise Exception("❌ Se esperaba ':=' después del nombre")
    
    return lstTokens
"""

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
    lstTokens.pop(0)  # quitar el primer |
    
    while lstTokens and lstTokens[0][0] != tk.TK_VAR_DIV:  # mientras no encuentre el | final
        if lstTokens[0][0] == tk.TK_NAME:
            varName = lstTokens[0][1]
            lstTokens.pop(0)
            if nombreProc == "":
                variables_globales.append(varName)
            else:
                variables_locales[nombreProc].append(varName)
        else:
            raise Exception("Se esperaba un nombre de variable")
    
    if lstTokens and lstTokens[0][0] == tk.TK_VAR_DIV:
        lstTokens.pop(0)  # quitar el | final
    else:
        raise Exception("Falta el | final")


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
    lstTokens.pop(0)
    if (lstTokens[0][0]==tk.TK_NUMERO) or (check_ValidVariable(lstTokens, nombreProc)):
        lstTokens.pop(0)
        
        if lstTokens[0][0]==tk.TK_TOTHE:
            lstTokens.pop(0)
            
            if check_Direction_FBLR(lstTokens):
                lstTokens.pop(0)
                # Verificar si hay dos puntos después de la dirección
                if lstTokens[0][0] == tk.TK_NAMEPUNTOS:
                    lstTokens.pop(0)
                
                if lstTokens[0][0]==tk.TK_PUNTO:
                    lstTokens.pop(0) 
                else:
                    raise Exception("token MOVE")        
            else:
                raise Exception("token MOVE")
            
        elif lstTokens[0][0]==tk.TK_INDIR:
            lstTokens.pop(0)
            
            if check_Direction_NESW(lstTokens):
                lstTokens.pop(0)
                # Verificar si hay dos puntos después de la dirección
                if lstTokens[0][0] == tk.TK_NAMEPUNTOS:
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
    lstTokens.pop(0)
    if (lstTokens[0][0]==tk.TK_NUMERO) or (check_ValidVariable(lstTokens, nombreProc)):
        lstTokens.pop(0)
        
        # Verificar si tiene inDir o toThe
        if lstTokens[0][0]==tk.TK_TOTHE:
            lstTokens.pop(0)
            
            if check_Direction_FBLR(lstTokens):
                lstTokens.pop(0)
                
                if lstTokens[0][0]==tk.TK_PUNTO:
                    lstTokens.pop(0) 
                else:
                    raise Exception("token JUMP")        
            else:
                raise Exception("token JUMP")
            
        elif lstTokens[0][0]==tk.TK_INDIR:
            lstTokens.pop(0)
            
            if check_Direction_NESW(lstTokens):
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
    
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◢◤◢◤◢◤
# funcs de auxiliares
# ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◢◤◢◤◢◤

#Chequea si el token es una variable valida de tipo TK_NAME
def check_ValidVariable(lstTokens, nombreProc="")->bool:
    if not lstTokens or lstTokens[0][0] != tk.TK_NAME:
        return False
        
    nombreVar = lstTokens[0][1]
    
    # Variables globales (x, y, z)
    if nombreVar in variables_globales:
        return True
        
    # Variables locales del procedimiento actual
    if nombreProc and nombreVar in variables_locales.get(nombreProc, []):
        return True
        
    # Variables de iteración del FOR (x, y, z)
    if nombreVar in ['x', 'y', 'z']:
        return True
        
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
 

