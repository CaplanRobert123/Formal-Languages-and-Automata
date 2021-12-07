
class DFA:
    def __init__(self, alphabet, name, steps, finalStates, initialState):
        self.alphabet = alphabet
        self.name = name
        self.delta = {}
        self.initialState = int(initialState)
        self.finalStates = []
        self.currentState = self.initialState
        self.seekingState = {'seeking': False,
                             'accepted': False, 'rejected': False, 'initial': True}
        self.lastAccepted = ''
        self.currentWord = ''
        self.states = []
        self.isSinkState = False

        stariFinale = finalStates.split()
        for i in stariFinale:
            self.finalStates.append(int(i))

        for i in steps:
            step = i.split(',')
            self.delta[int(step[0]), int(step[2])] = step[1].replace("\'", '')
            if (int(step[0]) not in self.states):
                self.states.append(int(step[0]))
            if (int(step[2]) not in self.states):
                self.states.append(int(step[2]))

    def changeState(self, character, f, accepted):
        found = 0
        for key, value in self.delta.items():
            # print("key[0]: " +
            #   str(key[0]) + " key[1] " + str(key[1]) + " value " + str(value) + " character " + character + " current state " + str(self.currentState))
            # print("key[0]: " + str(type(key[0])) +
            #   " value: " + str(type(value)))
            if (key[0] == self.currentState) and (value == character):
                if (self.seekingState['initial']):
                    self.seekingState['initial'] = False
                    self.seekingState['seeking'] = True
                self.seekingState['accepted'] = False
                self.seekingState['seeking'] = True
                self.currentWord += character
                self.currentState = key[1]
                found = 1
                if(self.currentState in self.finalStates):
                    self.lastAccepted = self.currentWord
                    self.seekingState['seeking'] = False
                    self.seekingState['accepted'] = True
                    accepted[self.name] = self.lastAccepted
                # print('IM HERE ')
                break

        if(found == 0):
            # print('REJECTING because of: key[0] ' + str(key[0]) + " key[1] " + str(key[1]) + " value " + str(
            # value) + " character " + character + " current state " + str(self.currentState))
            if (not self.lastAccepted == ''):
                accepted[self.name] = self.lastAccepted
            self.seekingState['rejected'] = True
            self.seekingState['accepted'] = False
            self.seekingState['seeking'] = False
            self.isSinkState = True
            # acceptedWords.append(self.lastAccepted)
            self.lastAccepted = ''
            self.currentWord = ''
            self.currentState = self.initialState
        # print(self.name + " " + str(self.currentState))
        # print("last accepted: " + self.lastAccepted)

    def __str__(self):
        return f"Alfabetul este: {self.alphabet}\n" \
            f"Name: {self.name}\n" \
            f"Final States: {self.finalStates}\n" \
            f"Initial State: {self.initialState}\n" \
            f"Steps: {self.states}\n" \
            f"Delta: {self.delta}\n" \



class State:
    def __init__(self, initialState, finalState, currentState, lastState):
        self.initialState = initialState
        self.finalState = finalState
        self.currentState = currentState
        self.lastState = lastState


def splitByDFA(lexer):
    with open(lexer) as f:
        listOfDFAs = f.read().split("\n\n")
        f.close()
        return listOfDFAs


def createDFAs(listOfDFAs):
    DFAs = []
    for myDFA in listOfDFAs:
        lines = myDFA.splitlines()
        steps = []
        for i in range(3, len(lines) - 1):
            steps.append(lines[i])
        DFAs.append(DFA(lines[0], lines[1], steps, lines.pop(), lines[2]))
    return DFAs


def readInput(finput):
    with open(finput) as f:
        input = f.read()
        f.close()
        return input


def runlexer(lexer, finput, foutput):
    f = open(foutput, 'w')
    strings = splitByDFA(lexer)
    DFAS = createDFAs(strings)
    lastFoundIdx = 0
    accepted = {}
    input = readInput(finput)
    rejected = 0
    idx = 0
    while idx < len(input):
        # print("idx: " + str(idx))
        # print("i: " + input[idx])
        for a in DFAS:
            if (not a.seekingState['rejected']):
                if (a.seekingState['initial']):
                    a.changeState(input[idx], f, accepted)
                    if (a.seekingState['rejected']):
                        rejected += 1
                        # print(a.name + " got rejected")
                elif (a.seekingState['accepted']):
                    lastFoundIdx = idx
                    a.changeState(input[idx], f, accepted)
                    if (a.isSinkState):
                        rejected += 1
                        # print("REJECTED++ adica: " + str(rejected))
                    # print(a.name + " has accepted")
                elif (a.seekingState['seeking']):
                    if (a.currentState in a.finalStates):
                        a.seekingState['accepted'] = True
                        a.seekingState['seeking'] = False
                        a.changeState(input[idx], f, accepted)
                        if (a.isSinkState):
                            rejected += 1
                    else:
                        a.changeState(input[idx], f, accepted)
                        if (a.isSinkState):
                            rejected += 1
        idx += 1
        # print('rejected: ' + str(rejected))
        if(rejected == len(DFAS)):
            idx = lastFoundIdx
            rejected = 0
            longestMatchName = ''
            longestMatch = ''
            for key, value in accepted.items():
                if len(value) > len(longestMatch):
                    longestMatch = value
                    longestMatchName = key
            f.write(longestMatchName + " " + longestMatch + "\n")
            accepted.clear()
            for a in DFAS:
                a.seekingState['rejected'] = False
                a.seekingState['initial'] = True
                a.isSinkState = False
    for a in DFAS:
        if(not a.lastAccepted == ''):
            f.write(a.name + " " + a.lastAccepted)
    f.close()


def main():
    runlexer("/home/robert/LFA/proiect/etapa1/tests/T1/T1.4/T1.4.lex",
             "/home/robert/LFA/proiect/etapa1/tests/T1/T1.4/input/T1.4.5.in", "output.out")


if __name__ == "__main__":
    main()
