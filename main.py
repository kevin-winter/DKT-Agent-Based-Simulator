from Simulator import Simulator
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import numpy as np
import pygame
from time import sleep
from pygame.locals import *
import sys
from game_constants import *
from Property import Property
import matplotlib
matplotlib.use("Agg")
plt.style.use('ggplot')

playerCols = {}

def initBoard(s):
    DISPLAYSURF = pygame.display.set_mode((1640, 1000))
    pygame.display.set_caption('DKT Simulator')
    for i, p in enumerate(s.players):
        playerCols[p] = COLS[i]
    return DISPLAYSURF

def updateBoard(s):
    BOARD.fill(WHITE)
    BOARD.blit(BOARD_BG, (0,0))
    printStats(s)
    drawProperties(s)
    for i, p in enumerate(s.players):
        pygame.draw.circle(BOARD, playerCols[p], offset(playerLocs[p.currentPosition],(i*5,i*5)), 20, 0)

def printStats(s):
    myfont = pygame.font.Font(None, 40)
    for i, p in enumerate(s.players):
        label = myfont.render(p.printSummary(), 1, playerCols[p])
        BOARD.blit(label, (1020, 20+i*50))

def drawProperties(s):
    for p in s.props.values():
        if p.owner is not None:
            pygame.draw.rect(BOARD, playerCols[p.owner], (*fieldLocs[p.id], 50, 20))

            if Property.__instancecheck__(p) and p.houses != 0:
                font = pygame.font.Font(None, 20)
                nrHouses = font.render(str(p.houses), 1, BLACK)
                nrHotels = font.render(str(p.hotel), 1, BLACK)
                BOARD.blit(HOUSES_BG, fieldLocs[p.id])
                BOARD.blit(nrHouses, offset(fieldLocs[p.id], (6, 6)))
                BOARD.blit(nrHotels, offset(fieldLocs[p.id], (23, 6)))

def offset(tup, offset):
    return tuple(map(sum, zip(tup, offset)))

def plotResults(s):
    fig = s.plotResults()
    plotToCanvas(fig, (1000, 520))

def plotToCanvas(fig, xy):
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    raw_data = canvas.get_renderer().tostring_rgb()
    size = canvas.get_width_height()
    graph = pygame.image.fromstring(raw_data, size, "RGB")
    BOARD.blit(graph, xy)

def plotTable(s):
    data = s.playerData()
    table = r'\begin{table} ' \
            r'\begin{tabular}{|l|l|l|}  \hline  ' \
            r'200 & 321 & 50 \\  \hline  ' \
            r'\end{tabular} \end{table}'
    fig = plt.figure()
    ax=plt.gca()
    plt.plot(np.arange(100))
    plt.text(10,80,table, size=50)
    plotToCanvas(fig, (1000, 0))



pygame.init()
nrGames = 1
nrPlayers = 3
nrMaxRounds = 10000
sim = Simulator(nrPlayers)
BOARD = initBoard(sim)

for i in range(nrMaxRounds):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    sim.currentRound = i
    done = sim.runOneRound()

    updateBoard(sim)
    #plotTable(sim)
    plotResults(sim)
    pygame.display.update()

    #sleep(.2)
    if done:
        sleep(10)
        break

