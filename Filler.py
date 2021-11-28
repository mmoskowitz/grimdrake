#!/usr/bin/env python

import sys, os, random, copy
from Grid import Grid
from Dictionary import Dictionary

class Filler:
	defaultwordssource = './scowlunder55ordered.txt'
	#defaultwordssource = './scowlunder55-2021-04-07.txt'
	#wordssource = './ordered9c.txt'
        is_debug = False
	
        def __init__(self, grid=None, wordssource=defaultwordssource):
                if (grid is not None):
                        self.grid = grid
                        self.lights = []
                        self.setup_lights()
                        self.searchsizes = {}
                        self.searchletters = {}
                        self.entries = []
	                self.searchchoices = {}
                        self.numbers = grid.getnumbers()
                        self.entrylist = []
                        
	        self.dictionary = Dictionary(wordssource)
                self.full_auto = False

        """Prepare to make use of a grid"""
        def set_grid(self, grid):
                self.grid = grid
                self.lights = []
                self.setup_lights()
                self.searchsizes = {}
                self.searchletters = {}
                self.entries = []
	        self.searchchoices = {}
                self.numbers = grid.getnumbers()
                self.entrylist = []
                

	"create lights array"
        def setup_lights(self):
            for x in range(0, self.grid.width):
                self.lights.append([])
                for y in range(0, self.grid.height):
                    self.lights[x].append('.')

        "print if debug is true"
        def debug (self, *str):
                if (self.is_debug):
                        print str
                    
	"print grid to stdout"
	def printgrid (self):
		print '_' + ('__' * self.grid.width)
	
		for row in range(0, self.grid.height): 
			rowstr = '|'
			for col in range(0,self.grid.width):
				light = self.lights[col][row]
				if (light == '.'):
				    rowstr += ' '
				else:
				    rowstr += light
				if (self.grid.barafter(col, row, 1)):	
					rowstr += '|'
				else:
					rowstr += ' '
			print rowstr
			if (row < self.grid.height - 1):
				interrowstr = '+'
				for col in range(0, self.grid.width):	
					if (self.grid.barafter(col, row, 0)):
						interrowstr += '-+'	
					else:
						interrowstr += ' +'
				print interrowstr
		
		print '-' + ('--' * self.grid.width)

	"add a word to the grid"
	def insertword(self, column,row,dir, word):
		tr = row
		tc = column
		for ch in word:
			self.lights[tc][tr] = ch
			if (dir): 
				tc += 1
			else:
				tr += 1
	
	"get the search for a specific word in the grid"
	def getsearch(self, column,row, dir, lookahead):
		wordlength = self.grid.length(column,row,dir)
		#print (column,row,dir,wordlength)
		if (wordlength == 0):
			return ''
		search = ''
		tc = column
		tr = row
		for i in range(0,wordlength):
			search += self.getsearchletter(tc, tr, dir, lookahead)
			if (dir): 
				tc += 1
			else:
				tr += 1
		return search

	def getsearchletter(self, column, row, dir, lookahead):
                #print (column,row)
		ch = self.lights[column][row] 
		if (not(ch in ('.'))):
			return ch
		else: #square is unfilled
			if (lookahead == 0 or self.grid.isunch(column,row,not(dir))):
				return ch
			else:
				return self.lettersforsearch(column, row, not(dir), lookahead - 1)
				
	def lettersforsearch(self, column, row, dir, lookahead):
		tc = column
		tr = row
		index = 0
		while (tc >= 0 and tr >= 0 and self.grid.length(tc, tr, dir) == 0):
			if (dir):
				tc -= 1
			else:
				tr -= 1
			index += 1
		search = self.getsearch(tc, tr, dir, lookahead)
		length = self.grid.length(tc, tr, dir)
		#print (column, row, dir, tc, tr, index)
		return self.getsearchletters(search,length,index)

	def getsearchletters(self, search, length, index):
		if (not(self.searchletters.has_key(search))):
			self.searchletters[search] = {} #create caching hash
		if (self.searchletters[search].has_key(index)):
			return self.searchletters[search][index] #use cache
		letters = self.findsearchletters(search, length, index)
		searchletters = '.'
		if (not(letters == 'abcdefghijklmnopqrstuvwxyz')):
			searchletters = '[' + letters + ']'
		self.searchletters[search][index] = searchletters #feed cache
		return searchletters
		'grep -i ^q....$ /usr/dict/words | sed -e s/^..// | sed -e s/..\$// | tr A-Z a-z | sort | uniq'
		
	"get all the searches for a given location"
	def getsearches(self):
		searches = {}
		for x in range(0,self.grid.width):
			for y in range(0,self.grid.height):
				search = self.getsearch(x,y,1,1)
				if ('.' in search):
					searches[(x,y,1)] = search
				search = self.getsearch(x,y,0,1)
				if ('.' in search):
					searches[(x,y,0)] = search
		return searches

	def getshortestsearchkey (self, searches):
		searchkey = ()
		searchkeycount = 1000000
		for key in searches.keys():
			count = searchkeycount
			search = searches[key]
			if (search in self.searchsizes):
				count = self.searchsizes[search]
			else:
				count = self.findsearchcount(search)
				self.searchsizes[search] = count
			if (count < searchkeycount):
				searchkeycount = count
				searchkey = key
		return searchkey

	"converts 'a.[bsp]le' to ('a','.','bsp','l','e')"
	def convertsearch(self, search):
		newsearch = []
		current = ''
		bracket = False
		for letter in search:
			if (letter == '['):
				bracket = True
				continue
			if (letter == ']'):
				bracket = False
				newsearch.append(current)
				current = ''
				continue
			if (bracket):
				current += letter
				continue
			newsearch.append(letter)
		return newsearch
		

	def findsearchletters(self, search, length, index):
		dsearch = self.convertsearch(search)
		return self.dictionary.find_letters(dsearch, index)
		

	def findsearchcount(self, search):
		dsearch = self.convertsearch(search)
		return self.dictionary.find_word_count(dsearch)
		


	def findsearchlist (self, search):
		if ('[]' in search):
			return []
		dsearch = self.convertsearch(search)
		return self.dictionary.find_words(dsearch)
