class EditDistance:

    def __init__(self, S, T):
        self.S = S
        self.T = T
        self.tab = []

    def __genTable(self):
        self.tab = [[0 for i in range(len(self.S) + 1)]
                    for j in range(len(self.T) + 1)]

        self.S = "-" + self.S
        self.T = "-" + self.T

        for j in range(len(self.T)):

            for i in range(len(self.S)):

                choose = []

                if j > 0:
                    choose.append(self.tab[j-1][i] + 1)

                if i > 0:
                    choose.append(self.tab[j][i-1] + 1)

                if j > 0 and i > 0:
                    if self.S[i] == self.T[j]:
                        choose.append(self.tab[j-1][i-1])
                    else:
                        choose.append(self.tab[j-1][i-1] + 1)

                if len(choose) > 0:
                    self.tab[j][i] = min(choose)

    def getDistance(self):

        if len(self.tab) == 0:
            self.__genTable()

        return self.tab[-1][-1]

    def getTable(self):

        if len(self.tab) == 0:
            self.__genTable()

        return self.tab
