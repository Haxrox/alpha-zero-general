from .XiangqiPiece import XiangqiPiece, Colour
from ..Boardgame import Coord

class Advisor(XiangqiPiece):
  def __init__(self, colour : Colour = Colour.NONE):
    super().__init__("Advisor", colour)
    self._legal_vectors = [
      Coord(1, 1), Coord(1, -1), Coord(-1, 1), Coord(-1, -1)
    ]

    def bound(coord):
      match self.colour:
        case Colour.RED:
          return Coord(3, 0) <= coord <= Coord(5, 2)
        case Colour.BLACK:
          return Coord(3, 7) <= coord <= Coord(5, 9)

    self._bounds.append(bound)
