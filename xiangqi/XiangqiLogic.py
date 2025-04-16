from .Boardgame import Board, Coord, Move
from .Xiangqi import Colour, XiangqiPiece, King, Advisor, Elephant, Knight, Rook, Cannon, Soldier

from itertools import chain
from functools import partial
import logging

import numpy as np

logger = logging.getLogger(__name__)

PLANE_MAPPING = {
  Soldier: 0,
  Rook: 1,
  Knight: 2,
  Elephant: 3,
  Advisor: 4,
  King: 5,
  Cannon: 6
}

COLOUR_MAPPING = {
  Colour.RED: 0,
  Colour.BLACK: 7
}

DEFAULT_PIECE_COORDS = {
  Rook: {
    Colour.RED: [
      (0, 0), (8, 0),
    ],
    Colour.BLACK: [
      (0, 9), (8, 9)
    ]
  },
  Knight: {
    Colour.RED: [
      (1, 0), (7, 0)
    ],
    Colour.BLACK: [
      (1, 9), (7, 9)
    ]
  },
  Elephant: {
    Colour.RED: [
      (2, 0), (6, 0)
    ],
    Colour.BLACK: [
      (2, 9), (6, 9)
    ]
  },
  Advisor: {
    Colour.RED: [
      (3, 0), (5, 0)
    ],
    Colour.BLACK: [
      (3, 9), (5, 9)
    ]
  },
  King: {
    Colour.RED: [
      (4, 0)
    ],
    Colour.BLACK: [
      (4, 9)
    ]
  },
  Cannon: {
    Colour.RED: [
      (1, 2), (7, 2)
    ],
    Colour.BLACK: [
      (1, 7), (7, 7)
    ]
  },
  Soldier: {
    Colour.RED: [
      (0, 3), (2, 3), (4, 3), (6, 3), (8, 3)
    ],
    Colour.BLACK: [
      (0, 6), (2, 6), (4, 6), (6, 6), (8, 6)
    ]
  }
}

class XiangqiBoard(Board):
  def __init__(self, rows : int = 9, cols : int = 10):
    super().__init__(rows, cols)

    self.planes = 14
    self._red_king = None
    self._black_king = None

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

        # get coords of piece
        for x, y in zip(*plane.nonzero()):
          piece = piece_cls(colour)

          if piece_cls == King:
            if colour == Colour.RED:
              instance._red_king = piece
            else:
              instance._black_king = piece

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

  def setup(self, piece_coords : dict = DEFAULT_PIECE_COORDS):
    for piece_cls, coords in piece_coords.items():
      for colour, coords in coords.items():
        for coord in coords:
          piece = piece_cls(colour)
          self.add_piece(Coord(*coord), piece)
          if piece_cls == King:
            if colour == Colour.RED:
              self._red_king = piece
            else:
              self._black_king = piece

  def kings_exist(self):
    return self._red_king != None and self._black_king != None and self._red_king.coord != None and self._black_king.coord != None

  def is_check(self, colour : Colour, move : Move = None) -> bool:
    logger.debug(f"is_check({self}, {colour}, {move})")

    if move:
      move, _ = self.move(move)

    if not self.kings_exist():
      logger.debug(f"Kings not on board: {self._red_king}, {self._black_king}")
      if move:
        self.undo_move(move)
      return True

    king = self._red_king if colour == Colour.RED else self._black_king
    oppositeColour = colour.opposite()

    # Check if the opposite colour's pieces can attack the king
    opponent_pieces = filter(lambda piece : piece.colour == oppositeColour, self.pieces)
    dest_positions = chain.from_iterable(piece.get_moves(self) for piece in opponent_pieces)

    is_check = any(map(lambda piece_move : piece_move.dest == king.coord, dest_positions))

    if move:
      self.undo_move(move)

    return is_check

  def is_checkmate(self, colour : Colour):
    logger.debug(f"is_checkmate({self}, {colour})")
    return self.is_check(colour) and len(list(self.get_legal_moves(colour))) == 0

  def kings_facing(self, move : Move = None) -> bool:
    if move:
      move, _ = self.move(move)

    if not self.kings_exist():
      logger.debug(f"Kings not on board: {self._red_king}, {self._black_king}")
      if move:
        self.undo_move(move)
      return True

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
    logger.debug(f"is_legal_move({self}, {move}, {colour})")
    return self.is_valid_move(move) and \
      self.get_piece(move.src).colour == colour and \
      self.get_piece(move.dest).colour != colour and \
      not self.is_check(colour, move) and \
      not self.kings_facing(move)

  def get_legal_moves(self, colour : Colour):
    logger.debug(f"get_legal_moves({self}, {colour})")

    if not self.kings_exist():
      logger.debug(f"Kings not on board: {self._red_king}, {self._black_king}")
      return []

    for piece in filter(lambda piece : piece.colour == colour, self.pieces):
      logger.debug(f"Piece: {piece}")
      logger.debug(f"Piece moves:")
      for move in piece.get_moves(self):
        logger.debug(f"Move: {move}")

      yield from filter(lambda move : self.is_legal_move(move, colour), piece.get_moves(self))

