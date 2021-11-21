from automata import readAutomata, createAFD, printAutomata

'''
    TRABALHO FINAL
    LINGUAGENS FORMAIS E AUTÔMATOS - 2021/1

    Bernardo Beneduzi Borba
'''



AFN = readAutomata("teste.txt")

AFD = createAFD(AFN)

printAutomata(AFD)