from helpers import *

class Business:
    rent = [5, 10, 20]
    partners = [4, 14, 34]

    def __init__(self, simulator, id):
        self.owner = None
        self.s = simulator
        self.id = id

    def canBuy(self, money):
        return money >= 160

    def buyNpay(self, agent):
        if self.owner is None and self.canBuy(agent.money):
            agent.pay(160)
            self.owner = agent
            print("{} - Buy Business {}".format(agent.name, self.id))
        elif self.owner is not None and self.owner != agent:
            self.payRent(agent)

    def payRent(self, agent):
        global props
        nrLines = sum([self.s.props[x].owner == self.owner for x in self.partners]) - 1
        payed = agent.lastDice * self.rent[nrLines]
        agent.pay(payed)
        self.owner.money += payed
        print("{} - Pay {} Rent to {} for Business {}".format(agent.name, payed, self.owner.name, self.id))

    def valueForPlayer(self, agent):
        sumMine = sum([self.s.props[p].owner == agent for p in self.partners])
        sumNone = sum([self.s.props[p].owner is None for p in self.partners])
        sumOthers = sum([self.s.props[p].owner is not None and self.s.props[p].owner != agent for p in self.partners])
        return sumMine * 2 + sumNone - sumOthers * 2

    def sellTop(self, agent):
        if self.owner == agent:
            self.owner = None
            agent.money += 80