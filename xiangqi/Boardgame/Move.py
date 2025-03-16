from .Coord import Coord

class Move():
  def __init__(self, src_pos : Coord, dest_pos : Coord):
    self.src = src_pos
    self.dest = dest_pos