#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Board tests"""

# Imports
from unittest import TestCase

import numpy as np

import board
import tile

__author__ = "Michael Lane"
__email__ = "mikelane@gmail.com"
__copyright__ = "Copyright 2017, Michael Lane"
__license__ = "MIT"


class TestBoard(TestCase):
    def test_is_solved(self):
        b = board.Board((2, 2))
        self.assertFalse(b.is_solved())
        b.place_tile(tile.OTile(), (0, 0))
        self.assertTrue(b.is_solved())

    def test_tile_can_be_placed(self):
        b = board.Board((2, 3))
        self.assertTrue(np.array_equal(b.tile_can_be_placed(tile.FiveTile()), np.array([0, 0])))
        self.assertFalse(b.tile_can_be_placed(tile.ITile()))

    def test_get_potential_locations(self):
        b = board.Board((3, 5))
        b.place_tile(tile.OTile(), (0, 0))
        self.assertTrue((1, 0) in b.get_potential_locations(tile.LTile().rotate()))

    def test_tile_fits(self):
        b = board.Board((3, 5))
        b.place_tile(tile.OTile(), (0, 0))
        self.assertTrue(b.tile_fits(tile.LTile().rotate(), (1, 0)))
        self.assertFalse(b.tile_fits(tile.FiveTile(), (0, 1)))

    def test_place_tile(self):
        b = board.Board((3, 3))
        b.place_tile(tile.tile_factory('5').rotate(), (0, 0))
        self.assertTrue(np.array_equal(b.board, np.array([[0, 1, 1], [0, 0, 1], [1, 0, 1]])))

    def test_remove_tile(self):
        b = board.Board((4, 6))
        b.place_tile(tile.tile_factory('2'), (1, 2))
        b.remove_tile(tile.tile_factory('2'), (1, 2))
        self.assertTrue(np.array_equal(np.ones((4, 6), dtype=np.int), b.board))

    def test_is_valid(self):
        b = board.Board((5, 5))
        b.place_tile(tile.tile_factory('I'), (0, 1))
        b.place_tile(tile.tile_factory('I'), (1, 0))
        self.assertFalse(b.is_valid())

    def test_gen_board_output(self):
        solution = [
            ((0, 0), tile.tile_factory('I').rotate()),
            ((2, 0), tile.tile_factory('T').rotate().rotate()),
            ((2, 2), tile.tile_factory('T')),
            ((0, 3), tile.tile_factory('5')),
            ((1, 0), tile.tile_factory('L').rotate().rotate().rotate()),
            ((1, 4), tile.tile_factory('P').rotate().rotate())
        ]
        output = board.Board().gen_board_output((4, 6), solution)
        self.assertEqual(output, 'aaaabb\ncccbbd\ncefffd\neeefdd')
