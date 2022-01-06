from os import stat
import sys
import collections

EPS = 'ε'


def increaseStates(n, increaseNumber):
    return n + increaseNumber


class Expr:
    def __init__(self, string):
        self.string = string

    def __str__(self):
        return self.string


class Var(Expr):
    def __init__(self, value):
        self.value = value
        self.initialState = 0
        self.finalState = 1
        self.alphabet = [value]
        self.states = [0, 1]
        self.delta = {}

        self.delta[self.states[0], self.states[1]] = value

        NFA(self.initialState, self.finalState,
            self.delta, self.alphabet, self.states)

    def __str__(self):
        return f"Alfabetul este: {self.alphabet}\n" \
            f"Final States: {self.finalState}\n" \
            f"Initial State: {self.initialState}\n" \
            f"States: {self.states}\n" \
            f"Delta: {self.delta}\n" \
            f"Value: {self.value}\n" \



class Plus(Expr):
    def __init__(self, expr):
        self.expr = expr
        self.alphabet = list(expr.alphabet)
        self.states = []
        self.delta = {}

        for state in list(expr.states):
            state = state + 1
            self.states.append(state)
        exprNewInitialState = min(self.states)
        exprNewFinalState = max(self.states)

        for k, v in expr.delta.items():
            y = list(k)
            y[0] = y[0] + 1
            y[1] = y[1] + 1
            x = tuple(y)
            self.delta[x] = v

        self.initialState = 0
        self.states.append(self.initialState)
        self.finalState = exprNewFinalState + 1
        self.states.append(self.finalState)
        self.delta[self.initialState, exprNewInitialState] = EPS
        self.delta[exprNewFinalState, self.finalState] = EPS
        self.delta[exprNewFinalState, exprNewInitialState] = EPS
        if EPS not in self.alphabet:
            self.alphabet.append(EPS)

        NFA(self.initialState, self.finalState,
            self.delta, self.alphabet, self.states)

    def __str__(self):
        return f"Alfabetul este: {self.alphabet}\n" \
            f"Final States: {self.finalState}\n" \
            f"Initial State: {self.initialState}\n" \
            f"States: {self.states}\n" \
            f"Delta: {self.delta}\n"


class Star(Expr):
    def __init__(self, expr):
        self.expr = expr
        self.alphabet = list(expr.alphabet)
        self.states = []
        self.delta = {}

        for state in list(expr.states):
            state = state + 1
            self.states.append(state)
        exprNewInitialState = min(self.states)
        exprNewFinalState = max(self.states)

        for k, v in expr.delta.items():
            y = list(k)
            y[0] = y[0] + 1
            y[1] = y[1] + 1
            x = tuple(y)
            self.delta[x] = v

        self.initialState = 0
        self.states.append(self.initialState)
        self.finalState = exprNewFinalState + 1
        self.states.append(self.finalState)
        self.delta[self.initialState, exprNewInitialState] = EPS
        self.delta[exprNewFinalState, self.finalState] = EPS
        self.delta[exprNewFinalState, exprNewInitialState] = EPS
        self.delta[self.initialState, self.finalState] = EPS
        if EPS not in self.alphabet:
            self.alphabet.append(EPS)

        NFA(self.initialState, self.finalState,
            self.delta, self.alphabet, self.states)

    def __str__(self):
        return f"Alfabetul este: {self.alphabet}\n" \
            f"Final States: {self.finalState}\n" \
            f"Initial State: {self.initialState}\n" \
            f"States: {self.states}\n" \
            f"Delta: {self.delta}\n" \



