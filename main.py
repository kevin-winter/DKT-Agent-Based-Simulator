from Simulator import Simulator
from DKTGame import DKTGame

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
plt.style.use('ggplot')

nrPlayers = 2
maxRounds = 1000
gui = False

if gui:
    game = DKTGame(2)
    game.run(maxRounds)
else:
    s = Simulator(3)
    s.run(maxRounds)
