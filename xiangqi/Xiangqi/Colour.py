from enum import Enum

class Colour(Enum):
  RED = 1
  BLACK = -1
  NONE = 0

  def __str__(self):
    match self:
      case Colour.RED:
        return "Red"
      case Colour.BLACK:
        return "Black"
      case Colour.NONE:
        return "None"

  def __neg__(self):
    return Colour(-self.value)

  @staticmethod
  def to_colour(value : int):
    if value == 1:
      return Colour.RED
    elif value == -1:
      return Colour.BLACK
    else:
      return Colour.NONE

  def opposite(self):
    return Colour(-self.value)

  @property
  def name(self):
    match self:
      case Colour.RED:
        return "Red"
      case Colour.BLACK:
        return "Black"
      case Colour.NONE:
        return " "

