import lexer as lx


archivo = 'code-examples.txt'
codigo = ""

with open(archivo, 'r') as fichero:
    for linea in fichero:
        codigo = codigo+linea

lstTokens=lx.tokenize(codigo)

for token in lstTokens:
    print(token)