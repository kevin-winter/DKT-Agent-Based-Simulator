from simulator.Simulator import Simulator
from gui.DKTGame import DKTGame
from learner.AgentLearner import AgentLearner

nrPlayers = 2
maxRounds = 1000

rf_learning = True
gui = True

if rf_learning:
    learner = AgentLearner()
    learner.trainNtest(testgui=gui, nrPlayers=nrPlayers, nrMaxRounds=maxRounds)
    exit()

if gui:
    game = DKTGame(2, maxRounds)
    game.run()
else:
    s = Simulator(3)
    s.run(maxRounds)

