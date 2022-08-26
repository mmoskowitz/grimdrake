#!/usr/bin/env python

from .Grid import Grid
from .Puzzle import Puzzle
import sys
import copy

# import cProfile

width = int(sys.argv[1])
height = int(sys.argv[2])

puzzle = Puzzle(width, height, None, None)
# cProfile.run('puzzle.creategrid()')
puzzle.creategrid()

puzzle.fill()
