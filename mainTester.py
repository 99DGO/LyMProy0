import lexer as lx
import parser as ps

#ESTE NO ES EL MAIN 
#Este fue solamente un tester que hicimos, ignorenlo porfa

carpeta="test_texts/"
lstArchivos = ["TrueInstructions2.txt"]
#, "FalseGoTo.txt","FalseGoTo2.txt", "FalseGoTo3.txt", "FalseFace.txt", "FalseMove.txt", "FalseMove2.txt", "FalsePut.txt", "FalsePut2.txt", "FalsePick.txt", "FalseMoveToThe.txt", "FalseMoveInDir.txt",
#               "FalseMoveInDir2.txt", "FalseNop.txt", "FalseVarDiv.txt", "FalseVarDiv2.txt", "FalseJumpInDir.txt", "FalseJumpToThe.txt"] 

for archName in lstArchivos:
    codigo = ""
    with open(carpeta+archName, 'r') as fichero:
        for linea in fichero:
            codigo = codigo+linea

    lstTokens=lx.tokenize(codigo)

    correcto=ps.parserMain(lstTokens);

    if correcto:
        print(archName, True)
    else:
        print(archName, False)