class Union(Expr):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2
        self.initialState = 0
        self.alphabet = []
        self.states = []
        self.delta = {}

        for letter in expr1.alphabet + expr2.alphabet:
            if letter not in self.alphabet:
                self.alphabet.append(letter)

        for state in list(expr1.states):
            state = state + 1
            self.states.append(state)
        expr1NewInitialState = min(expr1.states) + 1
        expr1NewFinalState = max(expr1.states) + 1

        for state in list(expr2.states):
            state = state + expr1NewFinalState + 1
            self.states.append(state)
        expr2NewInitialState = min(expr2.states) + expr1NewFinalState + 1
        expr2NewFinalState = max(expr2.states) + expr1NewFinalState + 1

        self.finalState = expr2NewFinalState + 1

        for k, v in expr1.delta.items():
            y = list(k)
            y[0] = y[0] + 1
            y[1] = y[1] + 1
            x = tuple(y)
            self.delta[x] = v

        for k, v in expr2.delta.items():
            y = list(k)
            y[0] = y[0] + expr1NewFinalState + 1
            y[1] = y[1] + expr1NewFinalState + 1
            x = tuple(y)
            self.delta[x] = v

        self.states.append(self.initialState)
        self.states.append(self.finalState)
        self.delta[self.initialState, expr1NewInitialState] = EPS
        self.delta[self.initialState, expr2NewInitialState] = EPS
        self.delta[expr1NewFinalState, self.finalState] = EPS
        self.delta[expr2NewFinalState, self.finalState] = EPS
        if EPS not in self.alphabet:
            self.alphabet.append(EPS)

        NFA(self.initialState, self.finalState,
            self.delta, self.alphabet, self.states)

    def __str__(self):
        return f"Alfabetul este: {self.alphabet}\n" \
            f"Final State: {self.finalState}\n" \
            f"Initial State: {self.initialState}\n" \
            f"States: {self.states}\n" \
            f"Delta: {self.delta}\n" \



class Concat(Expr):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2
        self.initialState = 0
        self.alphabet = []
        self.states = list(expr1.states)
        self.delta = dict(expr1.delta)

        for letter in expr1.alphabet + expr2.alphabet:
            if letter not in self.alphabet:
                self.alphabet.append(letter)

        for state in list(expr2.states):
            state = state + expr1.finalState + 1
            self.states.append(state)
        expr2NewInitialState = min(expr2.states) + expr1.finalState + 1
        expr2NewFinalState = max(expr2.states) + expr1.finalState + 1

        self.finalState = expr2NewFinalState

        for k, v in expr2.delta.items():
            y = list(k)
            y[0] = y[0] + expr1.finalState + 1
            y[1] = y[1] + expr1.finalState + 1
            x = tuple(y)
            self.delta[x] = v

        self.delta[expr1.finalState, expr2NewInitialState] = EPS
        if EPS not in self.alphabet:
            self.alphabet.append(EPS)

        NFA(self.initialState, self.finalState,
            self.delta, self.alphabet, self.states)

    def __str__(self):
        return f"Alfabetul este: {self.alphabet}\n" \
            f"Final State: {self.finalState}\n" \
            f"Initial State: {self.initialState}\n" \
            f"States: {self.states}\n" \
            f"Delta: {self.delta}\n" \



class NFA:
    def __init__(self, initialState, finalState, delta, alphabet, states):
        self.initialState = initialState
        self.finalState = finalState
        self.delta = delta
        self.alphabet = alphabet
        self.states = states

    def __str__(self):
        return f"Alfabetul este: {self.alphabet}\n" \
            f"Final States: {self.finalState}\n" \
            f"Initial State: {self.initialState}\n" \
            f"Steps: {self.states}\n" \
            f"Delta: {self.delta}\n" \



