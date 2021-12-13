import sys

EPS = 'ε'


def increaseStates(n):
    return n + 2


class Expr:
    def __init__(self, string):
        self.string = string

    def __str__(self):
        return self.string


class Var(Expr):
    def __init__(self, value):
        self.value = value
        self.initialState = 1
        self.finalState = 2
        self.alphabet = [value]
        self.states = [1, 2]
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
        self.finalState = max(expr1.finalState, expr2.finalState) + 1
        self.alphabet = list(expr1.alphabet) + list(expr2.alphabet)
        self.states = list(expr1.states) + list(expr2.states)
        self.delta = dict(list(expr1.delta.items()) +
                          list(expr2.delta.items()))

        # TODO: FIX DUPLICATE STATES, WRONG FINAL STATE, ADD TRANSITIONS 
        self.states.append(self.initialState)
        self.states.append(self.finalState)
        self.delta[self.initialState, expr1.initialState] = EPS
        self.delta[expr1.finalState, expr1.initialState] = EPS
        self.delta[expr1.finalState, self.finalState] = EPS
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


class Concat(Expr):
    def __init__(self, expr1, expr2):
        self.expr1 = None
        self.expr2 = None

    def __str__(self):
        return f"{self.expr1}{self.expr2}"


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
            varUnion = Union(Var(operationsStack.pop()),
                             Var(operationsStack.pop()))
            print(varUnion)
            operationsStack.append(elem)
            print('UNION')
        elif elem == 'CONCAT':
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
    parseRegularExpression(regularExpression='a b UNION'.split())
    # nfa.parseRegularExpression(regularExpression)


if __name__ == "__main__":
    main()
