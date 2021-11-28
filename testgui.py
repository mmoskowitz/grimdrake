#!/usr/bin/env python
import sys
from Puzzle import Puzzle
from Gui import Gui

width = int(sys.argv[1])
height = int(sys.argv[2])
puzzle = Puzzle(width, height, None, None)
#puzzle.grid.randomizegrid()
app = Gui(puzzle) 
app.mainloop() 
