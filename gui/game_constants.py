import pygame
import numpy as np

def offset(tup, offset):
    return tuple(map(sum, zip(tup, offset)))

def scale(tup):
    return tuple((np.array(tup)*SCALE).astype(int))

def s(size):
    return int(size*SCALE)

#           R       G       B
WHITE   = ( 255 ,   255 ,   255 )
BLACK   = ( 0   ,   0   ,   0   )
GRAY    = ( 185 ,   185 ,   185 )
RED     = ( 255 ,   0   ,   0   )
MAROON	= (	127	,	0	,	0	)
YELLOW	= (	255	,	255	,	0	)
OLIVE	= (	127	,	127	,	0	)
LIME	= (	0	,	255	,	0	)
GREEN	= (	0	,	127	,	0	)
AQUA	= (	0	,	255	,	255	)
TEAL	= (	0	,	127	,	127	)
BLUE	= (	0	,	0	,	255	)
NAVY	= (	0	,	0	,	127	)
FUCHSIA	= (	255	,	0	,	255	)
PURPLE	= (	127	,	0	,	127	)

COLS = [BLACK, RED, GREEN, BLUE, MAROON, OLIVE, LIME, AQUA, TEAL, NAVY, FUCHSIA, PURPLE, YELLOW, GRAY]

SCALE = 0.8
BOARD_SIZE = scale((1640, 1000))
BOARD_BG = pygame.transform.rotozoom(pygame.image.load("gui/DKT_small.bmp"), 0, SCALE)

p_a = np.array([2]*11+[1]*9+[0]*11+[1]*9)
p_b = np.array([8]*11+list(np.arange(9)[::-1])+[0]*11+list(np.arange(9)))
p_consts = BOARD_SIZE[1] * np.array([0.095, 0.089, 0.079])

playerLocs = {i+1 : (int(p_consts[0] + p_a[(i+10) % 40]*p_consts[1] + p_b[(i+10) % 40]*p_consts[2]),
                     int(p_consts[0] + p_a[i]*p_consts[1] + p_b[i]*p_consts[2])) for i in range(40)}


f_a = np.array([0]*10+[-3]+[4]*9+[-3]+[0]*10+[-1]*9)
f_b = np.array(list(np.arange(11)[::-1])+[0]*9+list(np.arange(11))+[10]*9)
f_consts = BOARD_SIZE[1] * np.array([0.067, 0.008, 0.079])


fieldLocs = {i+1 : (int(f_consts[0] + f_a[i] * f_consts[1] + f_b[i] * f_consts[2]),
                    int(f_consts[0] + f_a[(i-10) % 40] * f_consts[1] + f_b[(i-10) % 40] * f_consts[2])) for i in range(40)}