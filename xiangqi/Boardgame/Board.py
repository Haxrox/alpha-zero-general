from .Coord import Coord
from .Piece import Piece
from .Cell import Cell
from .Move import Move

import numpy as np

class Board():
  def __init__(self, rows : int, cols : int):
    self.n = rows
    self.m = cols

    self.matrix = [[Cell(Coord(x, y), None) for y in range(self.m)] for x in range(self.n)]
    self.pieces = []

  def get_cell(self, coord : Coord):
    assert coord.x >= 0 and coord.x < self.n, f"coord.x: {coord.x}, n: {self.n}"
    assert coord.y >= 0 and coord.y < self.m, f"coord.y: {coord.y}, m: {self.m}"

    return self.matrix[coord.x][coord.y]

  def get_piece(self, coord : Coord):
    return self.get_cell(coord).piece or Piece("..")

  def set_piece(self, coord : Coord, piece : Piece):
    self.get_cell(coord).piece = piece

  def add_piece(self, coord : Coord, piece : Piece):
    self.set_piece(coord, piece)
    self.pieces.append(piece)

  def move(self, move : Move):
    src_cell = self.get_cell(move.src)
    dest_cell = self.get_cell(move.dest)

    dest_cell.piece = self.get_piece(move.src)
    src_cell.piece = None

  # add [][] indexer syntax to the Board
  def __getitem__(self, index):
    return self.matrix[index]

  def __str__(self):
    n = board.n
    m = board.m
    display_str = "   "
    for y in range(m):
        display_str += f"{y}  "
    display_str += "\n"
    display_str += "-------------------------------\n"
    for y in range(m):
        display_str += f"{y} |"    # print the row #
        for x in range(n):
            piece = board.get_piece(Coord(x, y))    # get the piece to print
            display_str += f"{piece.icon if piece else '.'} "
        display_str += "|\n"
    display_str += "-------------------------------\n"
    return display_str

  @staticmethod
  def display(board):
    print(board)
