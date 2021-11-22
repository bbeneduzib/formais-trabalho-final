from typing import NamedTuple, List
from collections import OrderedDict
from itertools import product

'''
    TRABALHO FINAL
    LINGUAGENS FORMAIS E AUTÔMATOS - 2021/1

    Bernardo Beneduzi Borba
'''

#-----------------------------------------------------------------
# Objeto que guarda uma transição do autômato. 
# origin é o estado atual; 
# symbol é o símbolo lido; 
# destination é o estado destino para aquele símbolo no estado atual.
#-----------------------------------------------------------------
class AFTransition(NamedTuple):
    origin: str
    symbol: str
    destination: str

#-----------------------------------------------------------------
# Objeto que guarda um estado do autômato. 
# state é o nome do estado; 
# transition é ums lista com todas as transições daquele estado.
#-----------------------------------------------------------------
class AFState(NamedTuple):
    state: str
    transition: List[AFTransition]

#-----------------------------------------------------------------
# Objeto que guarda o autômato. 
# name é o nome do autômato; 
# init é o nome do estado inicial; 
# final é a lista com os nomes dos estados finais; 
# program é a lista com todos os estados; 
# symbols é a lista com o alfabeto da linguagem.
#-----------------------------------------------------------------
class Automata(NamedTuple):
    name: str
    init: str
    final: List[str]
    program: List[AFState]
    symbols: List[str]

#-----------------------------------------------------------------
# Dada uma lista de estados, retorna uma lista com todos os 
# simbolos presentes neles.
#-----------------------------------------------------------------
def getSymbols(states: List[AFState]) -> List[str]:
    symbols = []

    for state in states:
        for transition in state.transition:
            if transition.symbol not in symbols:
                symbols.append(transition.symbol)

    return symbols

#-----------------------------------------------------------------
# Função que lê o arquivo no formato estabelecido pelo enunciado 
# do trabalho e guarda as informações no objeto Automata
#-----------------------------------------------------------------
def readAutomata(file_path: str) -> Automata:
    with open(file_path, 'r', encoding='utf8') as automata:
        header = automata.readline().strip().split("=")
        name = header[0]

        for char in header[1]:
            if char in "(){}":
                header[1] = header[1].replace(char,'')

        states = header[1].split(",")
        init = states[0]
        states.remove(states[0])
        final = states

        program = []
        lines = automata.readlines()
        count = -1
        for line in lines:
            if ":" in line:
                transition = line.strip().split(":")
                program[count].transition.append(AFTransition(currState, transition[0], transition[1]))
            else:
                count += 1
                currState = line.strip()
                program.append(AFState(currState, []))
        
        symbols = getSymbols(program)

        # Instancia o autômato.
        return Automata(
                name=name,
                symbols=symbols,
                init=init,
                final=final,
                program=program,)

#-----------------------------------------------------------------
# Converte a função programa dos autômatos em um dicionário no 
# formato: 
# key = (estado atual, símbolo lido) 
# value = lista de estados destinos para aquele símbolo no estado atual.
#-----------------------------------------------------------------
def convertToDict(automata: Automata):
    automataDict = {}

    # {(origin, symbol): [destinations]}

    for state in automata.program:
        for transition in state.transition:
            origin = transition.origin
            symbol = transition.symbol
            destination = transition.destination
            
            if (origin, symbol) in automataDict:
                automataDict[(origin, symbol)].append(destination)
            else:
                automataDict[(origin, symbol)] = [destination]

    return automataDict

#-----------------------------------------------------------------
# Converte as transições do AFN em transições AFD. Quando um mesmo 
# símbolo possui múltiplos estados de destino, une esses estados e 
# acrescenta o estado unido na lista de estados do AFD.
#-----------------------------------------------------------------
def handleTransitions(q, afd_symbols, afn_transitions):
    afd_transitions = {}
    afd_program = []
    for in_state in q:
        for symbol in afd_symbols:
            if len(in_state) == 1 and (in_state[0], symbol) in afn_transitions:
                afd_transitions[(in_state, symbol)] = afn_transitions[(in_state[0], symbol)]

                if tuple(afd_transitions[(in_state, symbol)]) not in q:
                    q.append(tuple(afd_transitions[(in_state, symbol)]))
            else:
                dest = []
                f_dest =[]

                for n_state in in_state:
                    if (n_state, symbol) in afn_transitions and afn_transitions[(n_state, symbol)] not in dest:
                        dest.append(afn_transitions[(n_state, symbol)])
                
                if dest:
                    for d in dest:
                        for value in d:
                            if value not in f_dest:
                                f_dest.append(value)
                
                    afd_transitions[(in_state, symbol)] = f_dest 

                    if tuple(f_dest) not in q: 
                        q.append(tuple(f_dest))
    
    for key, value in afd_transitions.items():
        temp_list = [[key[0], key[1], value]]
        afd_program.extend(temp_list)

    return afd_program, q

#-----------------------------------------------------------------
# Gera os estados finais do AFD verificando quais de seus estados
# foram gerados a partir de algum estado final do AFN
#-----------------------------------------------------------------
def handleFinalStates(q, automata):
    afd_final = []

    for q_state in q:
        for f_state in automata.final:
            if f_state in q_state:
                afd_final.append(q_state)
    
    return afd_final

#-----------------------------------------------------------------
# Faz a conversão de AFN para AFD conforme o algoritmo visto em 
# aula, primeiro "replica" o estado inicial e então, gera todas 
# as combinações, sem repetições, dos estados do AFN. Por fim, 
# gera os estados finais. Retorna o AFD como um dicionário para 
# facilitar a inserção no objeto Automata.
#-----------------------------------------------------------------
def AFNConversion(automata: Automata):
    afd_symbols = getSymbols(automata.program)
    afd_init = automata.init
    
    q = []
    q.append((afd_init,))

    afn_transitions = convertToDict(automata)
    afd_program, q = handleTransitions(q, afd_symbols, afn_transitions)
    afd_final = handleFinalStates(q, automata)

    afd = OrderedDict()
    afd["symbols"] = afd_symbols
    afd["program"] = afd_program
    afd["init"] = afd_init
    afd["final"] = afd_final

    return afd

