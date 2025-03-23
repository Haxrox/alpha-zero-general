from .XiangqiPiece import XiangqiPiece, Colour
from ..Boardgame import Coord, Board

class Knight(XiangqiPiece):
  def __init__(self, colour : Colour = Colour.NONE):
    super().__init__("Knight", colour)
    self._legal_vectors = [
      Coord(2, 1), Coord(2, -1), Coord(1, 2), Coord(1, -2), Coord(-2, 1), Coord(-2, -1), Coord(-1, 2), Coord(-1, -2)
    ]

    match self.colour:
      case Colour.RED:
        self._bounds.append(
          lambda x: Coord(0, 0) <= x <= Coord(9, 4)
        )
      case Colour.BLACK:
        self._bounds.append(
          lambda x: Coord(0, 5) <= x <= Coord(9, 10)
        )

  def is_valid_board_dest(self, board : Board, dest : Coord):
    # Make sure no pieces are blocking the knight
    delta = dest - self.coord
    blocking_coord = self.coord + Coord(int(delta.x / 2), int(delta.y / 2))

    # print(f"Piece: {self} | Coord: {self.coord} | Dest: {dest} | Blocking coord: {blocking_coord}")

    return not board.has_piece(blocking_coord)