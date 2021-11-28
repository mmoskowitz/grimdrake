#!/usr/bin/env python

import sys, os, random, copy, re

class Dictionary:

    LETTERS = 'abcdefghijklmnopqrstuvwxyz'
    BACK = '0'
    END = '\n'
    VALUE = '1'

    #words hash:
    #a-z plus "end", "back", and "value"
    #end contains rank as int
    #back links back up tree
    #value is value of hash
    #a-z contain more hashes
    words = {}

    def __init__(self, wordssource):
        self.setup_words(wordssource)

    def setup_words(self, wordssource):
        #read in words
        count = 0
        with open(wordssource) as wordsfile:
            #for each word
            for wordline in wordsfile:
                #add to words hash
                self.add_word(wordline,count)
                count += 1
                if (count % 1000 == 0):
                    print "Words ingested: %s" % count

    def add_word(self, word, index):
        tempwords = self.words
        for letter in word.lower():
            if (letter == self.END): #end
                if (letter not in tempwords):
                    tempwords[letter] = index
                    break
            elif (letter in self.LETTERS): #letter
                if (letter not in tempwords):
                    tempwords[letter] = {self.BACK:tempwords, self.VALUE:letter}
                tempwords = tempwords[letter]
            elif (letter in "'"): #skippable
                continue
            else: #non-letter
                break
                
    def find_words(self, searches, sources=None):
        #search format:
        #sequence of strings: 
        # ('a','p','p','l','e') or
        # ('a','.','birs','l','e')
        if (not(sources)):
            sources = (self.words,)
        #add to newsources
        if (len(searches) > 0):
            newsources = []
            search = searches[0]
            for source in sources:
                for letter in source:
                    if (letter in self.LETTERS and (letter in search or search == '.')):
                        newsources.append(source[letter])
            #call find_words
            return self.find_words(searches[1:len(searches)], newsources)
        else:
            wordlist = {}
            for source in sources:
            #generate list of words with numbers
                if (self.END in source):
                    index = source[self.END]
                    word = ''
                    tempsource = source
                    while (self.BACK in tempsource):
                        word = tempsource[self.VALUE] + word
                        tempsource = tempsource[self.BACK]
                    if (word != ''):
                        wordlist[index] = word
            #return them
            indices = wordlist.keys()
            indices.sort()
            return [wordlist[i] for i in indices]
        
    def find_word_count(self,searches):
        return len(self.find_words(searches))

    def find_letters(self,searches,index):
        #print ("index: %s" % index)
        wordlist = self.find_words(searches)
        letters = [word[index] for word in wordlist]
        letters.sort()
        letterstring = ''.join(letters)
        letterstring = re.sub(r'(.)\1+', r'\1', letterstring)
        return letterstring
