import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import matplotlib.backends.backend_agg as agg

from pygame.locals import *
from time import sleep
import sys

from gui.game_constants import *
from simulator.simulation_constants import *
from simulator.Simulator import Simulator
from simulator.Property import Property


class DKTGame:

    def __init__(self, nrPlayers=3, nrMaxRounds=10000):
        pygame.init()

        self.playerCols = {}
        self.nrPlayers = nrPlayers
        self.nrMaxRounds = nrMaxRounds
        self.s = Simulator(self.nrPlayers, verbose=False)
        self.BOARD = self.initBoard()

    def initBoard(self):
        DISPLAYSURF = pygame.display.set_mode(BOARD_SIZE,HWSURFACE|DOUBLEBUF|RESIZABLE)
        pygame.display.set_caption('DKT Simulator')
        for i, p in enumerate(self.s.players):
            self.playerCols[p] = COLS[i]
        return DISPLAYSURF

    def updateBoard(self):
        self.BOARD.fill(WHITE)
        self.BOARD.blit(BOARD_BG, (0, 0))
        self.printStats()
        self.drawProperties()
        for i, p in enumerate(self.s.players):
            pygame.draw.circle(self.BOARD, self.playerCols[p], offset(playerLocs[p.currentPosition], scale((5*i, 5*1))), s(20), 0)

    def printStats(self):
        pos = (1020, 20)
        myfont = pygame.font.SysFont("Courier New", int(20*SCALE))
        header = myfont.render(SUMMARY_FORMAT.format("Name", "Cash", "Assets", "Rent", "Dice", "Dead"), 1, BLACK)
        line = myfont.render("{:-^43}".format(""), 1, BLACK)
        self.BOARD.blit(header, scale(pos))
        self.BOARD.blit(line, scale(offset(pos, (0, 15))))
        for i, p in enumerate(self.s.players):
            label = myfont.render(p.printSummary(), 1, self.playerCols[p])
            self.BOARD.blit(label, scale(offset(pos, (0, (i+1)*30))))

    def drawProperties(self):
        for p in self.s.props.values():
            if p.owner is not None:
                pygame.draw.rect(self.BOARD, self.playerCols[p.owner], (*fieldLocs[p.id], s(50), s(20)))

                if Property.__instancecheck__(p) and p.houses != 0:
                    font = pygame.font.Font(None, s(20))
                    nrHouses = font.render(str(p.houses), 1, BLACK)
                    self.drawHouse(p)
                    if not p.hotel:
                        self.BOARD.blit(nrHouses, offset(fieldLocs[p.id], scale((6, 6))))

    def plotResults(self):
        fig = self.s.plotStats(SCALE)
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        raw_data = canvas.get_renderer().tostring_rgb()
        size = canvas.get_width_height()
        graph = pygame.transform.rotozoom(pygame.image.fromstring(raw_data, size, "RGB"), 0, SCALE)
        self.BOARD.blit(graph, offset(BOARD_SIZE, (-graph.get_width(), -graph.get_height())))

    def drawHouse(self, p):
        color = YELLOW if p.hotel else RED
        house = np.array([(1, 18), (17, 18), (17, 9), (9, 1), (1, 9)])*SCALE
        pointlist = list(map(offset, house, [fieldLocs[p.id]]*5))
        pygame.draw.polygon(self.BOARD, color, pointlist)

    def run(self):
        for i in range(self.nrMaxRounds):
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.s.currentRound = i
            done = self.s.runOneRound()

            self.updateBoard()
            self.plotResults()
            pygame.display.update()

            if done:
                break

        sleep(10)
        return done
