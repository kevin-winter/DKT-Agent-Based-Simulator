import numpy as np
PROPERTY, BUSINESS, ROUTE = 0, 1, 2


class Property:

    def __init__(self, simulator, id, rent, price, partners, type):
        self.houses = 0
        self.owner = None
        self.hotel = 0
        self.rent = rent
        self.price = price
        self.partners = partners
        self.s = simulator
        self.id = id
        self.type = type

    def canBuildHouse(self, money):
        return self.type == PROPERTY \
               and np.all([self.owner == self.s.props[p].owner for p in self.partners]) \
               and np.all([self.houses <= self.s.props[p].houses for p in self.partners]) \
               and self.houses < 4 \
               and money >= self.price[1]

    def canBuildHotel(self, money):
        return self.type == PROPERTY \
               and np.all([self.owner == self.s.props[p].owner for p in self.partners]) \
               and np.all([4 == self.s.props[p].houses for p in self.partners]) \
               and self.houses == 4 \
               and self.hotel == 0 \
               and money >= self.price[2]

    def canBuyProperty(self, money):
        return money >= self.price[0]

    def buyNpay(self, agent):
        old = agent.getReward(0)
        if self.owner is None:
            if self.canBuyProperty(agent.money) and agent.wantToBuy(self, self.price[0]):
                agent.pay(self.price[0])
                self.owner = agent
                if self.s.verbose: print("{} - Buy Property {}".format(agent.name, self.id))
                if agent.learner != None: agent.learner.react(agent.getReward(old))
        elif self.owner == agent:
            if self.canBuildHouse(agent.money) and agent.wantToBuy(self, self.price[1]):
                agent.pay(self.price[1])
                self.houses += 1
                if self.s.verbose: print("{} - Buy House at {}".format(agent.name, self.id))
                if agent.learner != None: agent.learner.react(agent.getReward(old))
            elif self.canBuildHotel(agent.money) and agent.wantToBuy(self, self.price[2]):
                agent.pay(self.price[2])
                self.hotel = 1
                if self.s.verbose: print("{} - Buy Hotel at {}".format(agent.name, self.id))
                if agent.learner != None: agent.learner.react(agent.getReward(old))
        else:
            self.payRent(agent)

    def sellTop(self, agent):
        if self.owner == agent:
            if self.hotel == 1:
                self.hotel = 0
                agent.money += int(self.price[2] / 2)
                if self.s.verbose: print("{} - Sell Hotel at {}".format(agent.name, self.id))

            elif self.houses > 0:
                self.houses -= 1
                agent.money += int(self.price[1] / 2)
                if self.s.verbose: print("{} - Sell House at {}".format(agent.name, self.id))

            else:
                self.owner = None
                agent.money += int(self.price[0] / 2)
                if self.s.verbose: print("{} - Sell Property {}".format(agent.name, self.id))

    def payRent(self, agent):
        if self.hotel == 1:
            payed = self.rent[5]
            agent.pay(payed)
            self.owner.money += payed
        else:
            if self.type != PROPERTY:
                nrLines = sum([self.s.props[x].owner == self.owner for x in self.partners])
                if self.type == BUSINESS:
                    payed = agent.lastDice * self.rent[nrLines - 1]
                elif self.type == ROUTE:
                    payed = self.rent[nrLines - 1]
            else:
                payed = self.rent[self.houses]

            agent.pay(payed)
            self.owner.money += payed

        if self.s.verbose: print("{} - Pay {} Rent to {} for Property {}".format(agent.name, payed, self.owner.name, self.id))

    def valueForPlayer(self, agent):
        sumMine = sum([self.s.props[p].owner == agent for p in self.partners])
        sumNone = sum([self.s.props[p].owner is None for p in self.partners])
        sumOthers = sum([self.s.props[p].owner is not None and self.s.props[p].owner != agent for p in self.partners])
        return sumMine * 2 + sumNone - sumOthers * 2
