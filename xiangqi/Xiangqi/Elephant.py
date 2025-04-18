from .XiangqiPiece import XiangqiPiece, Colour
from ..Boardgame import Coord, Board

class Elephant(XiangqiPiece):
  def __init__(self, colour : Colour = Colour.NONE):
    super().__init__("Elephant", colour)
    self._legal_vectors = [
      Coord(2, 2), Coord(2, -2), Coord(-2, 2), Coord(-2, -2)
    ]

    def bound(coord):
      match self.colour:
        case Colour.RED:
          return Coord(0, 0) <= coord <= Coord(9, 4)
        case Colour.BLACK:
          return Coord(0, 5) <= coord <= Coord(9, 10)

    self._bounds.append(bound)

  def is_valid_board_dest(self, board : Board, dest : Coord):
    if not super().is_valid_board_dest(board, dest):
      return False

    # Make sure no pieces are blocking the elephant
    delta = dest - self.coord
    blocking_coord = self.coord + Coord(delta.x // 2, delta.y // 2)

    return not board.has_piece(blocking_coord)