#-----------------------------------------------------------------
# Faz a inserção do automato convertido na estrutura Automata
#-----------------------------------------------------------------
def createAFD(automata: Automata):
    name = automata.name
    symbols = automata.symbols
    
    afd_dict = AFNConversion(automata)

    init = afd_dict["init"]
    
    final = []
    for finalState in afd_dict["final"]:
        final.append("".join(finalState))

    program = []
    for transition in afd_dict["program"]:
        currState = "".join(transition[0])
        origin = currState
        symbol = transition[1]
        destination = "".join(transition[2])

        found = False

        for state in program:
            if currState == state.state:
                state.transition.append(AFTransition(origin, symbol, destination))
                found = True
        
        if not found:
            program.append(AFState(currState, [AFTransition(origin, symbol, destination)]))
            found = False

    return Automata(
        name = name,
        symbols=symbols,
        init = init,
        final = final,
        program = program,
    )

#-----------------------------------------------------------------
# Printa o autômato convertido no formato estabelecido pelo 
# enunciado do trabalho
#-----------------------------------------------------------------
def printAutomata(automata: Automata):

    print("\nCerto! Aqui está ele:\n")
    
    finalStr = ""

    if len(automata.final) > 0:
        finalStr = automata.final[0]
    if len(automata.final) > 1:
        for finalState in range(1, len(automata.final)):
            finalStr += "," + automata.final[finalState]

    print(f'{automata.name}=({automata.init}, {{{finalStr}}})')
    
    for state in automata.program:
        print(state.state)
        for transition in state.transition:
            print(f'{transition.symbol}:{transition.destination}')

    print("\nLindo, não?")

    return

#-----------------------------------------------------------------
# Escreve no arquivo de saída o autômato convertido no formato 
# estabelecido pelo enunciado do trabalho
#-----------------------------------------------------------------
def writeAutomata(automata: Automata):
    finalStr = ""

    with open("saida.txt", 'w', encoding='utf8') as file:
        if len(automata.final) > 0:
            finalStr = automata.final[0]
        if len(automata.final) > 1:
            for finalState in range(1, len(automata.final)):
                finalStr += "," + automata.final[finalState]

        file.write(f'{automata.name}=({automata.init}, {{{finalStr}}})\n')
    
        for state in automata.program:
            file.write(f'{state.state}\n')
            for transition in state.transition:
                file.write(f'{transition.symbol}:{transition.destination}\n')

    return

#-----------------------------------------------------------------
# Converte a função programa para um dicionário no formato já 
# visto e percorre o autômato, guardando seu caminho e verificando 
# se a palavra inserida pertence à ACEITA ou não. Retorna um 
# booleano dizendo se aceita ou não, o caminho percorrido e a 
# mensagem de erro detalhando o motivo da palavra não ser aceita.
#-----------------------------------------------------------------
# Retorna bool (diz se foi aceita), lista de transições percorrida, mensagem de erro
def acceptWord(word: str, automata: Automata):

    currState = automata.init
    automataDict = convertToDict(automata)
    path = []

    for letter in word:
        if (currState, letter) in automataDict:
            nextState = automataDict[(currState, letter)][0]
            path.append(f"({currState}, {letter}) -> {nextState}")
            currState = nextState
        else:
            return False, path, (f'Desculpe, a palavra {word} é rejeitada por indefinição, pois não há transição para {letter} no estado {currState}!')
    
    if currState in automata.final:
        return True, path, ""
    else:
        return False, path, (f'Desculpe, a palavra {word} é rejeitada, pois para em {currState}, que não é um estado final!')

#-----------------------------------------------------------------
# Conta quantos estados há no autômato.
#-----------------------------------------------------------------
def countStates(automata: Automata):
    states = []
    for state in automata.program:
        states.append(state.state)
    
    for state in automata.final:
        if state not in states:
            states.append(state)

    return len(states)

#-----------------------------------------------------------------
# Gera todas as palavras possíveis de tamanho entre min e max-1 
# de um alfabeto. Sempre adiciona a palavra vazia.
#-----------------------------------------------------------------
def generateAllWords(symbols, min, max):
    words = [""]
    for z in range(min, max):
        for i in product(symbols, repeat=z):
            words.append(''.join(map(str, i)))
    return words

#-----------------------------------------------------------------
# Verifica se a linguagem aceita por um autômato é vazia, testando 
# todas as palavras possíveis de tamanho menor que o número de 
# estados.
#-----------------------------------------------------------------
def isEmpty(automata: Automata):
    stateCount = countStates(automata)

    allWords = generateAllWords(automata.symbols, 1, stateCount)

    for word in allWords:
        accepted, path, error = acceptWord(word, automata)
        if accepted:
            break

    return not accepted
 
#-----------------------------------------------------------------
# Verifica se a linguagem aceita por um autômato é finita, testando 
# todas as palavras possíveis de tamanho maior ou igual que o número 
# de estados e menor que o dobro do número de estados
#-----------------------------------------------------------------
def isFinite(automata: Automata):
    stateCount = countStates(automata)
    allWordsGreat = generateAllWords(automata.symbols, stateCount, 2*stateCount)
    
    if "" in allWordsGreat:
        allWordsGreat.remove("")

    for word in allWordsGreat:
        accepted, path, error = acceptWord(word, automata)
        if accepted:
            break

    return not accepted