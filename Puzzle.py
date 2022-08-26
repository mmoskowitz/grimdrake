#!/usr/bin/env python

import copy
from Grid import Grid
from Gridder import Gridder
from Filler import Filler


class Puzzle:
    def __init__(self, w, h, a, d):
        self.grid = Grid(w, h, a, d)
        self.gridder = Gridder(self)
        self.filler = Filler(self.grid)
        self.lastnumber = 1

    def creategrid(self):
        self.gridder.creategrid()
        self.grid = self.gridder.grid
        self.filler.grid = self.grid

    def fill(self):
        self.filler.fill()

    def printwordlist(self):
        print((self.filler.entries))
        for row in range(0, grid.width):
            for col in range(0, grid.height):
                a = 1
