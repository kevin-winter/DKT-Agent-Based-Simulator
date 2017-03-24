import numpy as np

class Property:

    def __init__(self, simulator, id, rent, price, partners):
        self.houses = 0
        self.owner = None
        self.hotel = 0
        self.rent = rent
        self.price = price
        self.partners = partners
        self.s = simulator
        self.id = id

    def canBuildHouse(self, money):
        return np.all([self.owner == self.s.props[p].owner for p in self.partners]) \
               and np.all([self.houses <= self.s.props[p].houses for p in self.partners]) \
               and self.houses < 4 \
               and money >= self.price[1]

    def canBuildHotel(self, money):
        return np.all([self.owner == self.s.props[p].owner for p in self.partners]) \
               and np.all([4 == self.s.props[p].houses for p in self.partners]) \
               and self.houses == 4 \
               and self.hotel == 0 \
               and money >= self.price[2]

    def canBuyProperty(self, money):
        return money >= self.price[0]

    def buyNpay(self, agent):
        if self.owner is None:
            if self.canBuyProperty(agent.money):
                agent.pay(self.price[0])
                self.owner = agent
                print("{} - Buy Property {}".format(agent.name, self.id))
        elif self.owner == agent:
            if self.canBuildHouse(agent.money):
                agent.pay(self.price[1])
                self.houses += 1
                print("{} - Buy House at {}".format(agent.name, self.id))
            elif self.canBuildHotel(agent.money):
                agent.pay(self.price[2])
                self.hotel = 1
                print("{} - Buy Hotel at {}".format(agent.name, self.id))
        else:
            self.payRent(agent)

    def sellTop(self, agent):
        if self.owner == agent:
            if self.hotel == 1:
                self.hotel = 0
                agent.money += int(self.price[2] / 2)
                print("{} - Sell Hotel at {}".format(agent.name, self.id))

            elif self.houses > 0:
                self.houses -= 1
                agent.money += int(self.price[1] / 2)
                print("{} - Sell House at {}".format(agent.name, self.id))

            else:
                self.owner = None
                agent.money += int(self.price[0] / 2)
                print("{} - Sell Property {}".format(agent.name, self.id))

    def payRent(self, agent):
        if self.hotel == 1:
            payed = self.rent[5]
            agent.pay(payed)
            self.owner.money += payed
        else:
            payed = self.rent[self.houses]
            agent.pay(payed)
            self.owner.money += payed
        print("{} - Pay {} Rent to {} for Property {}".format(agent.name, payed, self.owner.name, self.id))

    def valueForPlayer(self, agent):
        sumMine = sum([self.s.props[p].owner == agent for p in self.partners])
        sumNone = sum([self.s.props[p].owner is None for p in self.partners])
        sumOthers = sum([self.s.props[p].owner is not None and self.s.props[p].owner != agent for p in self.partners])
        return sumMine * 2 + sumNone - sumOthers * 2
