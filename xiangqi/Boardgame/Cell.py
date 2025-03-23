from .Coord import Coord
from .Piece import Piece

class Cell():
  def __init__(self, pos : Coord, piece : Piece):
    self._pos = pos
    self._piece = None

  @property
  def x(self):
    return self._pos.x

  @property
  def y(self):
    return self._pos.y

  @property
  def pos(self):
    return self._pos

  @property
  def piece(self):
    return self._piece

  @piece.setter
  def piece(self, value : Piece):
    self._piece = value

  def __str__(self):
    return f"{self.pos}: {self.piece}"
