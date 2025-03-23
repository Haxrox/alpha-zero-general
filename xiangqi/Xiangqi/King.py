from .XiangqiPiece import XiangqiPiece, Colour
from ..Boardgame import Coord

class King(XiangqiPiece):
  def __init__(self, colour, Colour = Colour.NONE):
    super().__init__("General", colour)
    self._legal_vectors = [
      Coord(0, 1), Coord(0, -1), Coord(1, 0), Coord(-1, 0)
    ]

    match self.colour:
      case Colour.RED:
        self._bounds.append(
          lambda coord: Coord(3, 0) <= coord <= Coord(5, 2)
        )
      case Colour.BLACK:
        self._bounds.append(
          lambda coord: Coord(3, 7) <= coord <= Coord(5, 9)
        )