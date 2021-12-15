import sys

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



class Star(Expr):
    def __init__(self, expr):
        self.expr = expr
        self.initialState = 0
        self.finalState = expr.finalState + 1
        self.alphabet = list(expr.alphabet)
        self.states = list(expr.states)
        self.delta = dict(expr.delta)

        self.states.append(self.initialState)
        self.states.append(self.finalState)
        self.delta[self.initialState, expr.initialState] = EPS
        self.delta[expr.finalState, expr.initialState] = EPS
        self.delta[expr.finalState, self.finalState] = EPS
        self.alphabet.append(EPS)

        print(type(self.states))
# {k: increaseStates(v) for k, v in expr.delta.items()}
        # self.delta[self.states[0], self.states[1]] = EPS

        NFA(self.initialState, self.finalState,
            self.delta, self.alphabet, self.states)

    def __str__(self):
        return f"Alfabetul este: {self.alphabet}\n" \
            f"Final States: {self.finalState}\n" \
            f"Initial State: {self.initialState}\n" \
            f"States: {self.states}\n" \
            f"Delta: {self.delta}\n" \
            # f"Expr: {self.expr}\n" \


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
        expr1NewInitialState = min(expr2.states) + 1
        expr1NewFinalState = max(expr2.states) + 1

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
        self.alphabet.append(EPS)

        NFA(self.initialState, self.finalState,
            self.delta, self.alphabet, self.states)

    def __str__(self):
        return f"Alfabetul este: {self.alphabet}\n" \
            f"Final State: {self.finalState}\n" \
            f"Initial State: {self.initialState}\n" \
            f"States: {self.states}\n" \
            f"Delta: {self.delta}\n" \
            # f"Expr: {self.expr}\n" \

# TODO: CREATE CONCAT CLASS


class Concat(Expr):
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
        expr1NewInitialState = min(expr2.states) + 1
        expr1NewFinalState = max(expr2.states) + 1

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



def parseRegularExpression(regularExpression):
    operationsStack = []
    for elem in regularExpression:
        if elem == 'UNION':
            # if len(regularExpression) >= 3:
            # Union().reduceUnion()
            # varUnion = Union(Var(operationsStack.pop()),
            #  Var(operationsStack.pop()))
            # print(varUnion)
            operationsStack.append(elem)
            print('UNION')
        elif elem == 'CONCAT':
            varConcat = Concat(Var(operationsStack.pop()),
                               Var(operationsStack.pop()))
            print(varConcat)
            operationsStack.append(elem)
            print('CONCAT')
        elif elem == 'STAR':
            # starNFA = Star(Var(operationsStack.pop()))
            # operationsStack.append(elem)
            # print(starNFA)
            print()
            print(varNFA)
        else:
            varNFA = Var(elem)
            operationsStack.append(elem)
            print(varNFA)
    # print(operationsStack)


def readRegularExpression(file):
    with open(file) as f:
        regularExpression = f.read().split(" ")
        f.close()
        return regularExpression


def main():
    args = sys.argv[1:]
    foutput = args[1]
    finput = args[0]
    f = open(foutput, "w")
    # nfa = NFA()
    # regularExpression = readRegularExpression(finput)
    parseRegularExpression(regularExpression='a b CONCAT'.split())
    # nfa.parseRegularExpression(regularExpression)


if __name__ == "__main__":
    main()