class DFA:
    def __init__(self, alphabet, initialState, finalState, numberOfStatesNFA):
        self.alphabet = list(alphabet)
        self.delta = {}
        self.initialState = initialState
        self.DFAfinalState = finalState
        self.finalStates = []
        self.numberOfStates = 0
        self.sinkStateTransitions = []
        self.states = {}
        self.statesToAdd = []
        self.addedLetters = {}
        self.newAddedStates = []
        self.stateToBeAdded = {}
        self.transitionsToBeAdded = {}
        self.mapStates = []
        self.statesCount = 0

        if EPS in self.alphabet:
            self.alphabet.remove(EPS)
        for i in range(len(alphabet) * numberOfStatesNFA):
            self.states[i] = []

    def EPSClosureForInitialState(self, stateToLookFor, indexOfNewState, NFA):
        for k, v in NFA.delta.items():
            if k[0] == stateToLookFor:
                if v == EPS:
                    self.states[indexOfNewState].append(k[1])
                    self.EPSClosureForInitialState(k[1], indexOfNewState, NFA)

    def EPSClosure2(self, stateToLookFor, indexOfNewState, NFA):
        for k, v in NFA.delta.items():
            if k[0] == stateToLookFor:
                if v == EPS:
                    self.stateToBeAdded[indexOfNewState].append(k[1])
                    self.EPSClosure2(k[1], indexOfNewState, NFA)

    def getAlphabetForCurrentState(self, state):
        alphabetForState = []
        for transition, letter in self.delta.items():
            if transition[0] == state:
                alphabetForState.append(letter)
        return alphabetForState

    def transitionsToSinkState(self):
        sinkState = max(self.states.keys()) + 1
        for k, v in self.states.items():
            stateAlphabet = self.getAlphabetForCurrentState(k)
            for letter in self.alphabet:
                if letter not in stateAlphabet:
                    self.sinkStateTransitions.append((k, letter, sinkState))
        for letter in self.alphabet:
            self.sinkStateTransitions.append((sinkState, letter, sinkState))

    def findFinalStates(self):
        for k, v in self.states.items():
            if self.DFAfinalState in v:
                self.finalStates.append(k)

    def NFAtoDFA(self, NFA):
        currentStateToCheck = -1
        self.states[0] = []
        self.states[0].append(0)
        self.statesCount = 0

        for k, v in NFA.delta.items():
            if k[0] == NFA.initialState:
                if v is not EPS:
                    if v in self.addedLetters:
                        self.states[self.addedLetters[v]].append(k[1])
                        self.EPSClosureForInitialState(
                            k[1], self.addedLetters[v], NFA)
                    else:
                        self.statesCount = self.statesCount + 1
                        self.addedLetters[v] = self.statesCount
                        self.states[self.statesCount].append(k[1])
                        self.delta[0, self.statesCount] = v
                        self.EPSClosureForInitialState(
                            k[1], self.statesCount, NFA)
                        self.newAddedStates.append(self.statesCount)
                else:
                    self.states[0].append(k[1])
                    self.EPSClosureForInitialState(k[1], 0, NFA)

        for k, v in self.states.items():
            self.newAddedStates.clear()
            self.transitionsToBeAdded = {}
            self.mapStates = []
            statesForIfToAddCheckCounter = 0
            for iterat in range(len(self.alphabet)):
                self.stateToBeAdded[iterat] = []
            listOfNFAStates = []
            currentStateToCheck = currentStateToCheck + 1
            self.addedLetters.clear()
            for state in v:
                for kNFA, vNFA in NFA.delta.items():
                    if state == kNFA[0]:
                        if vNFA is not EPS:
                            if vNFA in self.addedLetters:
                                self.stateToBeAdded[self.addedLetters[vNFA]].append(
                                    kNFA[1])
                                self.EPSClosure2(
                                    kNFA[1], self.addedLetters[vNFA], NFA)
                            else:
                                self.statesCount = self.statesCount + 1
                                self.addedLetters[vNFA] = statesForIfToAddCheckCounter
                                self.stateToBeAdded[statesForIfToAddCheckCounter].append(
                                    kNFA[1])
                                self.mapStates.append(
                                    (statesForIfToAddCheckCounter, self.statesCount))
                                self.transitionsToBeAdded[k,
                                                          self.statesCount] = vNFA
                                self.EPSClosure2(
                                    kNFA[1], statesForIfToAddCheckCounter, NFA)
                                self.newAddedStates.append(self.statesCount)
                                statesForIfToAddCheckCounter = statesForIfToAddCheckCounter + 1
            for i in range(len(self.stateToBeAdded)):
                listOfNFAStates = self.stateToBeAdded[i]
                if listOfNFAStates in self.states.values():
                    for key, value in self.states.items():
                        if collections.Counter(listOfNFAStates) == collections.Counter(value) and value != []:
                            for maps in self.mapStates:
                                if maps[0] == i:
                                    self.delta[k,
                                               key] = self.transitionsToBeAdded[k, maps[1]]
                        if (value != []):
                            self.statesCount = key
                else:
                    for maps in self.mapStates:
                        if maps[0] == i:
                            self.states[maps[1]] = list(listOfNFAStates)
                            self.delta[k, maps[1]
                                       ] = self.transitionsToBeAdded[k, maps[1]]

        for k in list(self.states.keys()):
            if self.states[k] == []:
                del self.states[k]

        self.findFinalStates()
        self.transitionsToSinkState()

    def __str__(self):
        return f"States: {self.states}\n" \
            f"Delta: {self.delta}\n" \



