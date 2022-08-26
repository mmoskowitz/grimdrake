#!/usr/bin/env python
from tkinter import *
from Puzzle import Puzzle
from Grid import Grid


class Gui(Frame):

    BAR_LENGTH = 20
    BAR_THICKNESS = 3

    def __init__(self, puzzle, master=None):
        Frame.__init__(self, master)
        self.puzzle = puzzle
        width = puzzle.grid.width
        height = puzzle.grid.height
        self.grid()
        self.setupStructs(width, height)
        self.createWidgets(width, height)
        self.displayGrid()
        self.master.title("Grimdrake")

    def setupStructs(self, width, height):
        self.vbars = []
        self.hbars = []
        self.squares = []
        for x in range(0, width):
            self.hbars.append([])
            self.squares.append([])
            if x < width:
                self.vbars.append([])

    def createWidgets(self, width, height):
        self.createGridDisplay(width, height)
        self.createInfoDisplay()
        self.createControls()
        self.createQuitButton()

    def createGridDisplay(self, width, height):
        self.gridFrame = Frame(self, bd=4)
        for x in range(0, width * 2 - 1):
            self.gridFrame.columnconfigure(x, pad=0)
        for y in range(0, height * 2 - 1):
            self.gridFrame.rowconfigure(y, pad=0)
        self.gridFrame.grid(row=1)
        # squares
        for x in range(0, width):
            for y in range(0, height):
                square = Label(self.gridFrame, text=" ")
                square.grid(column=x * 2, row=y * 2)
                square.gd_col = x
                square.gd_row = y
                self.squares[x].append(square)
        # vbars
        for x in range(0, width - 1):
            for y in range(0, width):
                vbar = Canvas(
                    self.gridFrame,
                    bg="#000",
                    width=self.BAR_THICKNESS,
                    height=self.BAR_LENGTH,
                )
                vbar.grid(column=x * 2 + 1, row=y * 2)
                vbar.gd_line = y
                vbar.gd_space = x
                vbar.gd_dir = Grid.ACROSS
                vbar.bind("<Button-1>", self.switchBar)
                self.vbars[x].append(vbar)
        # hbars
        for x in range(0, width):
            for y in range(0, width - 1):
                hbar = Canvas(
                    self.gridFrame,
                    bg="#000",
                    width=self.BAR_LENGTH,
                    height=self.BAR_THICKNESS,
                )
                hbar.grid(column=x * 2, row=y * 2 + 1)
                hbar.gd_line = x
                hbar.gd_space = y
                hbar.gd_dir = Grid.DOWN
                hbar.bind("<Button-1>", self.switchBar)
                self.hbars[x].append(hbar)
        # corners
        for x in range(0, width - 1):
            for y in range(0, width - 1):
                corner = Canvas(
                    self.gridFrame,
                    bg="#000",
                    width=self.BAR_THICKNESS,
                    height=self.BAR_THICKNESS,
                )
                corner.grid(column=x * 2 + 1, row=y * 2 + 1)
                # these do nothing, so we can drop them

    def displayGrid(self):
        puzzle = self.puzzle
        width = puzzle.grid.width
        height = puzzle.grid.height
        # vbars
        for col in range(0, width - 1):
            for row in range(0, height):
                isbar = puzzle.grid.barafter(col, row, 1)
                bgval = "#FFF"
                if isbar:
                    bgval = "#000"
                self.vbars[col][row].config(bg=bgval)
        # hbars
        for col in range(0, width):
            for row in range(0, height - 1):
                isbar = puzzle.grid.barafter(col, row, 0)
                bgval = "#FFF"
                if isbar:
                    bgval = "#000"
                self.hbars[col][row].config(bg=bgval)

        # squares
        # for col in range(0, width):
        # for row in range(0, height):
        # entry = puzzle.grid.barafter(col,row,1)
        # self.squares[col][row].config(text=text)
        # score
        puzzle.grid.generatescore()
        if puzzle.grid.iscorrect():
            self.infoDisplay.config(fg="#000")
        else:
            self.infoDisplay.config(fg="#f00")
        scores = puzzle.grid.scores
        infoText = "%s = GOOD %s OK %s LONG %s : len %s unc %s cns %s chk %s fil %s" % (
            puzzle.grid.gridscore(),
            scores[Grid.GOOD],
            scores[Grid.OKAY],
            scores[Grid.LONG],
            scores[Grid.LENGTH],
            scores[Grid.UNCHCOUNT],
            scores[Grid.CONSECUTIVE],
            scores[Grid.CHECKED],
            scores[Grid.FILLED],
        )
        self.infoDisplay.config(text=infoText)

    def switchBar(self, event):
        widget = event.widget
        self.puzzle.grid.switchbar(widget.gd_dir, widget.gd_line, widget.gd_space)
        self.displayGrid()

    def createInfoDisplay(self):
        self.infoDisplay = Label(self, text="")
        self.infoDisplay.grid(row=2)

    def createControls(self):
        self.controlFrame = Frame(self)
        self.controlFrame.grid(row=3)
        self.randomizeButton = Button(
            self.controlFrame, text="Randomize", command=self.randomizeGrid
        )
        self.randomizeButton.grid(row=1, column=1)
        self.rowButton = Button(self.controlFrame, text="Rows", command=self.rowSteps)
        self.rowButton.grid(row=1, column=2)
        self.barButton = Button(self.controlFrame, text="Bars", command=self.barSteps)
        self.barButton.grid(row=1, column=3)
        self.doubleBarButton = Button(
            self.controlFrame, text="Double Bars", command=self.doubleBarSteps
        )
        self.doubleBarButton.grid(row=1, column=4)

    def randomizeGrid(self):
        self.puzzle.gridder.randomizegrid()
        self.displayGrid()

    def rowSteps(self):
        self.puzzle.gridder.rowsteps()
        self.displayGrid()

    def barSteps(self):
        self.puzzle.gridder.barsteps()
        self.displayGrid()

    def doubleBarSteps(self):
        self.puzzle.gridder.doublebarsteps()
        self.displayGrid()

    def createQuitButton(self):
        self.quitButton = Button(self, text="Quit", command=self.quit)
        self.quitButton.grid(row=10)
