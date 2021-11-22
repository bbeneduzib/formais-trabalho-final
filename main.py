from automata import Automata, acceptWord, isEmpty, isFinite, readAutomata, createAFD, printAutomata, writeAutomata

'''
    TRABALHO FINAL
    LINGUAGENS FORMAIS E AUTÔMATOS - 2021/1

    Bernardo Beneduzi Borba
'''

#-----------------------------------------------------------------
# Tenta abrir e ler o arquivo com o automato, se não encontrar
# o arquivo ou se houver algum erro de leitura, prende o unsuário
# até que insira um arquivo válido
#-----------------------------------------------------------------
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

#-----------------------------------------------------------------
# Verifica se o usuário digitou "s" ou "sim" e retorna verdadeiro
# para ambos os casos, falso para qualquer outra digitação
#-----------------------------------------------------------------
def handleConfirmation(confirmation: str):
    if confirmation.upper() == "S":
        return True
    if confirmation.upper() == "SIM":
        return True
    return False

#-----------------------------------------------------------------
# Coloca o usuário em um loop onde ele pode testar quantas 
# palavras quiser. Mostra o resultado dizendo se aceita ou não,
# mostrando o caminho percorrido no autômato
#-----------------------------------------------------------------
def testWords(automata: Automata):
    while True:
        print("\nCerto! Diga-me qual palavra você quer testar!")
        word = input("Palavra: ")
        accepted, path, error = acceptWord(word, automata)

        if accepted:
            print(f'\nParabéns! A palavra {word} pertence à ACEITA do automato inserido!')
            print(f'Vou te mostrar o caminho que ele percorreu:\n{path}\n')
        else:
            print(error)
            print(f'Vou te mostrar o caminho que ele percorreu até chegar no erro:\n{path}\n')

        print("Deseja testar mais uma palavra?")
        confirmation = input("[S]im ou [N]ão? ")
        if not handleConfirmation(confirmation):
            break

    return

#-----------------------------------------------------------------
# Chama as funções que verificam as propriedades do autômato e
# exibe o resultado.
#-----------------------------------------------------------------
def handleProperties(automata: Automata):
    if isEmpty(automata):
        print(f'\nA linguagem aceita pelo autômato {automata.name} é vazia! E, por consequência, finita!\n')
    else:
        print(f'\nA linguagem aceita pelo autômato {automata.name} não é vazia!\n')
        if isFinite(automata):
            print(f'A linguagem aceita pelo autômato {automata.name} é finita!')
        else:
            print(f'A linguagem aceita pelo autômato {automata.name} é infinita!')

    return

#-----------------------------------------------------------------
# Função que é rodada ao chamar o arquivo. Faz as interações 
# principais com o usuário. Pega o nome do arquivo, converte o 
# autômato inserido em AFD, escreve o arquivo de saída e printa o 
# AFD na tela, caso o usuário deseje. Chama as funções de testes de 
# palavra e de propriedades. 
#
# OBS: os testes de propriedades estão comentados, pois autômatos 
# muito complexos demoram muito para serem verificados. Para 
# realizar esses testes, descomentar.
#-----------------------------------------------------------------
def console():

    print("Olá! Meu nome é Console e serei seu ajudante! Por favor, insira o nome do arquivo onde está o AFN a ser convertido!")
    fileName = input("Nome do arquivo: ")
    AFN = handleFile(fileName)

    print(f"\nMuito bem! Seu arquivo já está no meu sistema e estou convertendo {AFN.name} de AFN para AFD!")
    AFD = createAFD(AFN)

    print(f"\nTudo certo! Você quer que eu te mostre o autômato {AFD.name} convertido? Você também pode conferí-lo no arquivo 'saida.txt'")
    confirmation = input("[S]im ou [N]ão? ")
    writeAutomata(AFD)
    if handleConfirmation(confirmation):
        printAutomata(AFD)

    print(f"\nVocê quer que eu teste se alguma palavra pertence à ACEITA({AFD.name})?")
    confirmation = input("[S]im ou [N]ão? ")
    if handleConfirmation(confirmation):
        testWords(AFD)

    # print(f"\nAgora vou verificar as propriedades de {AFD.name} quanto à linguagem vazia e finita/infinita,mas já aviso que dependendo do tramanho do autômato e do alfabeto isso pode demorar um pouco!")
    # handleProperties(AFD)

    return

# Chamada da função principal
console()

