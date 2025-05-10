from itertools import zip_longest
import math

import logging

from .XiangqiPiece import XiangqiPiece, Colour
from ..Boardgame import Coord, Board

logger = logging.getLogger(__name__)
class Rook(XiangqiPiece):
  def __init__(self, colour, Colour = Colour.NONE):
    super().__init__("Rook", colour)
    self._legal_vectors = []

    for i in range(1, 9):
      self._legal_vectors += [
        Coord(0, 1*i), Coord(0, -1*i), Coord(1*i, 0), Coord(-1*i, 0)
      ]

    self._legal_vectors += [
      Coord(0, 9), Coord(0, -9)
    ]

  def is_valid_board_dest(self, board : Board, dest : Coord):
    # logger.debug(f"is_valid_board_dest({self}, {dest})")
    if not super().is_valid_board_dest(board, dest):
      return False

    # Make sure no pieces are blocking the rook's valid moves
    delta = dest - self.coord

    return not any(filter(
      lambda coord: board.has_piece(coord),
      map(
        lambda coord: self.coord + Coord(coord[0], coord[1]),
        filter(
          lambda coord: coord != (0, 0),
          zip_longest(
            range(0, delta.x, int(math.copysign(1, delta.x))),
            range(0, delta.y, int(math.copysign(1, delta.y))),
            fillvalue=0
          )
        )
      )
    ))

    for i in range(0, delta.x + 1):
      for j in range(0, delta.y + 1):
        blocking_coord = self.coord + Coord(i, j)
        if board.has_piece(blocking_coord):
          return False
    # print(f"Piece: {self} | Coord: {self.coord} | Dest: {dest} | Blocking coord: {blocking_coord}")

    return True