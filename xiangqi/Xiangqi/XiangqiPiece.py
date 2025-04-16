from ..Boardgame import Piece, Move, Coord, Board

from .Colour import Colour

import logging

import numpy as np

# Set up logging
logger = logging.getLogger(__name__)
class XiangqiPiece(Piece):
  def __init__(self, name : str, colour : Colour):
    super().__init__(name)
    self._colour = colour
    self._icon = f"{self._colour.name[0].lower()}{self.name[0].upper()}"
    self._legal_vectors = []
    self._bounds = [
      lambda coord: Coord(0, 0) <= coord <= Coord(8, 9)
    ]

  @property
  def colour(self):
    return self._colour

  @colour.setter
  def colour(self, colour : Colour):
    if colour == Colour.NONE:
      raise ValueError("Cannot set colour to NONE")
    self._colour = colour
    self._icon = f"{self._colour.name[0].lower()}{self.name[0].upper()}"

  def is_valid_move(self, dest : Coord):
    return all([bound(dest) for bound in self._bounds])

  def is_valid_board_dest(self, board : Board, dest : Coord):
    return True

  def get_moves(self, board : Board = None):
    logger.debug(f"get_moves({self}) | legal_vectors: {self._legal_vectors} | coord: {self.coord}")
    valid_dests = np.array(self._legal_vectors) + self.coord

    for dest in valid_dests:
      # board and board.is_valid_coord(dest)
      if self.is_valid_move(dest) and self.is_valid_board_dest(board, dest):
        yield Move(self.coord, dest)
