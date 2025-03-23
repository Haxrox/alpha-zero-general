from .Coord import Coord

class Move():
  def __init__(self, src_pos : Coord, dest_pos : Coord):
    self.src = src_pos
    self.dest = dest_pos

  def __getitem__(self, key):
    return self[key]

  def __eq__(self, other):
    return self.src == other.src and self.dest == other.dest

  def __str__(self):
    return f"{self.src} -> {self.dest}"