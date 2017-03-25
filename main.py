from Simulator import Simulator
from DKTGame import DKTGame

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
plt.style.use('ggplot')

# Simulation only
s = Simulator(3)
s.run()

# Simulation + GUI
#game = DKTGame(3)
#game.run()
