import lexer as lx
import parser as ps

####Escriban aca el nombre del archivo:
archivo = 'code-examples.txt'
codigo = ""

with open(archivo, 'r') as fichero:
    for linea in fichero:
        codigo = codigo+linea

lstTokens=lx.tokenize(codigo)

correcto=ps.parserMain(lstTokens);

if correcto:
    print(True)
else:
    print(False)

