from Simulator import Simulator
import matplotlib.pyplot as plt
import numpy as np

nrGames = 1
nrPlayers = 3
nrMaxRounds = 10000

for i in range(nrGames):
    sim = Simulator(nrPlayers)
    sim.run(nrMaxRounds)


sim.plotResults()