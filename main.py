from Simulator import Simulator
from DKTGame import DKTGame

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
plt.style.use('ggplot')

# Simulation only
s = Simulator(2)
s.run(10000)

# Simulation + GUI
#game = DKTGame(2)
#game.run()
