import lexer as lx
import parser as ps

lstArchivos = ["TrueGoTo.txt"]
#, "FalseGoTo.txt","FalseGoTo2.txt", "FalseGoTo3.txt"]

for archName in lstArchivos:
    codigo = ""
    with open(archName, 'r') as fichero:
        for linea in fichero:
            codigo = codigo+linea

    lstTokens=lx.tokenize(codigo)

    correcto=ps.parserMain(lstTokens);

    if correcto:
        print(archName, True)
    else:
        print(archName, False)
