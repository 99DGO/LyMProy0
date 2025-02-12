import lexer as lx
import parser as ps

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

"""
for token in lstTokens:
    print(token)
"""