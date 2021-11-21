from automata import Automata, acceptWord, readAutomata, createAFD, printAutomata

'''
    TRABALHO FINAL
    LINGUAGENS FORMAIS E AUTÔMATOS - 2021/1

    Bernardo Beneduzi Borba
'''

def handleFile(fileName):
    while True:
        if not ".txt" in fileName:
            fileName += ".txt"
        try:
            AFN = readAutomata(fileName)
        except:
            print("Desculpe, não consegui encontrar um arquivo com esse nome, tente novamente!")
            fileName = input("Nome do arquivo: ")
        else:
            break

    return AFN

def handleConfirmation(confirmation: str):
    if confirmation.upper() == "S":
        return True
    if confirmation.upper() == "SIM":
        return True
    return False


def testWords(automata: Automata):
    while True:
        print("\nCerto! Diga-me qual palavra você quer testar!")
        word = input("Palavra: ")
        accepted, path, error = acceptWord(word, automata)

        if accepted:
            print(f'\nParabéns a palavra {word} pertence à ACEITA do automato inserido!')
            print(f'Vou te mostrar o caminho que ele percorreu:\n{path}\n')
        else:
            print(error)
            print(f'Vou te mostrar o caminho que ele percorreu até chegar no erro:\n{path}\n')

        print("Deseja testar mais uma palavra?")
        confirmation = input("[S]im ou [N]ão? ")
        if not handleConfirmation(confirmation):
            break

    return

def console():

    print("Olá! Meu nome é Console e serei seu ajudante! Por favor, insira o nome do arquivo onde está o AFN a ser convertido!")
    fileName = input("Nome do arquivo: ")
    AFN = handleFile(fileName)

    print("\nMuito bem! Seu arquivo já está no meu sistema e estou convertendo seu AFN em um AFD!")
    AFD = createAFD(AFN)

    print("\nTudo certo! Você quer que eu te mostre seu autômato convertido?")
    confirmation = input("[S]im ou [N]ão? ")
    if handleConfirmation(confirmation):
        printAutomata(AFD)

    print("\nVocê quer que eu teste se alguma palavra pertence à ACEITA do autômato convertido?")
    confirmation = input("[S]im ou [N]ão? ")
    if handleConfirmation(confirmation):
        testWords(AFD)

    return

console()