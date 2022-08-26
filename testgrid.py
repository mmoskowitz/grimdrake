#!/usr/bin/env python3

from Grid import Grid
from Puzzle import Puzzle
import copy
import unittest


class TestGridFunctions(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(6, 6, None, None)
        self.grid.bars[Grid.ACROSS][0] = 22
        self.grid.bars[Grid.ACROSS][1] = 16
        self.grid.bars[Grid.DOWN][1] = 31
        self.grid.reversebar(4, Grid.ACROSS)
        self.grid.reversebar(5, Grid.ACROSS)
        self.grid.reversebar(4, Grid.DOWN)
        self.grid2 = Grid(4, 7, None, None)

    def testprintgrid(self):
        self.grid.printgrid()
        self.grid2.printgrid()
        self.assertTrue(True)

    def testreverseline(self):
        self.assertEqual(self.grid.reverse_line(13, 5), 22)

    def testbars(self):
        self.assertEqual(self.grid.bars[Grid.ACROSS][5], 13)
        self.assertFalse(self.grid.barpost(2, 0, Grid.ACROSS))
        self.assertTrue(self.grid.barpre(2, 0, Grid.ACROSS))
        self.assertTrue(self.grid.isunchX(0, 2, Grid.ACROSS))
        self.assertTrue(self.grid.isunchX(0, 5, Grid.ACROSS))
        self.assertTrue(self.grid.isunchX(5, 0, Grid.ACROSS))
        self.assertFalse(self.grid.isunchX(0, 0, Grid.ACROSS))

    def testgrid(self):
        self.assertEqual(self.grid.lengthX(2, 0, Grid.DOWN), 6)
        self.assertEqual(self.grid.lengthX(0, 0, Grid.ACROSS), 2)
        self.assertEqual(self.grid.lengthX(0, 3, Grid.ACROSS), 2)
        self.assertEqual(self.grid.lengthX(2, 0, Grid.ACROSS), 6)
        self.assertEqual(self.grid2.lengthX(0, 0, Grid.DOWN), 7)

    def testcheckword(self):
        self.assertEqual(self.grid.checkword(2, 0, Grid.DOWN), Grid.OKAY)
        self.assertEqual(self.grid.checkword(5, 0, Grid.DOWN), Grid.CONSECUTIVE)
        self.assertEqual(self.grid.checkword(1, 1, Grid.DOWN), Grid.NONWORD)
        self.assertEqual(self.grid.checkword(1, 1, Grid.ACROSS), Grid.NONWORD)
        self.assertEqual(self.grid.checkword(2, 0, Grid.ACROSS), Grid.GOOD)
        self.assertEqual(self.grid2.checkword(0, 0, Grid.DOWN), Grid.CHECKED)
        self.assertEqual(self.grid2.checkword(0, 0, Grid.ACROSS), Grid.CHECKED)


if __name__ == "__main__":
    unittest.main()
