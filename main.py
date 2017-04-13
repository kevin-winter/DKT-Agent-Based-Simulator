from DKTGame import DKTGame
from Simulator import Simulator

nrPlayers = 2
maxRounds = 1000
gui = True

if gui:
    game = DKTGame(2, maxRounds)
    game.run()
else:
    s = Simulator(3)
    s.run(maxRounds)
