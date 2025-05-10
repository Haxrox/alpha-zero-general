from .Move import Move
from .Piece import Piece

class BoardMove():
  def __init__(self, move : Move, dest_piece : Piece):
    self.move = move
    self.dest_piece = dest_piece

  def opposite(self):
    return BoardMove(self.move.opposite(), None)

  @property
  def src(self):
    return self.move.src

  @property
  def dest(self):
    return self.move.dest

  def __str__(self):
    return f"{self.move} {self.dest_piece}"

  def __eq__(self, other):
    return self.move.src == other.src and self.move.dest == other.dest