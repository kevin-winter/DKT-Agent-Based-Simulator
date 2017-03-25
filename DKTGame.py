from Simulator import Simulator
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import numpy as np
import pygame
from pygame.locals import *
from time import sleep
import sys
from game_constants import *
from Property import Property
import matplotlib

class DKTGame:

    def __init__(self, nrPlayers=3, nrMaxRounds=10000):
        pygame.init()
        matplotlib.use("Agg")
        plt.style.use('ggplot')

        self.playerCols = {}
        self.nrPlayers = nrPlayers
        self.nrMaxRounds = nrMaxRounds
        self.s = Simulator(self.nrPlayers)
        self.BOARD = self.initBoard()

    def initBoard(self):
        DISPLAYSURF = pygame.display.set_mode((1640, 1000))
        pygame.display.set_caption('DKT Simulator')
        for i, p in enumerate(self.s.players):
            self.playerCols[p] = COLS[i]
        return DISPLAYSURF

    def updateBoard(self):
        self.BOARD.fill(WHITE)
        self.BOARD.blit(BOARD_BG, (0,0))
        self.printStats()
        self.drawProperties()
        for i, p in enumerate(self.s.players):
            pygame.draw.circle(self.BOARD, self.playerCols[p], self.offset(playerLocs[p.currentPosition], (i*5, i*5)), 20, 0)

    def printStats(self):
        myfont = pygame.font.Font(None, 40)
        for i, p in enumerate(self.s.players):
            label = myfont.render(p.printSummary(), 1, self.playerCols[p])
            self.BOARD.blit(label, (1020, 20+i*50))

    def drawProperties(self):
        for p in self.s.props.values():
            if p.owner is not None:
                pygame.draw.rect(self.BOARD, self.playerCols[p.owner], (*fieldLocs[p.id], 50, 20))

                if Property.__instancecheck__(p) and p.houses != 0:
                    font = pygame.font.Font(None, 20)
                    nrHouses = font.render(str(p.houses), 1, BLACK)
                    self.drawHouse(p)
                    if not p.hotel:
                        self.BOARD.blit(nrHouses, self.offset(fieldLocs[p.id], (6, 6)))

    def offset(self, tup, offset):
        return tuple(map(sum, zip(tup, offset)))

    def plotResults(self):
        fig = self.s.plotStats()
        self.plotToCanvas(fig, (1000, 520))

    def plotToCanvas(self, fig, xy):
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        raw_data = canvas.get_renderer().tostring_rgb()
        size = canvas.get_width_height()
        graph = pygame.image.fromstring(raw_data, size, "RGB")
        self.BOARD.blit(graph, xy)

    def plotTable(self):
        data = self.s.playerData()
        table = r'\begin{table} ' \
                r'\begin{tabular}{|l|l|l|}  \hline  ' \
                r'200 & 321 & 50 \\  \hline  ' \
                r'\end{tabular} \end{table}'
        fig = plt.figure()
        ax=plt.gca()
        plt.plot(np.arange(100))
        plt.text(10,80,table, size=50)
        self.plotToCanvas(fig, (1000, 0))

    def drawHouse(self, p):
        color = YELLOW if p.hotel else RED
        house = [(1, 18), (17, 18), (17, 9), (9, 1), (1, 9)]
        pointlist = list(map(self.offset, house, [fieldLocs[p.id]]*5))
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
            #plotTable(sim)
            #self.plotResults()
            pygame.display.update()

            if done:
                sleep(10)
                break

