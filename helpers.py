import numpy as np
from Property import Property
from Business import Business
from Route import Route

JAIL = 31


def rollDice():
    rolls = np.random.randint(1,6,2)
    return rolls[0] == rolls[1], sum(rolls)


def getDeck():
    d = np.arange(16)
    np.random.shuffle(d)
    return d


