#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Short description

Long description
"""

# Imports
from unittest import TestCase

import numpy as np

from tile import OTile, ITile, LTile, PTile, TwoTile, FiveTile, TTile

__author__ = "Michael Lane"
__email__ = "mikelane@gmail.com"
__copyright__ = "Copyright 2017, Michael Lane"
__license__ = "MIT"


class TestTile(TestCase):
    def test_rotate(self):
        tile = OTile()
        self.assertEqual(OTile(), tile.rotate())

        tile = ITile()
        self.assertEqual(np.all(np.array([[1, 1, 1, 1]]) == tile.rotate().face), True)
        self.assertEqual(tile.current_orientation, 1)
        self.assertEqual(np.all(tile.anchor == [0, 0]), True)
        self.assertEqual(ITile(), tile.rotate())

        tile = LTile()
        self.assertEqual(np.all(np.array([[0, 0, 1], [1, 1, 1]]) == tile.rotate().face), True)
        self.assertEqual(tile.current_orientation, 1)
        self.assertEqual(np.all(tile.anchor == [0, 2]), True)
        self.assertEqual(np.all(np.array([[1, 1], [0, 1], [0, 1]]) == tile.rotate().face), True)
        self.assertEqual(tile.current_orientation, 2)
        self.assertEqual(np.all(tile.anchor == [0, 0]), True)
        self.assertEqual(np.all(np.array([[1, 1, 1], [1, 0, 0]]) == tile.rotate().face), True)
        self.assertEqual(tile.current_orientation, 3)
        self.assertEqual(np.all(tile.anchor == [0, 0]), True)
        self.assertEqual(LTile(), tile.rotate())

        tile = PTile()
        self.assertEqual(np.all(np.array([[1, 0, 0], [1, 1, 1]]) == tile.rotate().face), True)
        self.assertEqual(tile.current_orientation, 1)
        self.assertEqual(np.all(tile.anchor == [0, 0]), True)
        self.assertEqual(np.all(np.array([[0, 1], [0, 1], [1, 1]]) == tile.rotate().face), True)
        self.assertEqual(tile.current_orientation, 2)
        self.assertEqual(np.all(tile.anchor == [0, 1]), True)
        self.assertEqual(np.all(np.array([[1, 1, 1], [0, 0, 1]]) == tile.rotate().face), True)
        self.assertEqual(tile.current_orientation, 3)
        self.assertEqual(np.all(tile.anchor == [0, 0]), True)
        self.assertEqual(PTile(), tile.rotate())

        tile = TwoTile()
        self.assertEqual(np.all(np.array([[0, 1], [1, 1], [1, 0]]) == tile.rotate().face), True)
        self.assertEqual(tile.current_orientation, 1)
        self.assertEqual(np.all(tile.anchor == [0, 1]), True)
        self.assertEqual(TwoTile(), tile.rotate())

        tile = FiveTile()
        self.assertEqual(np.all(np.array([[1, 0], [1, 1], [0, 1]]) == tile.rotate().face), True)
        self.assertEqual(tile.current_orientation, 1)
        self.assertEqual(np.all(tile.anchor == [0, 0]), True)
        self.assertEqual(FiveTile(), tile.rotate())

        tile = TTile()
        self.assertEqual(np.all(np.array([[1, 0], [1, 1], [1, 0]]) == tile.rotate().face), True)
        self.assertEqual(tile.current_orientation, 1)
        self.assertEqual(np.all(tile.anchor == [0, 0]), True)
        self.assertEqual(np.all(np.array([[0, 1, 0], [1, 1, 1]]) == tile.rotate().face), True)
        self.assertEqual(tile.current_orientation, 2)
        self.assertEqual(np.all(tile.anchor == [0, 1]), True)
        self.assertEqual(np.all(np.array([[0, 1], [1, 1], [0, 1]]) == tile.rotate().face), True)
        self.assertEqual(tile.current_orientation, 3)
        self.assertEqual(np.all(tile.anchor == [0, 1]), True)
        self.assertEqual(TTile(), tile.rotate())
