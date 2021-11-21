from typing import NamedTuple, List
from collections import OrderedDict

class AFTransition(NamedTuple):
    origin: str
    symbol: str
    destination: str

class AFState(NamedTuple):
    state: str
    transition: List[AFTransition]

class Automata(NamedTuple):
    name: str
    init: str
    final: List[str]
    program: List[AFState]
    symbols: List[str]

def getSymbols(states: List[AFState]) -> List[str]:
    symbols = []

    for state in states:
        for transition in state.transition:
            if transition.symbol not in symbols:
                symbols.append(transition.symbol)

    return symbols

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

def handleTransitions(q, afd_symbols, nfa_transitions):
    afd_transitions = {}
    afd_program = []
    for in_state in q:
        for symbol in afd_symbols:
            if len(in_state) == 1 and (in_state[0], symbol) in nfa_transitions:
                afd_transitions[(in_state, symbol)] = nfa_transitions[(in_state[0], symbol)]

                if tuple(afd_transitions[(in_state, symbol)]) not in q:
                    q.append(tuple(afd_transitions[(in_state, symbol)]))
            else:
                dest = []
                f_dest =[]

                for n_state in in_state:
                    if (n_state, symbol) in nfa_transitions and nfa_transitions[(n_state, symbol)] not in dest:
                        dest.append(nfa_transitions[(n_state, symbol)])
                
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

def handleFinalStates(q, automata):
    afd_final = []

    for q_state in q:
        for f_state in automata.final:
            if f_state in q_state:
                afd_final.append(q_state)
    
    return afd_final

def AFNConversion(automata: Automata):
    afd_symbols = getSymbols(automata.program)
    afd_init = automata.init
    
    q = []
    q.append((afd_init,))

    nfa_transitions = convertToDict(automata)
    afd_program, q = handleTransitions(q, afd_symbols, nfa_transitions)
    afd_final = handleFinalStates(q, automata)

    afd = OrderedDict()
    afd["symbols"] = afd_symbols
    afd["program"] = afd_program
    afd["init"] = afd_init
    afd["final"] = afd_final

    return afd

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

def printAutomata(automata: Automata):

    print("\nCerto! Aqui está ele:\n")
    
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