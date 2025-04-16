from .Coord import Coord
from .Piece import Piece
from .Cell import Cell
from .Move import Move
from .BoardMove import BoardMove

from collections import deque
import logging

import numpy as np

# Set up logging
logger = logging.getLogger(__name__)

class Board():
  def __init__(self, rows : int, cols : int):
    self.n = rows
    self.m = cols

    self.matrix = [[Cell(Coord(x, y), None) for y in range(self.m)] for x in range(self.n)]
    self.pieces = []
    self.moves = deque()

  def get_cell(self, coord : Coord) -> Cell:
    assert coord.x >= 0 and coord.x < self.n, f"coord.x: {coord.x}, n: {self.n}"
    assert coord.y >= 0 and coord.y < self.m, f"coord.y: {coord.y}, m: {self.m}"

    return self.matrix[coord.x][coord.y]

  def has_piece(self, coord : Coord) -> bool:
    return self.get_cell(coord).piece != None

  def get_piece(self, coord : Coord) -> Piece:
    return self.get_cell(coord).piece or Piece("..")

  def set_piece(self, coord : Coord, piece : Piece):
    self.get_cell(coord).piece = piece

  def add_piece(self, coord : Coord, piece : Piece):
    piece.coord = coord
    self.set_piece(coord, piece)
    self.pieces.append(piece)

  def is_valid_coord(self, coord : Coord) -> bool:
    return coord.x >= 0 and coord.x < self.n and coord.y >= 0 and coord.y < self.m

  def is_valid_move(self, move : Move) -> bool:
    return self.is_valid_coord(move.src) and self.is_valid_coord(move.dest)

  def undo_move(self, move : BoardMove):
    logger.debug(f"undo_move({move})")
    undo_move = Move(move.dest, move.src)
    self.move(undo_move)

    if move.dest_piece:
      self.add_piece(move.dest, move.dest_piece)

  def move(self, move : Move) -> (BoardMove, str):
    if not self.is_valid_move(move):
      return None, "Invalid move"

    src_cell = self.get_cell(move.src)
    dest_cell = self.get_cell(move.dest)

    assert src_cell, f"src_cell: {src_cell}"
    assert dest_cell, f"dest_cell: {dest_cell}"

    if not src_cell.piece:
      return None, "No piece to move"

    src_cell.piece.coord = move.dest

    if dest_cell.piece:
      self.pieces.remove(dest_cell.piece)
      dest_cell.piece.coord = None

    board_move = BoardMove(move, dest_cell.piece)
    self.moves.append(board_move)

    dest_cell.piece = src_cell.piece
    src_cell.piece = None

    logger.debug(f"move({move}) {board_move}")

    for piece in self.pieces:
      logger.debug(f"piece: {piece} | coord: {piece.coord}")
    return board_move, "Move successful"

  def flip(self):
    # numpy flip matrix
    # logger.debug(f"Flipping board")
    # logger.debug(f"Before flip:\n{self}")
    self.matrix = np.flip(self.matrix, axis=1)
    # logger.debug(f"After flip:\n{self}")

    # # flip the board
    # flipped_matrix = [[None for _ in range(self.n)] for _ in range(self.m)]
    # for x in range(self.n):
    #   for y in range(self.m):
    #     flipped_matrix[y][x] = self.matrix[x][y]

    # flip the pieces
    # for piece in self.pieces:
      # piece.coord = Coord(piece.coord.x, abs(self.m - piece.coord.y - 1))

    for x in range(self.n):
      for y in range(self.m):
        cell = self.matrix[x][y]
        if cell.piece:
          cell.piece.coord = Coord(x, y)
          assert cell.piece.coord == Coord(x, y), f"Cell: {cell} | cell.piece.coord: {cell.piece}"

    # self.matrix = flipped_matrix

  def stringRepresentation(self):
    # create a string representation of the board
    board_str = ""
    for x in range(self.n):
      for y in range(self.m):
        piece = self.get_piece(Coord(x, y))
        board_str += piece.icon + " "
      board_str += "\n"
    return board_str

  # add [][] indexer syntax to the Board
  def __getitem__(self, index) -> Piece:
    return self.matrix[index]

  def __str__(self):
    n = self.n
    m = self.m
    display_str = "Board:\n   "
    for y in range(m):
        display_str += f"{y}  "
    display_str += "\n"
    display_str += "-------------------------------\n"
    for y in range(m):
        display_str += f"{y} |"    # print the row #
        for x in range(n):
            piece = self.get_piece(Coord(x, y))    # get the piece to print
            display_str += f"{piece.icon} "
        display_str += "|\n"
    display_str += "-------------------------------\n"

    display_str += "Pieces:\n"
    for piece in self.pieces:
      display_str += f"{piece}\n"
    display_str += "-------------------------------\n"
    return display_str

  @staticmethod
  def display(board):
    print(board)
