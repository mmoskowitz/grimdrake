#!/usr/bin/env python

from Filler import Filler
from Grid import Grid
import math

grid = Grid(15, 15, None, None)
for i in range(0, 7):
    grid.bars[Grid.ACROSS][i * 2 + 1] = int(math.pow(2, 14)) - 1
    grid.bars[Grid.DOWN][i * 2 + 1] = int(math.pow(2, 14)) - 1
grid.bars[Grid.ACROSS][0] = 3 * 64
grid.bars[Grid.ACROSS][2] = 3 * 256
grid.bars[Grid.ACROSS][4] = 3 * 16
grid.bars[Grid.ACROSS][6] = 3 * 64
grid.bars[Grid.ACROSS][8] = 3 * 64
grid.bars[Grid.ACROSS][10] = 3 * 256
grid.bars[Grid.ACROSS][12] = 3 * 16
grid.bars[Grid.ACROSS][14] = 3 * 64
grid.bars[Grid.DOWN][0] = 3 * 64
grid.bars[Grid.DOWN][2] = 3 * 256
grid.bars[Grid.DOWN][4] = 3 * 16
grid.bars[Grid.DOWN][6] = 3 * 64
grid.bars[Grid.DOWN][8] = 3 * 64
grid.bars[Grid.DOWN][10] = 3 * 256
grid.bars[Grid.DOWN][12] = 3 * 16
grid.bars[Grid.DOWN][14] = 3 * 64
filler = Filler(grid)
filler.lights[0][0] = "m"
filler.lights[2][2] = "y"
filler.lights[4][4] = "a"
filler.lights[6][6] = "n"
filler.lights[8][8] = "s"
filler.lights[10][10] = "w"
filler.lights[12][12] = "e"
filler.lights[14][14] = "r"
filler.lights[0][14] = "i"
filler.lights[2][12] = "s"
filler.lights[4][10] = "c"
filler.lights[6][8] = "o"
filler.lights[8][6] = "u"
filler.lights[10][4] = "r"
filler.lights[12][2] = "s"
filler.lights[14][0] = "e"
# for i in range(7):
#    for j in range(7):
#        filler.lights[i*2+1][j*2+1] = '#'
filler.printgrid()
filler.fill()
filler.printgrid()
