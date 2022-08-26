#!/usr/bin/env python

from .Dictionary import Dictionary
from .Filler import Filler
from .Grid import Grid
import copy
import unittest


class TestGridFunctions(unittest.TestCase):

    dict = 0

    def setUp(self):
        if not (self.dict):
            self.dict = Dictionary("./scowlunder55ordered.txt")
        self.filler = Filler(Grid(5, 5))

    #    def testsetup(self):
    #        self.assertEqual(1, 1)

    #    def testpresent(self):
    #        self.assertTrue(self.dict.words['a']['p']['p']['l']['e']['\n'])

    #    def testabsent(self):
    #        self.assertFalse(self.dict.words['b']['p']['p']['l']['e']['\n'])

    def testsearch(self):
        wordlist = self.dict.find_words(("a", ".", "birsp", "l", "e"))
        self.assertTrue(wordlist)
        self.assertTrue("apple" in wordlist)
        self.assertTrue("aisle" in wordlist)
        self.assertFalse("bpple" in wordlist)
        self.assertFalse("essay" in wordlist)
        self.assertFalse("app" in wordlist)
        self.assertFalse("apples" in wordlist)
        self.assertEqual(wordlist[0], "apple")
        self.assertEqual(self.dict.find_word_count(("a", "p", "p", "l", "e")), 1)
        self.assertEqual(self.dict.find_word_count(("b", "p", "p", "l", "e")), 0)
        self.assertEqual(self.dict.find_word_count(("a", ".", "p", "l", "e")), 2)
        self.assertEqual(self.dict.find_letters(("a", ".", "bsp", "l", "e"), 1), "imp")
        self.assertEqual(
            self.filler.convertsearch("a.[bsp]le"), ["a", ".", "bsp", "l", "e"]
        )
        # wordlist = self.dict.find_words(('u', 'p', 'l', '.', '.', '.', 'c', '.', '.'))
        wordlist = self.dict.find_words(("u", "p", "l", ".", ".", ".", "x", ".", "."))
        self.assertEqual(wordlist, [])


if __name__ == "__main__":
    unittest.main()
