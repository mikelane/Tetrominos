#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""HW 1 - Tetrominos: Board management

CS542
Michael Lane
Homework 1: Tetrominos
Due: 10 April 2017

A board will have dimensions no greater than 10. The board will determine if a piece can be placed at a given location,
it will place a piece at a given location, and it will determine if there is any reason to short circuit the current
search branch or the entire search. Some reasons that a search can be terminated:

    1. The board is an invalid size. Each tile has 4 cells, so the board must be a multiple of 4 cells
    2. The number of tiles is invalid. There must be 1/4th as many tiles as there are board cells
    3. There is an odd number of 'T' tiles. Imagine the board is colored like a checkers board. The 'T' tile will take
       up either 3 white and one black or 3 black and one white spaces. So even though the 'T' tile itself only takes up
       4 total tiles, it takes them unevenly in such a way that no collection of other tiles can recover. NOTE: this
       should be evaluated by the AI, not the board.
    4. Partitions are an invalid size. If the board is partitioned by a tile placement, then the number of free cells in 
       each partition must be a multiple of 4.
    5. All tiles have been placed. We should quit searching if we've won!
"""

import re
import string

import numpy as np
from scipy.ndimage.measurements import label
from typing import Tuple, List, Union

from tile import Tile, tile_factory

__author__ = "Michael Lane"
__email__ = "mikelane@gmail.com"
__copyright__ = "Copyright 2017, Michael Lane"
__license__ = "MIT"


class Board:
    """The game board class
    
    This class handles the administration of the game board to include construction, checking to see if a Tile fits in
    a given location, placing a Tile in a specific location, and determining whether or not further Tile placement is
    possible. 
    """

    def __init__(self, size: Tuple[int, int] = (4, 6)) -> None:
        """
        Initialize the game board for a given size
        :param size: Size is a tuple that corresponds to the shape of the underlying numpy array in (row, col) format.
        """
        self.board_size = size
        self.num_cells = np.prod(size)
        self.board = np.ones(size, dtype=np.int)

    def __str__(self) -> str:
        """
        Outputs the current board.
        :return: (str) Printable representation of the board 
        """
        return re.sub(r'[^{}]'.format(string.ascii_lowercase + string.digits + '\n'), '', str(self.board))

    def is_solved(self):
        return self.board.sum() == 0

    def tile_can_be_placed(self, tile: Tile) -> Union[np.ndarray, bool]:
        for location in self.get_potential_locations(tile):
            if self.tile_fits(tile, location):
                return location
        return False

    def get_potential_locations(self, tile: Tile) -> np.ndarray:
        """
        The goal here is to snug a tile up against another tile. If we have the following situation:
        
            0 0 1 1 1
            0 0 1 1 1
            1 1 1 1 1
            
        ... and we are considering placing an L in the following orientation:
        
            0 0 1
            1 1 1
            
        ... the first available open spot (the first 1) will be at [0, 2]. If we place the L there naively, we'll end up
        with 
        
            0 0 1 1 0
            0 0 0 0 0
            1 1 1 1 1
            
        but that isn't what we want. We really want to place it at spot [1,2] with this result:
        
            0 0 1 1 1
            0 0 0 1 1
            0 0 0 1 1
            
        You can see the L is now snug against the O that was already in the top left.
        
        To do this we can find all the cells that are 1 and subtract the value of the anchor to shift the placement 
        point over to the correct location. Then we simply need to filter out any result that has a negative column 
        value since those are invalid.
        
        NOTE: The resulting list does not guarantee the ability to place a tile at the given location. It simply returns
        a list of potential locations and you must still check to see if the tile fits at that location.
        :param tile: (Tile)       The tile to consider
        :return:     (np.ndarray) An array of placement points for a given tile
        """
        result = np.argwhere(self.board == 1) - tile.anchor
        return result[np.all(result >= 0, axis=1)]

    def tile_fits(self, tile: Tile, position: Tuple[int, int]) -> Union[bool, np.ndarray]:
        """
        Determines if a given Tile fits at a given board location.
        :param tile:     (Tile)     The Tile object to be checked
        :param position: (int, int) The location of the top left cell in (row, col) format
        :return:         (bool)     True if the Tile fits at the location, otherwise False
        """
        # If the Tile is too wide or tall to fit at the desired location, reject it.
        if position[0] + tile.shape[0] > self.board.shape[0] or position[1] + tile.shape[1] > self.board.shape[1]:
            return False
        # Otherwise, subtract the Tile values from the values in the Tile-sized subarray. Returns True if all values
        # are greater than or equal to 0 and False if any value is less than 0.
        return np.all(self.board[position[0]:position[0] + tile.shape[0],
                      position[1]:position[1] + tile.shape[1]] - tile.face >= 0)

    def place_tile(self, tile: Tile, position: np.ndarray) -> None:
        """
        Places a Tile at a desired position. This modifies the object's board.
        :param tile:     (Tile)     The Tile object to be placed
        :param position: (int, int) The location of the top left cell in (row, col) format
        :return:         (None)
        """
        # First get the subarray by using numpy's multidimensional slicing method, then
        # modify that slice by subtracting out the values for each cell of the tile.
        self.board[position[0]:position[0] + tile.shape[0], position[1]:position[1] + tile.shape[1]] -= tile.face

    def remove_tile(self, tile: Tile, position: np.ndarray) -> Tile:
        """
        Removes a Tile at a desired position. This modifies the object's board.
        :param tile:     (Tile)     The Tile object to be placed
        :param position: (int, int) The location of the top left cell in (row, col) format
        :return:         (None)
        """
        # First get the subarray by using numpy's multidimensional slicing method, then
        # modify that slice by adding the values for each cell of the tile
        self.board[position[0]:position[0] + tile.shape[0], position[1]:position[1] + tile.shape[1]] += tile.face
        return tile

    def is_valid(self) -> bool:
        """
        Determine if we should keep searching for a fit for a given board state. That is to say, check to see if we can
        short circuit the search.
        :return: (bool, string) False, and the reason if the search should not continue, otherwise True and ""
        """
        # If a Tile splits the available cells into multiple groups and if
        # the groups do not each have a multiple of 4 cells, then no
        labeled_board, num_groups = label(self.board)
        for group_number in range(1, num_groups + 1):
            if (labeled_board == group_number).sum() % 4 != 0:
                return False
        return True

    @staticmethod
    def gen_board_output(board_size, solution:Union[List[Tuple[Tuple[np.ndarray], Tile]], List]) -> str:
        if solution == []:
            return '?'
        to_print = list(zip(string.ascii_lowercase, sorted(solution, key=lambda x: (x[0][0], x[0][1]))))
        helper_board = np.ones(board_size, dtype=np.int)
        result = np.ones(board_size, dtype='U0')
        result[np.where(helper_board == 1)] = '.'
        for label, (position, tile) in to_print:
            helper_board[position[0]:position[0] + tile.shape[0], position[1]:position[1] + tile.shape[1]] -= tile.face
            result[np.where(helper_board == 0)] = label
            helper_board[position[0]:position[0] + tile.shape[0], position[1]:position[1] + tile.shape[1]] += tile.face

        return re.sub(r'[^{}]'.format(string.ascii_lowercase + string.digits + '.\n'), '', str(result))



if __name__ == '__main__':
    board = Board()
    print(board, '\n')
    board.place_tile(tile_factory('L'), np.array([0,1]))
    print(board, '\n')
    board.place_tile(tile_factory('I').rotate(), (0, 1))
    print(board, '\n')
    board.place_tile(tile_factory('2'), [1, 3])
    print(board, '\n')
    components, num_groups = label(board.board)
    print(components)
    for i in range(4):
        for j in range(6):
            print('({},{})'.format(i, j), board.tile_fits(tile_factory('O'), (i, j)))
