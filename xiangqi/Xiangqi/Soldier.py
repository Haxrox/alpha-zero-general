import logging

from .XiangqiPiece import XiangqiPiece, Colour
from ..Boardgame import Coord, Board

# Set up logging
logger = logging.getLogger(__name__)

class Soldier(XiangqiPiece):
  def __init__(self, colour : Colour = Colour.NONE):
    super().__init__("Soldier", colour)
    self._legal_vectors = [
      Coord(1, 0), Coord(-1, 0)
    ]

    def bound(coord):
      match self.colour:
        case Colour.RED:
          return Coord(0, 3) <= coord <= Coord(9, 10)
        case Colour.BLACK:
          return Coord(0, 0) <= coord <= Coord(9, 6)

    match self.colour:
      case Colour.RED:
        self._legal_vectors.append(
          Coord(0, 1)
        )
      case Colour.BLACK:
        self._legal_vectors.append(
          Coord(0, -1)
        )

    self._bounds.append(bound)

  def is_valid_board_dest(self, board : Board, dest : Coord):
    # logger.debug(f"is_valid_board_dest({self}, {dest})")
    if not super().is_valid_board_dest(board, dest):
      return False

    delta = dest - self.coord

    if delta.x != 0:
      match self.colour:
        case Colour.RED:
          return self.coord.y >= 5
        case Colour.BLACK:
          return self.coord.y <= 4

    return True