#		command = "grep -i ^%s$ %s" % (search, self.wordssource)
#		command += ' | tr A-Z a-z | grep -v [^a-z]'
#		list = self.getcommandlist(command)
#		return list

	

	def getcommandfile (self, command):
		# print command
		source = os.popen(command)
		return source


	def getcommandlist (self, command):
		source = self.getcommandfile(command)
		list = []
		line = source.readline()
		while (line):
			list.append(line.strip())
			line = source.readline()
		return list

	def getcommandvalue (self, command):
		source = self.getcommandfile(command)
		value = source.readline().strip()
		return value

	def fill(self):
		#gather list of searches
		searches = self.getsearches()
		if (len(searches) == 0):
			#print self if done
			if (self.is_debug):
                                self.printgrid()
			return True
		#find shortest search
		shortkey = self.getshortestsearchkey(searches)
		#get list
		wlist = list(self.findsearchlist(searches[shortkey]))
		#store old word
		oldword = self.getsearch(shortkey[0],shortkey[1],shortkey[2],0)
		while (wlist):
			#find best
			wtuple = tuple(wlist)
			if (self.searchchoices.has_key(wtuple)):
				word = self.searchchoices[wtuple]
			else:
				if (self.is_debug):
                                        self.printgrid()
                                if (not(self.full_auto)):
				        print "Available for:"
				        print shortkey
				        print searches[shortkey]
				        print len(wlist)
				        print wlist[0:100]
				word = ''
				if (not(self.full_auto)):
					word = raw_input ("type word to choose, [RET] for auto, '!' for full auto or '0' to skip: ")
				if (word and word in '!'):
					self.full_auto = True
					print "switching to full auto"
					print word
					word = ''
				if (not(word)):
					word = random.choice(wlist[0:len(wlist)/4 + 1])
			        #cache choice
				if (word in wlist):
					self.searchchoices[wtuple] = word
			if (word in '0'):
				break
			if (word in wlist):
				wlist.remove(word)
                        if (word in self.entries):
                                continue
			#alter grid
			self.insertword(shortkey[0],shortkey[1],shortkey[2],word)
                        self.entries.append(word)
                        self.entrylist.append((shortkey[2], self.numbers[(shortkey[0], shortkey[1])], word))
			self.debug (shortkey, word)
                        if (self.is_debug):
			        self.printgrid()
			#recurse
			done = self.fill()
                        if (done):
                            self.debug ('done',shortkey,word)
                            return True 
                        else:
                            self.entries.remove(word)
                            self.entrylist.pop()
		#alter grid back
		self.insertword(shortkey[0],shortkey[1],shortkey[2],oldword)
                return False
