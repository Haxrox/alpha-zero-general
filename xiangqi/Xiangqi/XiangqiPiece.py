from Boardgame import Piece

from .Colour import Colour

class XiangqiPiece(Piece):
  def __init__(self, name : str, colour : Colour):
    super().__init__(name)
    self._colour = colour
    self._icon = f"{self._colour.name[0].lower()}{self.name[0].upper()}"
    self._legal_moves = []

  def get_legal_moves(self):
    return self._legal_moves