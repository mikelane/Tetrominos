#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tetrominos Tile functions

CS542
Michael Lane
Homework 1: Tetrominos
Due: 10 April 2017

There are seven basic tetrominos:

     I) ####

         ##
     5) ##

        ##
     2)  ##

     T) ###
         #

          #
     L) ###

     P) ###
          #

     O) ##
        ##
        
The Tetromino Tiling Problem asks for a non-overlapping covering a rectangular grid with a given collection of 
tetrominos. You are to construct a depth-first-search solver for instances of this problem.

Note: Each tetromino, except for the 'O', can be rotated into at least 2 and up to 4 orientations.

"""

import numpy as np
from typing import List, Tuple, Union

__author__ = "Mike"
__email__ = "mikelane@gmail.com"
__copyright__ = "Copyright 2017, Mike"
__license__ = "MIT"
__all__ = ['Tile', 'tile_factory', 'gen_tiles']


class Tile:
    """The base tile class"""

    def __init__(self, tile_type: str, face: np.ndarray, num_orientations: int, orientation: int = 0) -> None:
        """
        Tile constructor. Defaults to an 'O' tile
        :param tile_type:        (str)           The type of tile. Can be one of 'I', '5', '2', 'T', 'L', 'P', or 'O'
        :param face:             (numpy.ndarray) The tile data is stored as a numpy ndarray
        :param num_orientations: (int)           The number of possible orientations for this tile 
        """
        self.type = tile_type
        self.face = face
        self.shape = face.shape
        self.num_orientations = num_orientations
        self.current_orientation = orientation
        self.anchor = np.argwhere(self.face == 1)[0]

    def __str__(self) -> str:
        """
        Returns a printable tile with the metadata included
        :return: (str) The string data
        """
        return 'type: "{}" Orientation: {}\n{}\n'.format(self.type, self.current_orientation, self.face)

    def __repr__(self) -> str:
        return '{}'.format(type(self))

    def __eq__(self, other):
        return (self.type == other.type) \
               and (np.all(self.face == other.face)) \
               and (self.num_orientations == other.num_orientations) \
               and (self.current_orientation == other.current_orientation) \
               and (np.all(self.anchor == other.anchor))

    def rotate(self):
        """
        Rotate the tile 90 degrees and update the current orientation and the tile's shape (height, width)
        :return: (Tile) Returns self to facilitate residual calculations
        """
        self.face = np.rot90(self.face)
        self.current_orientation = (self.current_orientation + 1) % self.num_orientations
        self.shape = self.face.shape
        self.anchor = np.argwhere(self.face == 1)[0]  # Picks the most northern and most western 1
        return self


# Collection of specific tile classes
class OTile(Tile):
    def __init__(self):
        super().__init__('O', np.ones((2, 2), np.int), num_orientations=1)


class ITile(Tile):
    def __init__(self):
        super().__init__('I', np.ones((4, 1), np.int), num_orientations=2)


class LTile(Tile):
    def __init__(self):
        super().__init__('L', np.array([[1, 0], [1, 0], [1, 1]]), num_orientations=4)


class PTile(Tile):
    def __init__(self):
        super().__init__('P', np.array([[1, 1], [1, 0], [1, 0]]), num_orientations=4)


class TwoTile(Tile):
    def __init__(self):
        super().__init__('2', np.array([[1, 1, 0], [0, 1, 1]]), num_orientations=2)


class FiveTile(Tile):
    def __init__(self):
        super().__init__('5', np.array([[0, 1, 1], [1, 1, 0]]), num_orientations=2)


class TTile(Tile):
    def __init__(self):
        super().__init__('T', np.array([[1, 1, 1], [0, 1, 0]]), num_orientations=4)


def tile_factory(tile_type: str) -> Tile:
    """
    The factory method for creating tiles. Take a string character representing a tile type, return a tile of that type.
    :param tile_type: (str)  Desired tile type
    :return:          (Tile) Tile of that type.
    """
    if tile_type == 'O':
        return OTile()
    elif tile_type == 'I':
        return ITile()
    elif tile_type == 'L':
        return LTile()
    elif tile_type == 'P':
        return PTile()
    elif tile_type == '2':
        return TwoTile()
    elif tile_type == '5':
        return FiveTile()
    elif tile_type == 'T':
        return TTile()
    else:
        raise ValueError('ERROR: {} is an unknown Tile type'.format(tile_type))


def gen_tiles(input_str: str) -> Union[List, List[Tuple[str, Tile]]]:
    """
    Generates a list of (label, Tile) tuples such that the Tile type corresponds to the type at each element in the
    input string and the label of the first tile is 'a', the second is 'b', and so on up to the 26th tile which is 'z'.
    If an invalid tile type is passed, an exception will be thrown by the tile factory and bubbled up here.
    :param input_str: (str) String of inputs of tile types.
    :return: [(str, Tile)] Returns a list of tuples that is as long as the input_str
    """
    if input_str == '':
        return []
    return [tile_factory(c) for c in input_str]


if __name__ == '__main__':
    from pprint import pprint

    tiles = gen_tiles('OILP25T')
    pprint(tiles)
    print('-' * 100, '\n')
    for _, tile in tiles:
        for i in range(tile.num_orientations):
            print(tile)
            tile.rotate()
        print('-' * 100, '\n')

    print(OTile() == OTile())
