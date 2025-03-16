from .XiangqiPiece import XiangqiPiece
from Boardgame import Coord

class King(XiangqiPiece):
  def __init__(self, colour):
    super().__init__("King", colour)
    self._legal_moves = [
      Coord(0, 1), Coord(0, -1), Coord(1, 0), Coord(-1, 0)
    ]
