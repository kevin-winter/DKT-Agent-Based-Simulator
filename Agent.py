from Property import Property
import numpy as np
from game_constants import *


class Agent:
    JAIL = 31

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
        self.control = np.random.choice([RANDOM, AUTO])
        self.learner = None

    def printSummary(self):
        return SUMMARY_FORMAT.format(*self.summary())

    def summary(self):
        return self.name, self.money, self.netWorth(), self.rentWorth(), self.lastDice, "DEAD" if self.dead else ""

    def setCurrentPosition(self, field):
        self.visits[field-1] += 1
        self.currentPosition = field

    def pay(self, amount):
        if self.s.verbose: print("{} - Pay {}".format(self.name, amount))
        self.money -= amount
        if self.money < 0:
            self.sell()

    def sell(self, pid=-1):
        if pid in self.s.props:
            if self.s.props[pid].owner == self:
                self.s.props[pid].sellTop(self)
        else:
            p = self.selectInvaluableProperty()
            if p:
                p.sellTop(self)
            else:
                self.dead = True
                return
        if self.money < 0:
            self.sell()

    def selectInvaluableProperty(self):
        ownProps = [p for p in self.s.props.values() if p.owner == self]
        if len(ownProps) == 0:
            return None
        ownValues = {p: p.valueForPlayer(self) for p in ownProps}
        return min(ownValues, key=ownValues.get)

    def netWorth(self):
        sum = self.money
        ownProps = [p for p in self.s.props.values() if p.owner == self]
        for p in ownProps:
            if p.type == 0:
                sum += p.price[0] + p.price[1] * p.houses + p.price[2] * p.hotel
            else:
                sum += p.price[0]
        return sum

    def rentWorth(self):
        rentsum = 0
        ownProps = [p for p in self.s.props.values() if p.owner == self]
        for p in ownProps:
            if p.hotel == 1:
                payed = p.rent[5]
            else:
                if p.type != 0:
                    nrLines = sum([self.s.props[x].owner == p.owner for x in p.partners])
                    if p.type == 1:
                        payed = 6 * p.rent[nrLines - 1]
                    elif p.type == 2:
                        payed = p.rent[nrLines - 1]
                else:
                    payed = p.rent[p.houses]

            rentsum += payed
        return rentsum

    def rollDice(self):
        rolls = np.random.randint(1,6,2)
        return rolls[0] == rolls[1], sum(rolls)


    def move(self):
        if self.roundsInJail != 0:
            if self.jailFreeCard:
                self.jailFreeCard = False
            else:
                self.roundsInJail -= 1
                return

        dbl, eyes = self.rollDice()
        self.lastDice = eyes
        if dbl:
            self.doubleCount += 1
            if self.doubleCount == 3:
                self.setCurrentPosition(self.JAIL)
                self.doubleCount = 0
                self.roundsInJail = 2
            else:
                self.moveby(eyes)
                self.move()
        else:
            self.moveby(eyes)

        if self.s.verbose: print("{} - MONEY: {}".format(self.name, self.money))

    def moveby(self, d):
        field = self.currentPosition + d
        if field > 40:
            if self.fromJail:
                self.fromJail = False
            else:
                self.money += 200
            field -= 40
        elif field < 1:
            field += 40
        self.visit(field)

    def visit(self, field):
        self.setCurrentPosition(field)
        if self.s.verbose: print("{} - Move to Field {}".format(self.name, field))

        if field in [3, 23, 38]:
            self.handleRiskCard()
        elif field in [9, 28]:
            self.handleBankCard()
        elif field == 33:
            self.money -= 80
        elif field == 11:
            self.visit(self.JAIL)
        elif field == 21:
            self.money -= min(350, int(self.money/10))
        elif field == 1:
            self.money += 200
        elif field == 31: True
        else:
            self.s.props[field].buyNpay(self)

    def wantToBuy(self, p, price):
        if self.control == AUTO:
            return True
        elif self.control == AI:
            return self.learner.decide(self.getObservations(p, price))
        elif self.control == MANUAL:
            while True:
                try:
                    q = "{}: Do you want to buy Property {} for {}$ from {}"\
                        .format(self.name, p.id, price, "the bank" if p.owner is None else p.owner.name)
                    return {"y":True, "n":False}[input(q).lower()]
                except KeyError:
                    print("Invalid input, please enter y or n!")
        elif self.control == RANDOM:
            return np.random.choice([True, False])

    def getReward(self, old):
        return self.netWorth() / sum([p.netWorth() for p in self.s.players]) \
        + (len(self.s.players) * (self.rentWorth()+1)) / sum([(p.rentWorth()+1) * len(self.s.players) for p in self.s.players]) - old

    def getObservations(self, p=None, price=None):
        ownerships = np.array([np.mean([[self.s.props[p].owner == self,
                   self.s.props[p].owner not in (None, self),
                   np.max([self.s.props[p].owner == i for i in self.s.players if i != self])]
                  for p in gr], axis=0) for gr in self.s.groups])

        finance = np.array([self.money / sum([p.money for p in self.s.players]),
                  self.netWorth() / sum([p.netWorth() for p in self.s.players])])

        if p is None:
            saleInfo = np.array([0, 1, 1])
        else:
            saleInfo = np.array([price / self.money, price / p.price[0],
                                 [p.id in a for a in self.s.groups].index(True) / 12])

        observations = np.concatenate((ownerships.flatten(), finance, saleInfo))
        return observations

    def handleRiskCard(self):
        card = self.s.drawRiskCard()
        if self.s.verbose: print("{} - Risk Card {} drawn".format(self.name, card))
        if card == 0:
            self.moveby(-4)
        elif card == 1:
            if self.currentPosition > 25:
                self.money += 200
            self.visit(25)
        elif card == 2:
            self.jailFreeCard = True
        elif card == 3:
            self.visit(self.JAIL)
        elif card == 4:
            self.moveby(7)
        elif card == 5:
            if self.currentPosition > 34:
                self.money += 200
            self.visit(34)
        elif card == 6:
            if self.currentPosition > 22:
                self.money += 200
            self.visit(22)
        elif card == 7:
            if self.currentPosition > 6:
                self.money += 200
            self.visit(6)
        elif card == 8:
            self.money += 140
        elif card == 9:
            self.money += 60
        elif card == 10:
            self.pay(140)
        elif card == 11:
            self.pay(10)
        elif card == 12:
            self.pay(5)
        elif card == 13:
            self.pay(20)
        elif card == 14:
            totalcost = 0
            for p in self.s.props:
                if Property.__instancecheck__(p) and p.owner == self:
                    totalcost += p.price[0]
            self.pay(int(totalcost / 10))
        elif card == 15:
            totalcost = 0
            for p in self.s.props.values():
                if Property.__instancecheck__(p) and p.owner == self:
                    if p.hotel == 1:
                        totalcost += 80
                    else:
                        totalcost += p.houses * 20
            self.pay(totalcost)
        else:
            return

    def handleBankCard(self):
        card = self.s.drawBankCard()
        if self.s.verbose: print("{} - Bank Card {} drawn".format(self.name, card))
        if card == 0:
            self.visit(1)
        elif card == 1:
            self.visit(self.JAIL)
        elif card == 2:
            self.money += 20
        elif card == 3:
            self.money += 180
        elif card == 4:
            self.money += 25
        elif card == 5:
            self.money += 120
        elif card == 6:
            self.money += 40
        elif card == 7:
            self.money += 35
        elif card == 8:
            self.money += 50
        elif card == 9:
            self.money += 20
        elif card == 10:
            self.pay(48)
        elif card == 11:
            self.pay(130)
        elif card == 12:
            self.pay(50)
        elif card == 13:
            self.pay(15)
        elif card == 14:
            self.pay(40)
        elif card == 15:
            self.pay(120)
        else:
            return
