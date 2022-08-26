#!/usr/bin/env python3

import copy
from Grid import Grid


class Gridder:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.grid = self.puzzle.grid
        self.score = -50000
        self.direction = Grid.ACROSS
        self.i = 0
        self.j = 0
        self.iterationcount = 0
        self.threshold = -1
        self.tries = 0

    def creategrid(self):
        self.grid = self.puzzle.grid
        self.grid.randomizegrid()
        # self.grid.printgrid()
        self.score = self.grid.gridscore()
        while 1:
            self.tries += 1
            self.printscoredetails()
            self.rowsteps()
            print("score after rowsteps: %d" % self.grid.gridscore())
            self.printscoredetails()
            print("Trying barsteps")
            self.barsteps()
            print("score after barsteps: %d" % self.grid.gridscore())
            self.printscoredetails()
            if not (self.grid.iscorrect()):
                print("Trying doublebarsteps")
                self.doublebarsteps()
                print("score after doublebarsteps: %d" % self.grid.gridscore())
                self.printscoredetails()
            if self.grid.iscorrect():
                print("Grid OK after %d tries" % (self.tries))
                self.printscoredetails()
                self.grid.printgrid()
                return
            else:
                print("Giving up on grid #%d" % self.tries)
                self.grid.printgrid()
                print()
                self.grid.randomizegrid()
                self.score = self.grid.gridscore()
        self.puzzle.grid = self.grid

    def randomizegrid(self):
        self.puzzle.grid = self.grid
        self.grid.randomizegrid()
        self.score = -50000
        self.grid = self.puzzle.grid

    def barsteps(self):
        self.grid = self.puzzle.grid
        self.threshold = 2 * self.grid.width * self.grid.height
        self.iterationcount = 0
        while 1:
            grid2 = copy.deepcopy(self.grid)
            grid2.switchbar(self.direction, self.i, self.j)
            # self.grid.printgrid()
            # grid2.printgrid()
            # print self.grid.gridscore()
            # print grid2.gridscore()
            # die()
            self.comparegrid(grid2, 0)
            if self.iterationcount > self.threshold:
                break
            else:
                self.iterationcount += 1
                # print (self.i, self.j)
                self.j += 1
                if self.j >= self.grid.getdimension(self.direction):
                    self.j = 0
                    self.i += 1
                    if self.i >= self.grid.getdimension(not (self.direction)):
                        self.i = 0
                        self.direction = not (self.direction)
        self.puzzle.grid = self.grid

    def doublebarsteps(self):
        self.grid = self.puzzle.grid
        self.threshold = 2 * self.grid.width * self.grid.height
        self.iterationcount = 0
        while 1:
            grid2 = copy.deepcopy(self.grid)
            grid2.switchbar(self.direction, self.i, self.j)
            grid2.switchbar(self.direction, self.i, self.j + 1)
            # self.grid.printgrid()
            # grid2.printgrid()
            # print self.grid.gridscore()
            # print grid2.gridscore()
            # die()
            self.comparegrid(grid2, 0)
            if self.iterationcount > self.threshold:
                break
            else:
                self.iterationcount += 1
                # print (self.i, self.j)
                self.j += 1
                if self.j + 1 >= self.grid.getdimension(self.direction):
                    self.j = 0
                    self.i += 1
                    if self.i >= self.grid.getdimension(not (self.direction)):
                        self.i = 0
                        self.direction = not (self.direction)
        self.puzzle.grid = self.grid

    def rowsteps(self):
        self.grid = self.puzzle.grid
        self.threshold = (self.grid.width + self.grid.height) * self.grid.width
        self.iterationcount = 0
        while 1:
            grid2 = copy.deepcopy(self.grid)
            grid2.randomizenextbar()
            self.grid.iterate()
            self.iterationcount += 1
            self.comparegrid(grid2, 0)
            if self.iterationcount > self.threshold:
                break
        self.puzzle.grid = self.grid

    def comparegrid(self, grid2, printit):
        score2 = grid2.gridscore()
        if score2 > self.score:
            self.grid = grid2
            # self.grid.printgrid()
            # self.printscoredetails()
            if printit:
                print("Improved from %d to %d" % (self.score, score2))
            self.score = score2
            self.iterationcount = 0
        else:
            if score2 != self.score and printit:
                a = 1
                # print "old %d new %d" % (self.score, score2)

    def printscoredetails(self):
        scores = self.grid.scores
        print(
            "%s = GD %s OK %s LG %s : len %s unc %s cns %s chk %s fil %s"
            % (
                self.score,
                scores[Grid.GOOD],
                scores[Grid.OKAY],
                scores[Grid.LONG],
                scores[Grid.LENGTH],
                scores[Grid.UNCHCOUNT],
                scores[Grid.CONSECUTIVE],
                scores[Grid.CHECKED],
                scores[Grid.FILLED],
            )
        )
