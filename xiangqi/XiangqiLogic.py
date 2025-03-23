from .Boardgame import Board, Coord, Move
from .Xiangqi import Colour, XiangqiPiece, King, Advisor, Elephant, Knight

from itertools import chain
from functools import partial

import numpy as np

PLANE_MAPPING = {
  # Pawn: 0,
  # Rook: 1,
  Knight: 2,
  Elephant: 3,
  Advisor: 4,
  King: 5,
  # Cannon: 6
}

COLOUR_MAPPING = {
  Colour.RED: 0,
  Colour.BLACK: 7
}

class XiangqiBoard(Board):
  def __init__(self, rows : int = 9, cols : int = 10):
    super().__init__(rows, cols)

    self.planes = 14

  @classmethod
  def from_encoding(cls, encoding : np.ndarray):
    plane_count, rows, cols = encoding.shape
    instance = cls(rows, cols)

    for plane_num in range(0, plane_count):
      plane = encoding[plane_num]
      if plane_num < 7:
        colour = Colour.RED
      else:
        colour = Colour.BLACK
        plane_num -= 7

      try:
        piece_cls = next(filter(lambda piece : PLANE_MAPPING[piece] == plane_num, PLANE_MAPPING))

        piece = piece_cls(colour)

        if piece_cls == King:
          if colour == Colour.RED:
            instance._red_king = piece
          else:
            instance._black_king = piece

        # get coords of piece
        for x, y in zip(*plane.nonzero()):
          instance.add_piece(Coord(int(x), int(y)), piece)
      except StopIteration:
        print(f"Could not find piece for plane {plane_num}")

    return instance

  def encode(self) -> np.ndarray:
    encoded_board = np.zeros((self.planes, self.n, self.m))

    for piece in self.pieces:
      colour_plane = COLOUR_MAPPING[piece.colour]
      piece_plane = PLANE_MAPPING[type(piece)]

      encoded_board[piece_plane + colour_plane][piece.coord.x][piece.coord.y] = 1

    return encoded_board.astype(bool)

  def setup(self):
    self._red_king = King(Colour.RED)
    self._black_king = King(Colour.BLACK)

    self.add_piece(Coord(4, 0), self._red_king)
    self.add_piece(Coord(4, 9), self._black_king)

    self.add_piece(Coord(3, 0), Advisor(Colour.RED))
    self.add_piece(Coord(5, 0), Advisor(Colour.RED))

    self.add_piece(Coord(3, 9), Advisor(Colour.BLACK))
    self.add_piece(Coord(5, 9), Advisor(Colour.BLACK))

    self.add_piece(Coord(2, 0), Elephant(Colour.RED))
    self.add_piece(Coord(6, 0), Elephant(Colour.RED))

    self.add_piece(Coord(2, 9), Elephant(Colour.BLACK))
    self.add_piece(Coord(6, 9), Elephant(Colour.BLACK))

    self.add_piece(Coord(1, 0), Knight(Colour.RED))
    self.add_piece(Coord(7, 0), Knight(Colour.RED))

    self.add_piece(Coord(1, 9), Knight(Colour.BLACK))
    self.add_piece(Coord(7, 9), Knight(Colour.BLACK))

  def is_check(self, colour : Colour, move : Move = None) -> bool:
    if move:
      move, _ = self.move(move)

    oppositeColour = colour.opposite()

    king = self._red_king if colour == Colour.RED else self._black_king

    # Check if the opposite colour's pieces can attack the king
    opponent_pieces = filter(lambda piece : piece.colour == oppositeColour, self.pieces)
    dest_positions = chain.from_iterable(piece.get_moves(self) for piece in opponent_pieces)

    is_check = any(map(lambda move : move.dest == king._coord, dest_positions))

    if move:
      self.undo_move(move)

    return is_check

  def is_checkmate(self, colour : Colour):
    return self.is_check(colour) and len(list(self.get_legal_moves(colour))) == 0

  def kings_facing(self, move : Move = None) -> bool:
    if move:
      move, _ = self.move(move)

    kings_facing = self._red_king.coord.x == self._black_king.coord.x

    if kings_facing:
      x = self._red_king.coord.x

      # These are all the cells between the 2 kings that aren't empty
      cells_between_kings = len(list(filter(lambda cell : cell.piece != None, self[x][min(self._red_king.coord.y, self._black_king.coord.y) + 1:max(self._red_king.coord.y, self._black_king.coord.y)])))

      # If there are no pieces between the 2 kings, then they are facing each other
      kings_facing = cells_between_kings == 0

    if move:
      self.undo_move(move)

    return kings_facing

  def get_piece(self, coord : Coord):
    return self.get_cell(coord).piece or XiangqiPiece("..", Colour.NONE)

  def is_legal_move(self, move : Move, colour : Colour):
    return self.is_valid_move(move) and \
      self.get_piece(move.src).colour == colour and \
      self.get_piece(move.dest).colour != colour and \
      not self.is_check(colour, move) and \
      not self.kings_facing(move)

  def get_legal_moves(self, colour : Colour):
    for piece in filter(lambda piece : piece.colour == colour, self.pieces):
      yield from filter(lambda move : self.is_legal_move(move, colour), piece.get_moves(self))

if __name__ == "__main__":
  board = XiangqiBoard()
  board.setup()
  print(board)

  red_king_board_move, _ = board.move(Move(Coord(4, 0), Coord(4, 1)))
  print(board)
  assert board._red_king.coord == Coord(4, 1), "Red king should be at (4, 1)"

  black_king_board_move, _ = board.move(Move(Coord(4, 9), Coord(4, 8)))
  print(board)
  assert board._black_king.coord == Coord(4, 8), "Black king should be at (4, 8)"

  board.undo_move(black_king_board_move)
  print(board)

  assert board._black_king.coord == Coord(4, 9), "Black king should be at (4, 9)"
  assert board.kings_facing(), "Kings should be facing each other"

  advisor_move, _ = board.move(Move(Coord(3, 9), Coord(4, 8)))
  print(board)

  advisor_piece = board.get_piece(Coord(4, 8))
  assert type(advisor_piece) == Advisor, "Piece at (4, 8) should be a advisor"
  assert advisor_piece.colour == Colour.BLACK, "Advisor at (4, 8) should be black"
  assert not board.kings_facing(), "Kings should not be facing each other"

  print("Red king moves")
  for move in board._red_king.get_moves(board):
    print(move)

  print("Red legal moves")
  red_legal_moves = board.get_legal_moves(Colour.RED)

  for move in red_legal_moves:
    print(move)

  print("Black legal moves")
  black_legal_moves = board.get_legal_moves(Colour.BLACK)
  for move in black_legal_moves:
    print(move)