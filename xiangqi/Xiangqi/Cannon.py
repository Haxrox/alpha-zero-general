from .XiangqiPiece import XiangqiPiece, Colour
from ..Boardgame import Coord, Board

class Cannon(XiangqiPiece):
  def __init__(self, colour, Colour = Colour.NONE):
    super().__init__("Cannon", colour)
    self._legal_vectors = []

    for i in range(0, 9):
      self._legal_vectors += [
        Coord(0, 1*i), Coord(0, -1*i), Coord(1*i, 0), Coord(-1*i, 0)
      ]

    self._legal_vectors += [
      Coord(0, 9), Coord(0, -9)
    ]

  def is_valid_board_dest(self, board : Board, dest : Coord):
    # Make sure no pieces are blocking the Cannon's valid moves
    delta = dest - self.coord
    block_count = 0

    for i in range(0, delta.x + 1):
      for j in range(0, delta.y + 1):
        blocking_coord = self.coord + Coord(i, j)
        if board.has_piece(blocking_coord):
          block_count += 1
    # print(f"Piece: {self} | Coord: {self.coord} | Dest: {dest} | Blocking coord: {blocking_coord}")

    return (block_count == 0 and not board.has_piece(dest)) or (block_count == 1 and not board.has_piece(dest))