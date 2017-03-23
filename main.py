from Simulator import Simulator
import matplotlib.pyplot as plt
import numpy as np

nrGames = 1
nrPlayers = 2
nrMaxRounds = 10000

for i in range(nrGames):
    sim = Simulator(nrPlayers)
    sim.run(nrMaxRounds)

plt.plot(sim.moneytime)
plt.xlabel('rounds')
plt.ylabel('money')
plt.title('Players money over played rounds')
plt.show()