def parseRegularExpression(regularExpression):
    operationsStack = []
    for elem in regularExpression:
        if elem == 'UNION':
            prevNFA1 = operationsStack.pop()
            prevNFA2 = operationsStack.pop()
            unionNFA = Union(prevNFA1, prevNFA2)
            print('UNION NFA: ' + str(unionNFA))
            operationsStack.append(unionNFA)
        elif elem == 'CONCAT':
            prevNFA1 = operationsStack.pop()
            prevNFA2 = operationsStack.pop()
            concatNFA = Concat(prevNFA1, prevNFA2)
            print('concatNFA NFA: ' + str(concatNFA))
            operationsStack.append(concatNFA)
        elif elem == 'STAR':
            prevNFA = operationsStack.pop()
            starNFA = Star(prevNFA)
            print('starNFA NFA: ' + str(starNFA))
            operationsStack.append(starNFA)
        elif elem == 'PLUS':
            prevNFA = operationsStack.pop()
            plusNFA = Plus(prevNFA)
            print('plusNFA NFA: ' + str(plusNFA))
            operationsStack.append(plusNFA)
        else:
            varNFA = Var(elem)
            print('varNFA NFA: ' + str(varNFA))
            operationsStack.append(varNFA)
    return operationsStack


def readRegularExpression(file):
    with open(file) as f:
        print(str(file))
        regularExpression = f.read().split(" ")
        print(regularExpression)
        f.close()
        return regularExpression


def main():
    args = sys.argv[1:]
    finput = args[0]
    foutput = args[1]
    regularExpression = readRegularExpression(finput)
    regularExpression.reverse()
    print(regularExpression)
    f = open(foutput, "w")
    finalNFA = parseRegularExpression(regularExpression).pop()
    print(finalNFA)
    myDFA = DFA(finalNFA.alphabet, finalNFA.initialState,
                finalNFA.finalState, len(finalNFA.states))
    myDFA.NFAtoDFA(finalNFA)
    for letter in myDFA.alphabet:
        f.write(str(letter))
    f.write("\n")
    f.write(str(len(myDFA.states) + 1) + "\n")
    f.write(str(myDFA.initialState) + "\n")
    for i in range(len(myDFA.finalStates)):
        if i == len(myDFA.finalStates) - 1:
            f.write(str(myDFA.finalStates[i]))
        else:
            f.write(str(myDFA.finalStates[i]) + " ")
    f.write("\n")
    for transition, letter in myDFA.delta.items():
        f.write(str(transition[0]) + ",\'" + letter +
                "\'," + str(transition[1]) + "\n")
    iter = 0
    for transition in myDFA.sinkStateTransitions:
        if iter == len(myDFA.sinkStateTransitions) - 1:
            f.write(str(transition[0]) + ",\'" + transition[1] +
                    "\'," + str(transition[2]))
        else:
            f.write(str(transition[0]) + ",\'" + transition[1] +
                    "\'," + str(transition[2]) + "\n")
        iter = iter + 1
    print(myDFA)
    f.close()


if __name__ == "__main__":
    main()
