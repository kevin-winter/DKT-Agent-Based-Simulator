import numpy as np
import matplotlib.pyplot as plt
from helpers import *
from Agent import Agent
from Property import Property

class Simulator:

    def __init__(self, nrPlayers):
        self.riskCards = getDeck()
        self.bankCards = getDeck()
        self.players = []
        self.initProperties()
        self.moneytime = []
        for i in range(nrPlayers):
            a = Agent(self, "Player{}".format(i))
            self.players.append(a)

    def drawBankCard(self):
        if len(self.bankCards) == 0:
            self.bankCards = getDeck()
        card = self.bankCards[0]
        self.bankCards = np.delete(self.bankCards, 0)
        return card

    def drawRiskCard(self):
        if len(self.riskCards) == 0:
            self.riskCards = getDeck()
        card = self.riskCards[0]
        self.riskCards = np.delete(self.riskCards, 0)
        return card

    def run(self,rounds):
        for i in range(rounds):
            for p in self.players:
                if not p.dead:
                    p.move()

            self.moneytime.append([p.money for p in self.players])
            if sum([not p.dead for p in self.players]) <= 1:
                break

        self.sumUpVisits()
        return

    def sumUpVisits(self):
        results = np.zeros(40)
        for p in self.players:
            results += p.visits
        self.visits = results

    def initProperties(self):
        self.props = {
            2: Property(self, 2, [20, 100, 300, 600, 750, 950], [220, 160, 160], [39, 40]),
            4: Business(self, 4),
            5: Property(self, 5, [30, 150, 450, 850, 1050, 1200], [300, 200, 200], [6, 7]),
            6: Property(self, 6, [24, 110, 330, 700, 900, 1050], [250, 150, 140], [5, 7]),
            7: Property(self, 7, [20, 100, 300, 600, 750, 950], [220, 130, 130], [6, 7]),
            8: Route(self, 8),
            10: Property(self, 10, [6, 30, 90, 260, 380, 550], [100, 50, 50], [12]),
            12: Property(self, 12, [20, 100, 300, 600, 750, 950], [220, 160, 160], [10]),
            13: Route(self, 13),
            14: Business(self, 14),
            15: Property(self, 15, [50, 200, 600, 1300, 1600, 1950], [380, 220, 220], [16, 17]),
            16: Property(self, 16, [40, 170, 500, 1000, 1300, 1600], [350, 220, 220], [15, 17]),
            17: Property(self, 17, [24, 110, 330, 700, 900, 1050], [250, 150, 140], [15, 16]),
            18: Route(self, 18),
            19: Property(self, 19, [30, 150, 450, 850, 1050, 1200], [300, 200, 200], [20, 22]),
            20: Property(self, 20, [14, 70, 210, 500, 700, 850], [180, 100, 100], [19, 22]),
            22: Property(self, 22, [20, 100, 300, 600, 750, 950], [220, 160, 160], [19, 20]),
            24: Route(self, 24),
            25: Property(self, 25, [24, 110, 330, 700, 900, 1050], [250, 150, 140], [26, 27]),
            26: Property(self, 26, [22, 100, 320, 680, 850, 1000], [240, 140, 130], [25, 27]),
            27: Property(self, 27, [24, 110, 330, 700, 900, 1050], [250, 150, 140], [25, 26]),
            29: Property(self, 29, [10, 50, 150, 450, 600, 730], [140, 100, 100], [30, 32]),
            30: Property(self, 30, [16, 80, 230, 550, 710, 900], [200, 110, 110], [29, 32]),
            32: Property(self, 32, [18, 90, 250, 600, 730, 930], [210, 120, 150], [29, 30]),
            34: Business(self, 34),
            35: Property(self, 35, [30, 150, 450, 850, 1050, 1200], [300, 200, 200], [36, 37]),
            36: Property(self, 36, [24, 110, 330, 700, 900, 1050], [250, 150, 140], [35, 37]),
            37: Property(self, 37, [30, 150, 450, 850, 1050, 1200], [300, 200, 200], [35, 36]),
            39: Property(self, 39, [8, 40, 100, 300, 450, 600], [120, 50, 50], [40]),
            40: Property(self, 40, [14, 70, 210, 500, 700, 850], [180, 100, 100], [39])
        }

    def plotResults(self):
        fig, (ax1, ax2) = plt.subplots(nrows=2)
        fig.suptitle("Game Results", size=16)

        ax1.plot(self.moneytime)
        ax1.set_title('Players money over played rounds')
        ax1.set_xlabel('rounds')
        ax1.set_ylabel('money')

        ax2.bar(np.arange(40), self.visits/sum(self.visits))
        ax2.set_title("Fields visited")
        ax2.set_xlabel('fields')
        ax2.set_ylabel('probability')

        fig.tight_layout()
        fig.subplots_adjust(top=0.88)
        plt.show()