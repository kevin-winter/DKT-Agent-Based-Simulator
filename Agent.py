import numpy as np
from helpers import *


class Agent:

    def __init__(self, simulator, name):
        self.visits = np.zeros(40)
        self.currentPosition = 1
        self.roundsInJail = 0
        self.doubleCount = 0
        self.jailFreeCard = False
        self.money = 1500
        self.fromJail = False
        self.dead = False
        self.lastDice = 0
        self.s = simulator
        self.name = name

    def setCurrentPosition(self, field):
        self.visits[field-1] += 1
        self.currentPosition = field

    def pay(self, amount):
        self.money -= amount
        if self.money < 0:
            self.money = 0
            self.dead = True

    def move(self):
        if self.roundsInJail != 0:
            if self.jailFreeCard:
                self.jailFreeCard = False
            else:
                self.roundsInJail -= 1
                return

        dbl, eyes = rollDice()
        self.lastDice = eyes
        if dbl:
            self.doubleCount += 1
            if self.doubleCount == 3:
                self.setCurrentPosition(JAIL)
                self.doubleCount = 0
                self.roundsInJail = 2
            else:
                self.moveby(eyes)
                self.move()
        else:
            self.moveby(eyes)

        print("{} - MONEY: {}".format(self.name, self.money))

    def moveby(self, d):
        field = self.currentPosition + d
        if field > 40:
            if self.fromJail:
                self.fromJail = False
            else:
                self.money += 200
            field -= 40
        self.visit(field)

    def visit(self, field):
        self.setCurrentPosition(field)
        print("{} - Move to Field {}".format(self.name, field))

        if field in [3, 23, 38]:
            self.handleRiskCard()
        elif field in [9, 28]:
            self.handleBankCard()
        elif field == 33:
            self.money -= 80
        elif field == 11:
            self.visit(JAIL)
        elif field == 21:
            self.money -= min(350, int(self.money/10))
        elif field == 1:
            self.money += 200
        elif field == 31: True
        else:
            self.s.props[field].buyNpay(self)


    def handleRiskCard(self):
        print("{} - RISKCARD drawn".format(self.name))
        card = self.s.drawRiskCard()
        if card == 0:
            self.moveby(-4)
        elif card == 1:
            self.visit(25)
        elif card == 2:
            self.jailFreeCard = True
        elif card == 3:
            self.visit(JAIL)
        elif card == 4:
            self.moveby(7)
        elif card == 5:
            self.visit(34)
        elif card == 6:
            self.visit(22)
        elif card == 7:
            self.visit(6)
        else:
            return

    def handleBankCard(self):
        print("{} - BANKCARD drawn".format(self.name))
        card = self.s.drawBankCard()
        if card == 0:
            self.visit(1)
        elif card == 1:
            self.visit(JAIL)
        else:
            return
