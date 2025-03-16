from .XiangqiPiece import XiangqiPiece
from Boardgame import Coord

class Advisor(XiangqiPiece):
  def __init__(self, colour):
    super().__init__("Advisor", colour)
    self._legal_moves = [
      Coord(2, 2), Coord(2, -2), Coord(-2, 2), Coord(-2, -2)
    ]