def main():
  board = XiangqiBoard()
  board.setup()
  logger.info(board)

  red_king_board_move, _ = board.move(Move(Coord(4, 0), Coord(4, 1)))
  logger.info(board)
  assert board._red_king.coord == Coord(4, 1), "Red king should be at (4, 1)"

  black_king_board_move, _ = board.move(Move(Coord(4, 9), Coord(4, 8)))
  logger.info(board)
  assert board._black_king.coord == Coord(4, 8), "Black king should be at (4, 8)"

  board.undo_move(black_king_board_move)
  logger.info(board)

  assert board._black_king.coord == Coord(4, 9), "Black king should be at (4, 9)"
  # assert board.kings_facing(), "Kings should be facing each other"

  advisor_move, _ = board.move(Move(Coord(3, 9), Coord(4, 8)))
  logger.info(board)

  advisor_piece = board.get_piece(Coord(4, 8))
  assert type(advisor_piece) == Advisor, "Piece at (4, 8) should be a advisor"
  assert advisor_piece.colour == Colour.BLACK, "Advisor at (4, 8) should be black"
  assert not board.kings_facing(), "Kings should not be facing each other"

  logger.info("Red king moves")
  for move in board._red_king.get_moves(board):
    logger.info(move)

  logger.info("Red legal moves")
  red_legal_moves = board.get_legal_moves(Colour.RED)

  for move in red_legal_moves:
    logger.info(move)

  logger.info("Black legal moves")
  black_legal_moves = board.get_legal_moves(Colour.BLACK)
  for move in black_legal_moves:
    logger.info(move)

def test():
  board = XiangqiBoard()
  piece_coords = {
    King: {
      Colour.RED: [
        (4, 0)
      ],
      Colour.BLACK: [
        (4, 9)
      ]
    },
    Soldier: {
      Colour.RED: [
        (4, 7)
      ],
      Colour.BLACK: [
        (4, 1), (0, 4)
      ]
    }
  }

  board.setup(piece_coords)
  logger.info(board)

  logger.info(f"Red in check: {board.is_check(Colour.RED)}")
  logger.info(f"Black in check: {board.is_check(Colour.BLACK)}")

  logger.info("Red legal moves")
  red_legal_moves = board.get_legal_moves(Colour.RED)
  for move in red_legal_moves:
    logger.info(move)

  logger.info("Black legal moves")
  black_legal_moves = board.get_legal_moves(Colour.BLACK)
  for move in black_legal_moves:
    logger.info(move)

  board.move(Move(Coord(4, 0), Coord(4, 1)))
  logger.info(board)

  logger.info(f"Red in check: {board.is_check(Colour.RED)}")
  logger.info(f"Black in check: {board.is_check(Colour.BLACK)}")

  logger.info("Red legal moves")
  red_legal_moves = board.get_legal_moves(Colour.RED)
  for move in red_legal_moves:
    logger.info(move)

  logger.info("Black legal moves")
  black_legal_moves = board.get_legal_moves(Colour.BLACK)
  for move in black_legal_moves:
    logger.info(move)

  board.move(Move(Coord(4, 7), Coord(4, 8)))
  logger.info(board)

  logger.info(f"Red in check: {board.is_check(Colour.RED)}")
  logger.info(f"Black in check: {board.is_check(Colour.BLACK)}")

  logger.info("Red legal moves")
  red_legal_moves = board.get_legal_moves(Colour.RED)
  for move in red_legal_moves:
    logger.info(move)

  logger.info("Black legal moves")
  black_legal_moves = board.get_legal_moves(Colour.BLACK)
  for move in black_legal_moves:
    logger.info(move)

if __name__ == "__main__":
  main()