#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""HW 1 - Tetrominos

CS542
Michael Lane
Homework 1: Tetrominos
Due: 10 April 2017

As discussed in class, there are seven basic tetrominos:

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

Your program should read an instance description from standard input. The first line of the description will be the 
horizontal and vertical dimension of the grid, separated by a space. The second line will be a string of tetromino 
names. For example (taken from The Talos Principle):

    6 8
    OOI22TTLLPPP
    
The grid size will be no wider or taller than 10. The string of tetromino names will be at most 26 long.

Your program must print on standard output either a ? if the instance has no solution, or a diagram showing a solution 
if one exists. The diagram must consist of lowercase letters showing the pattern of tetrominos making up the solution. 
The tetrominos will be labeled starting with 'a' for the upper-leftmost and proceeding with subsequent letters for each 
tetromino as encountered in a left-to-right, top-to-bottom scan of the grid. For example, for the input given above the 
program might output

    aabbcccc
    aabbddde
    fffghdee
    figghhhe
    iigjklll
    ijjjkkkl
    
Your program must run for no more than 5 seconds on any input instance, as measured on the Linux Lab boxes.

You must provide a brief writeup in ASCII text, UTF-8 text or PDF (with your type and email address in it) describing 
your solution to the problem and showing test runs. You must provide sufficient build instructions and tooling to build 
and run your program. For C or C++ programs you must provide a Makefile, for Rust programs a Cargo file, etc. We will 
try to run your program on our test set to verify that it works.

You must provide at least three tests. The tests should be named "test1-in.txt", "test1-out.txt" and so forth. The input 
file should contain a valid input. The output file should contain the expected output.

Do not submit any files other than text files and PDF files. Do not submit executables. Do not submit Word or OpenOffice 
documents. For the sake of all that is holy, do not submit Notepad UTF-16 files.

All submission materials must be placed in a ZIP file named "hw1-lastname.zip" and uploaded to the course Moodle.
"""

import sys
from collections import Counter
from datetime import datetime

import numpy as np
from typing import Union, List, Tuple

from board import Board
from tile import gen_tiles, Tile

__author__ = "Michael Lane"
__email__ = "mikelane@gmail.com"
__copyright__ = "Copyright 2017, Michael Lane"
__license__ = "MIT"


def tettile(board: Board, tiles: List[Tile]) -> Union[List[Tuple[Tuple[int, int], Tile]], bool]:
    """Attempt to tile the board with tetrominos tiles
    
    The pseudocode is as follows:
    
    tettile(board, tiles) -> solution or fail:
        solution is empty List
        tiles_used is an empty Set
        for each tile in tiles
            if the same type of tile is in the tiles_used set
                continue
            Add the tile to the tiles_used set
            for j from 0 up to the number of rotations for the tile
                position <- location to place tile or False if it cannot be placed
                if position is a location
                    place tile on board
                    if the board is now in an invalid state
                        remove the tile from the board
                        rotate the tile
                        continue
                    append tuple (l, tile) to solution
                    if board is solved
                        return solution
                    result <- tettile(board, tiles except for current tile)
                    if board is solved
                        append result to solution
                        return solution
                    else
                        remove the tile from the board
                        remove the tile from the solution
                rotate tile
        return False
        """
    solution = []
    tiles_used = set()
    for i, tile in enumerate(tiles):
        if tile.type in tiles_used:  # Prevent us from trying the same failed piece over and over
            continue
        tiles_used |= set(tile.type)  # Add the current tile to the set of used tiles
        for j in range(tile.num_orientations):
            # Find the most northwestern possible tile position (or False if there isn't one)
            position = board.tile_can_be_placed(tile)
            if type(position) == np.ndarray:
                # If there's a position, place the tile
                board.place_tile(tile, position)
                # It might be the case that the placed tile partitioned the board such that
                # there is at least one partition that doesn't have a multiple of 4 cells
                if not board.is_valid():
                    # If that's the case, short circuit the search of this branch
                    board.remove_tile(tile, position)
                    tile.rotate()
                    continue
                # Otherwise, append the tile to the list of possible solutions
                solution.append((position, tile))
                if board.is_solved():
                    # If the board is now solved, return the solution so it can bubble up
                    return solution
                # If the board is not solved, call the function recursively, slicing out the current
                # tile from the list of tiles passed into the recursive call
                result = tettile(board, tiles[:i] + tiles[i + 1:])
                if board.is_solved():
                    # If the recursion found a solution, append it to the solution that contains
                    # the current tile and return that to bubble it up
                    return solution + result
                else:
                    # If the recursion did not find a solution, remove the current tile from the list
                    # of solutions and from the board.
                    board.remove_tile(tile, position)
                    solution.pop()
            # Make sure to try all orientations of a piece at the given location
            tile.rotate()
    # Return the empty list if no solution was found
    return solution


if __name__ == '__main__':
    # Get the data from the file passed as a command line parameter. This was used to facilitate
    # development in the pycharm IDE.
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            size, tile_string = f.read().strip().split('\n')
        size = tuple(map(int, size.split(' ')))
    else:  # I expect stdin to be redirected at runtime
        size = tuple(map(int, input().split(' ')))
        tile_string = input()

    # Validate the number of cells is divisble by 4
    if np.prod(size) % 4 != 0:
        print('?')
        exit()

    # Validate that the number of tiles is appropriate for this board
    if len(tile_string) != np.prod(size) / 4:
        print('?')
        exit()

    # There must be an even number of Ts
    tiles_counter = Counter(tile_string)
    if tiles_counter['T'] % 2 != 0:
        print('?')
        exit()

    board = Board(size)
    tiles = gen_tiles(tile_string)

    # Attempt to find a solution
    solution = tettile(board, tiles)
    # Print the solution or ?
    print(Board().gen_board_output(board.board_size, solution))

