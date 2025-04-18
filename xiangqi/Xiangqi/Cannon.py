from itertools import zip_longest
import math

from .XiangqiPiece import XiangqiPiece, Colour
from ..Boardgame import Coord, Board

class Cannon(XiangqiPiece):
  def __init__(self, colour, Colour = Colour.NONE):
    super().__init__("Cannon", colour)
    self._legal_vectors = []

    for i in range(1, 9):
      self._legal_vectors += [
        Coord(0, 1*i), Coord(0, -1*i), Coord(1*i, 0), Coord(-1*i, 0)
      ]

    self._legal_vectors += [
      Coord(0, 9), Coord(0, -9)
    ]

  def is_valid_board_dest(self, board : Board, dest : Coord):
    if not super().is_valid_board_dest(board, dest):
      return False
    # Make sure no pieces are blocking the Cannon's valid moves
    delta = dest - self.coord
    block_count = 0

    # print(f"Piece: {self} | Coord: {self.coord} | Dest: {dest} | Delta: {delta}")

    block_count = len(list(filter(
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
    )))

    # print(f"Block count: {block_count}")

    # block_count = sum(
    #   1 for _ in filter(
    #   lambda coord: board.has_piece(coord),
    #   (self.coord + Coord(x, y) for x, y in zip_longest(
    #     range(delta.x),
    #     range(delta.y),
    #     fillvalue=0
    #   ))
    #   )
    # )

    # for x, y in zip_longest(
    #   range(delta.x),
    #   range(delta.y),
    #   fillvalue = 0
    # ):
    # # for i in range(0, delta.x + 1):
    #   # for j in range(0, delta.y + 1):
    #     blocking_coord = self.coord + Coord(x, y)
    #     # print(f"blocking_coord: {blocking_coord} | x: {x} | y: {y} | block_count: {block_count}")
    #     if board.has_piece(blocking_coord):
    #       block_count += 1

    # print(f"Block count: {block_count}")

    return (block_count == 0 and not board.has_piece(dest)) or (block_count == 1 and board.has_piece(dest))