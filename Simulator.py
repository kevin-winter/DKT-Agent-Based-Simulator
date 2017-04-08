import numpy as np
import matplotlib.pyplot as plt
from Agent import Agent
from Property import Property


class Simulator:

    def __init__(self, nrPlayers):
        self.players = []
        self.moneytime = []
        self.networthtime = []
        self.visits = []

        self.riskCards = self.getDeck()
        self.bankCards = self.getDeck()
        self.initProperties()

        for i in range(nrPlayers):
            a = Agent(self, "Player{}".format(i))
            self.players.append(a)

    def getDeck(self):
        d = np.arange(16)
        np.random.shuffle(d)
        return d

    def drawBankCard(self):
        if len(self.bankCards) == 0:
            self.bankCards = self.getDeck()
        card = self.bankCards[0]
        self.bankCards = np.delete(self.bankCards, 0)
        return card

    def drawRiskCard(self):
        if len(self.riskCards) == 0:
            self.riskCards = self.getDeck()
        card = self.riskCards[0]
        self.riskCards = np.delete(self.riskCards, 0)
        return card

    def run(self,rounds=10000):
        for i in range(rounds):
            self.currentRound = i
            done = self.runOneRound()
            if done: break

        fig = self.plotStats()
        plt.show()
        return

    def runOneRound(self):
        for p in self.players:
            if not p.dead:
                p.move()

        self.sumUpStats()

        if sum([not p.dead for p in self.players]) <= 1 and len(self.players) != 1:
            return 1

    def sumUpStats(self):
        self.visits = np.sum([p.visits for p in self.players], axis=0)
        self.moneytime.append([p.money for p in self.players])
        self.networthtime.append([p.netWorth() for p in self.players])

    def initProperties(self):
        self.props = {
            2: Property(self, 2, [20, 100, 300, 600, 750, 950], [220, 160, 160], [39, 40], 0),
            4: Property(self, 4, [5, 10, 20], [160], [14, 34], 1),
            5: Property(self, 5, [30, 150, 450, 850, 1050, 1200], [300, 200, 200], [6, 7], 0),
            6: Property(self, 6, [24, 110, 330, 700, 900, 1050], [250, 150, 140], [5, 7], 0),
            7: Property(self, 7, [20, 100, 300, 600, 750, 950], [220, 130, 130], [5, 6], 0),
            8: Property(self, 8, [20, 40, 80, 160], [160], [13, 18, 24], 2),
            10: Property(self, 10, [6, 30, 90, 260, 380, 550], [100, 50, 50], [12], 0),
            12: Property(self, 12, [20, 100, 300, 600, 750, 950], [220, 160, 160], [10], 0),
            13: Property(self, 13, [20, 40, 80, 160], [160], [8, 18, 24], 2),
            14: Property(self, 14, [5, 10, 20], [160], [4, 34], 1),
            15: Property(self, 15, [50, 200, 600, 1300, 1600, 1950], [380, 220, 220], [16, 17], 0),
            16: Property(self, 16, [40, 170, 500, 1000, 1300, 1600], [350, 220, 220], [15, 17], 0),
            17: Property(self, 17, [24, 110, 330, 700, 900, 1050], [250, 150, 140], [15, 16], 0),
            18: Property(self, 18, [20, 40, 80, 160], [160], [8, 13, 24], 2),
            19: Property(self, 19, [30, 150, 450, 850, 1050, 1200], [300, 200, 200], [20, 22], 0),
            20: Property(self, 20, [14, 70, 210, 500, 700, 850], [180, 100, 100], [19, 22], 0),
            22: Property(self, 22, [20, 100, 300, 600, 750, 950], [220, 160, 160], [19, 20], 0),
            24: Property(self, 24, [20, 40, 80, 160], [160], [8, 13, 18], 2),
            25: Property(self, 25, [24, 110, 330, 700, 900, 1050], [250, 150, 140], [26, 27], 0),
            26: Property(self, 26, [22, 100, 320, 680, 850, 1000], [240, 140, 130], [25, 27], 0),
            27: Property(self, 27, [24, 110, 330, 700, 900, 1050], [250, 150, 140], [25, 26], 0),
            29: Property(self, 29, [10, 50, 150, 450, 600, 730], [140, 100, 100], [30, 32], 0),
            30: Property(self, 30, [16, 80, 230, 550, 710, 900], [200, 110, 110], [29, 32], 0),
            32: Property(self, 32, [18, 90, 250, 600, 730, 930], [210, 120, 150], [29, 30], 0),
            34: Property(self, 34, [5, 10, 20], [160], [4, 34], 1),
            35: Property(self, 35, [30, 150, 450, 850, 1050, 1200], [300, 200, 200], [36, 37], 0),
            36: Property(self, 36, [24, 110, 330, 700, 900, 1050], [250, 150, 140], [35, 37], 0),
            37: Property(self, 37, [30, 150, 450, 850, 1050, 1200], [300, 200, 200], [35, 36], 0),
            39: Property(self, 39, [8, 40, 100, 300, 450, 600], [120, 50, 50], [2, 40], 0),
            40: Property(self, 40, [14, 70, 210, 500, 700, 850], [180, 100, 100], [2, 39], 0)
        }

    def plotStats(self):
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, facecolor='white')
        fig.suptitle("Game Results", size=16)

        ax0.set_title('Players net worth over played rounds')
        ax0.set_xlabel('rounds')
        ax0.set_ylabel('net worth')
        ax0.plot(self.networthtime)

        ax1.set_title('Players money over played rounds')
        ax1.set_xlabel('rounds')
        ax1.set_ylabel('money')
        ax1.plot(self.moneytime)

        ax2.set_title("Fields visited")
        ax2.set_xlabel('fields')
        ax2.set_ylabel('probability')
        ax2.bar(np.arange(40), self.visits/sum(self.visits))

        fig.tight_layout()
        fig.subplots_adjust(top=0.88)

        return fig

    def updatePlot(self):
        self.fig[1][0].plot(self.networthtime)
        self.fig[1][1].plot(self.moneytime)
        self.fig[1][2].bar(np.arange(40), self.visits/sum(self.visits))
        return self.fig[0]

    def playerData(self):
        data = []
        for p in self.players:
            data.append(p.summary())

        return np.asmatrix(data).T
