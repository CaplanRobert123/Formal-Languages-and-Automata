def splitByDFA():
    with open("/home/robert/LFA/proiect/etapa1/T1/T1.1/T1.1.lex") as f:
        listOfDFAs = []
        # lines = f.read().splitlines()
        DFA = f.read().split("\n\n")
        listOfDFAs.append(DFA)
        f.close()
        for test in listOfDFAs:
            print(test)
        # print(DFA)
        return listOfDFAs


class DFA:
    def __init__(self, lines):
        self.alphabet = []
        self.delta = {}
        # self.finalStates =
        # self.initialState =

        self.steps = []
        # for i in range(1, len(lines)):
        #     step = lines[i].strip()
        #     state = step[2]
        #     self.steps.append(step)
        #     if state not in self.alphabet:
        #         self.alphabet.append(state)

        # for i in self.steps:
        # self.delta[(int(i[0]), i[2])] = int(i[4])

    # def __str__(self):
    # return f"Alfabetul este: {self.alphabet}\n" \
    #    f"Steps: {self.steps}\n" \
    #    f"Functia delta este din starea: {self.delta}\n"
    #    f"Starea initiala este: {self.initialState}\n" \
    #    f"Starile finale sunt: {self.finalStates}\n" \


class State:
    def a(self):
        return 0


strings = splitByDFA()
# print(strings[0])
# dfa = DFA(strings)
# print(dfa)
# print(strings[4])
