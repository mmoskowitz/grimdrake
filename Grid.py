#!/usr/bin/env python

import sys, os, random, copy

"""Class to represent a grid. Spaces are a 2-d grid. Bars are two lists, each of which contains a vector field for the bars in that direction."""
class Grid:

	#directions
	NORTH = 0
	EAST = 1
	SOUTH = 2
	WEST = 3

	ACROSS = True
	DOWN = False

	NONWORD = 0
	LENGTH = -1
	CONSECUTIVE = -2
	UNCHCOUNT = -3
	CHECKED = -4
	FILLED = 4
	OKAY = 1
	GOOD = 2
	LONG = 3

	VALUES = {
		NONWORD: 0, 
		LENGTH: -9, 
		CONSECUTIVE: -7, 
		UNCHCOUNT: -6, 
		CHECKED: -4, 
		FILLED: -0.1, 
		OKAY: 3, 
		GOOD: 3, 
		LONG: 2
		}


	def __init__(self, w, h, a=None,d=None):
		self.width = w
		self.height = h
		self.dimension = {Grid.ACROSS: w, Grid.DOWN: h}
		self.init_bars(a,d)
		self.iteratordir = Grid.ACROSS
		self.iteratorline = 0
		self.iteratorbar = 0
		self.scores = {}
		self.iterationcount = 0

	def getdimension(self, dir):
		return self.dimension[dir]

        """prints out grid to the command line"""
	def printgrid (self):
		print '_' + ('__' * self.width)
	
		for row in range(0, self.height): 
			rowstr = '|'
			for col in range(0,self.width):
                                if (self.isblack(col,row)):
                                    rowstr += '#'
                                else:
				    rowstr += ' '
				if (self.barafter(col, row, 1)):	
					rowstr += '|'
				else:
					rowstr += ' '
			print rowstr
			if (row < self.height - 1):
				interrowstr = '+'
				for col in range(0, self.width):	
					if (self.barafter(col, row, 0)):
						interrowstr += '-+'	
					else:
						interrowstr += ' +'
				print interrowstr
		
		print '-' + ('--' * self.width)


        def isblack (self, column, row):
                return self.isunch(column, row, Grid.ACROSS) and self.isunch(column, row, Grid.DOWN)
	def isunch (self, column, row, dir):
		if (dir):
			return self.isunchX(row,column,dir)
		else:
			return self.isunchX(column,row,dir)
		
	def isunchX (self, line, space, dir):
		return self.barpre(line,space,dir) and self.barpost(line,space,dir)

	def length(self, column, row, dir):
		if (dir):
			return self.lengthX(row,column,dir)
		else:
			return self.lengthX(column,row,dir)

	def lengthX(self,line,space,dir):
		#print (line,space,dir)
		if (self.barpost(line,space,dir) or not (self.barpre(line,space,dir))):
			#print ('b',self.barpre(line,space,dir), self.barpost(line,space,dir))
			return 0
		else:
			length = 1
			for i in range(space, self.dimension[dir]):
				if (self.barpost(line,i,dir)):
					#print length
					return length
					break
				length+= 1
			#print length - 1
			return length - 1
			

	#return false if word breaks rules
	#rules:
	#length > 3
	#at least one unch per word
	#no consecutive unches
	#no more than 1/3 unches
	def checkword(self, line, space, dir):
		wordlength = 0
		wordlength = self.lengthX(line, space, dir)
		if (wordlength == 0): #not a word
			#check for filled
			if (self.isunchX(space,line,not(dir)) and self.isunchX(line,space,dir)):
				return Grid.FILLED
			else:
				return Grid.NONWORD
		if (wordlength <= 3):
			return Grid.LENGTH
		unches = 0
		last_unch = -10
		tline = line
		tspace = space
		for i in range(0, wordlength):
			if (self.isunchX(tspace,tline,not(dir))):
			    #print (tline,tspace,dir,'unch')
			    if ((last_unch + 1) == i):
				    return Grid.CONSECUTIVE
			    last_unch = i
			    unches += 1
			    if ((unches * 3) > wordlength):
				    return Grid.UNCHCOUNT
			#else:
				#print(tline,tspace,dir,'ch')
			
			tspace += 1
		if (unches == 0):
			return Grid.CHECKED
		if (wordlength == self.dimension[dir] and wordlength > 8):
			return Grid.LONG
		if (((unches + 1) * 3) > wordlength):
			return Grid.GOOD
		return Grid.OKAY


	def generatescore(self):
		scores = self.scores
		if (scores == {}):
			scores = {
				Grid.NONWORD: 0, 
				Grid.LENGTH: 0, 
				Grid.CONSECUTIVE: 0, 
				Grid.UNCHCOUNT: 0, 
				Grid.CHECKED: 0, 
				Grid.FILLED: 0, 
				Grid.OKAY: 0, 
				Grid.GOOD: 0, 
				Grid.LONG: 0
				}
			for x in range(0,self.width):
				for y in range(0,self.height):
					check = self.checkword(y,x,Grid.ACROSS)
					scores[check] += 1
					check = self.checkword(x,y,Grid.DOWN)
					scores[check] += 1
			self.scores = scores


	def gridscore(self):
		self.generatescore()
		scores = self.scores
		score = sum([scores[key] * Grid.VALUES[key] for key in scores.keys()])
		return score
	#return (3 * scores[Grid.OKAY] + 3 * scores[Grid.GOOD] + 2 * scores[Grid.LONG] - (scores[Grid.LENGTH] + scores[Grid.CONSECUTIVE] + scores[Grid.UNCHCOUNT] + scores[Grid.CHECKED] + scores[Grid.FILLED]) * 8 )

	def iscorrect(self):
		self.generatescore()
		scores = self.scores
		if (scores[Grid.FILLED] > 0):
			return False
		if (self.width > 9 and scores[Grid.LONG] > 2):
			return False
		for i in scores.keys():
			if (i < 0 and scores[i] > 0):
				return False
		return True


	def randomizegrid(self):
		for dir in (Grid.ACROSS, Grid.DOWN):
			lines = self.dimension[not(dir)]
			mid = (lines - 1) / 2
			for x in range(0, mid):
				self.randomizebar(x, dir)
			for x in range(mid, lines):
				self.reversebar(x, dir)
			if (not(lines % 2 == 0)):
				self.symmetricalbar(mid, dir)

	def iterate(self):
		self.iteratorline += 1
		lines = self.dimension[not(dir)]
		if (self.iteratorline >= lines):
			self.iteratordir = not(self.iteratordir)
			self.iteratorline = 0
		self.iterationcount += 1
		#self.printgrid()

	def getthreshold(self):
		return (self.width + self.height) * self.width


	#bars

	def init_bars(self, a, d):
		self.bars = {Grid.DOWN: [], Grid.ACROSS: []}
		self.setup_bars(a,d)

	def bar_in(self, line, bar, tl):
		return (line >> bar) & 1

	def reverse_line(self, line, tl):
		line = ((line >> 1 ) & 0x5555555555555555L) | ((line << 1 ) & 0xaaaaaaaaaaaaaaaaL)
		line = ((line >> 2 ) & 0x3333333333333333L) | ((line << 2 ) & 0xccccccccccccccccL)
		line = ((line >> 4 ) & 0x0f0f0f0f0f0f0f0fL) | ((line << 4 ) & 0xf0f0f0f0f0f0f0f0L)
		line = ((line >> 8 ) & 0x00ff00ff00ff00ffL) | ((line << 8 ) & 0xff00ff00ff00ff00L)
		line = ((line >> 16) & 0x0000ffff0000ffffL) | ((line << 16) & 0xffff0000ffff0000L)
		line = ((line >> 32) & 0x00000000ffffffffL) | ((line << 32) & 0xffffffff00000000L)
		line = (line >> (64 - tl))
		return line

	def setup_bars(self, a, d):
		if (d is None):
			for x in range(0,self.width):
				self.bars[Grid.DOWN].append(0)
		else:
			self.bars[Grid.DOWN] = d
		if (a is None):
			for y in range(0,self.height):
				self.bars[Grid.ACROSS].append(0)
		else:
			self.bars[Grid.ACROSS] = a

	def barpost (self, line, space, dir):
		#print (line,space,dir, 'bp')
		return space == self.dimension[dir] - 1 or self.bar_in(self.bars[dir][line], space, self.dimension[dir])  

	def barpre (self, line, space, dir):
		return space == 0 or self.bar_in(self.bars[dir][line], space - 1, self.dimension[dir])  

	def barafter (self, column, row, dir):
		#print(column, row, dir)
		if (dir):
			return self.barpost(row,column,dir)
		else:
			return self.barpost(column,row,dir)

	def barbefore (self, column, row, dir):
		if (dir):
			return self.barpre(row,column,dir)
		else:
			return self.barpre(column,row,dir)
			
	def randomizebar(self, index, dir):
		# get length
		tl = self.dimension[dir]
		# get bars
		bars = random.getrandbits(tl) & random.getrandbits(tl)
		# set
		self.bars[dir][index] = bars
		self.scores = {}
		self.iterationcount = 0

	def halfbar(self, index, dir):
		# get length
		tl = self.dimension[dir] - 1
		# get bars
		bars = random.getrandbits(tl/2) & random.getrandbits(tl/2)
		# set
		self.bars[dir][index] = bars

	def reversehalfbar(self, index, dir):
		tl = self.dimension[dir] - 1
		bars = self.bars[dir][index]
		bars = bars & 2 ** (tl/2) - 1
		bars = bars | self.reverse_line(bars, tl)
		# set
		self.bars[dir][index] = bars

	def symmetricalbar(self, index, dir):
		self.halfbar(index, dir)
		self.reversehalfbar(index, dir)
		#print bars
		self.scores = {}
		self.iterationcount = 0

	def reversebar(self, index, dir):
		lines = self.dimension[dir]
		#print (index, dir)
		oldbars = self.bars[dir][lines - 1 - index]
		newbars = self.reverse_line(oldbars, self.dimension[dir] - 1)
		self.bars[dir][index] = newbars
		#print oldbars
		#print newbars
		self.scores = {}
		self.iterationcount = 0

	def randomizegivenbar(self, line, dir):
		lines = self.dimension[not(dir)]
		if (line * 2 + 1 == lines):
			self.symmetricalbar(line, dir)
		else:
			self.randomizebar(line, dir)
			self.reversebar(lines - 1 - line, dir)
		
	def randomizerandombar(self):
		dir = random.choice((Grid.ACROSS, Grid.DOWN))
		lines = self.dimension[not(dir)]
		line = random.randint(0, lines - 1)
		self.randomizegivenbar(line,dir)

	def randomizenextbar(self):
		self.randomizegivenbar(self.iteratorline, self.iteratordir)
		self.iterate()

	def switchbar(self, dir, line, space):
		self.scores = {}
		bar = self.bars[dir][line]
		di = self.dimension[dir]
		dj = self.dimension[not(dir)]
		bar = bar ^ (1 << space)
		self.bars[dir][line] = bar
		xi = di - line - 1
		xj = dj - space - 2
		if (xi != line):
			self.reversebar(xi, dir)
		else:
			if (xj != space):
				self.reversehalfbar(line, dir)

        
        def fillbar(self, dir, line, space):
                bar = self.bars[dir][line]
                bar = bar | (1 << space)
                self.bars[dir][line] = bar

        def clearbar(self, dir, line, space):
                self.fillbar(dir, line, space)
                self.switchbar(dir, line, space)

        """Fills a given space in the grid"""
        def fillspace(self, column, row):
	        if (row > 0):
                        self.fillbar(Grid.DOWN, column, row - 1)
	        if (row < self.length):
                        self.fillbar(Grid.DOWN, column, row)
                if (column > 0):
	                self.fillbar(Grid.ACROSS, row, column - 1)
                if (column < self.width):
	                self.fillbar(Grid.ACROSS, row, column)
                        
