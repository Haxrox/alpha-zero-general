from .Boardgame import Board, Coord, Move, BoardMove
from .Xiangqi import Colour, XiangqiPiece, King, Advisor, Elephant, Knight, Rook, Cannon, Soldier

from itertools import chain
from functools import partial
from collections import deque
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
  HISTORY_PLANES = 4
  PLANES = 14 * (1 + HISTORY_PLANES)

  def __init__(self, rows : int = 9, cols : int = 10):
    super().__init__(rows, cols)

    self.history_planes = self.HISTORY_PLANES
    self.planes = self.PLANES
    self._red_king = None
    self._black_king = None

  @classmethod
  def from_encoding(cls, encoding : np.ndarray):
    plane_count, rows, cols = encoding.shape
    # print(f"Encoding: {encoding}")
    logger.debug(f"from_encoding({XiangqiBoard.display_encoding(encoding)})")
    instance = cls(rows, cols)

    first_nonzero_plane = plane_count

    for i in range(plane_count, 0, -14):
      plane = encoding[i - 14: i]

      if len(plane.nonzero()[0]) == 0:
        logger.debug(f"Plane {i} is empty")
        continue

      logger.debug(f"Initial state {i}")
      first_nonzero_plane = i

      for plane, x, y in zip(*plane.nonzero()):
        logger.debug(f"Plane: {plane} | x: {x} | y: {y}")
        plane_encoding = plane % 14
        if plane_encoding < 7:
          colour = Colour.RED
        else:
          colour = Colour.BLACK
          plane_encoding %= 7

        dest = Coord(int(x), int(y))

        if not instance.has_piece(dest):
          try:
            piece_cls = next(filter(lambda piece : PLANE_MAPPING[piece] == plane_encoding, PLANE_MAPPING))
            piece = piece_cls(colour)
            instance.add_piece(dest, piece)
            logger.debug(f"Adding piece at {dest}: {piece}")
          except StopIteration:
            logger.error(f"Could not find piece for plane {plane_encoding}")
            continue

      break

    logger.debug(f"Initial: {instance}")

    for i in range(1, instance.history_planes + 1):
      current_state = encoding[plane_count - 14 * (i + 1): plane_count - 14 * i]
      prev_state = encoding[plane_count - 14 * i: plane_count - 14 * (i - 1)]

      diff = np.logical_xor(prev_state, current_state)

      nonzero = diff.nonzero()

      logger.debug(f"Prev {i}: {XiangqiBoard.display_encoding(prev_state)}")
      logger.debug(f"Current {i}: {XiangqiBoard.display_encoding(current_state)}")
      logger.debug(f"Diff {i}: {XiangqiBoard.display_encoding(diff)}")
      logger.debug(f"Diff {i}: {nonzero}")

      if len(nonzero[0]) == 0:
        logger.debug(f"No pieces moved in state {i}")
        continue
      elif len(nonzero[0]) == 1:
        logger.debug(f"Only one piece moved in state {i}")
        continue
      elif len(nonzero[0]) == 2:
        logger.debug(f"Only 1 piece moved in state {i}")
        # 1 piece moved
        plane = nonzero[0][0]
        plane_encoding = plane % 14
        if plane_encoding < 7:
          colour = Colour.RED
        else:
          colour = Colour.BLACK
          plane_encoding %= 7

        src = None
        dest = None

        if current_state[plane][nonzero[1][0]][nonzero[2][0]] == 1:
          dest = Coord(int(nonzero[1][0]), int(nonzero[2][0]))
          src = Coord(int(nonzero[1][1]), int(nonzero[2][1]))
        else:
          dest = Coord(int(nonzero[1][1]), int(nonzero[2][1]))
          src = Coord(int(nonzero[1][0]), int(nonzero[2][0]))

        if not src or not dest:
          logger.error(f"Could not find src or dest for plane {plane_encoding}")
          continue

        board_move, state = instance.move(Move(src, dest))
        instance.add_history(board_move)
        logger.debug(f"Move: {board_move} | {state}")

      elif len(nonzero[0]) == 3:
        logger.debug(f"1 piece moved and 1 piece was eaten in state {i}")
        counts = {}

        for plane, x, y in zip(*nonzero):
          coord = (int(x), int(y))
          counts[coord] = counts.get(coord, 0) + 1

        src = Coord(*next(filter(lambda coord : counts[coord] == 1, counts)))
        dest = Coord(*next(filter(lambda coord : counts[coord] == 2, counts)))

        if not src or not dest:
          logger.error(f"Could not find src or dest for plane {plane_encoding}")
          continue

        board_move, state = instance.move(Move(src, dest))
        instance.add_history(board_move)
        logger.debug(f"Move: {board_move} | {state}")

      logger.debug(f"Current: {instance}")
      logger.debug(f"len(instance.moves): {len(instance.moves)}")

      for move in instance.moves:
        logger.debug(f"Move: {move}")

    return instance

  @classmethod
  def display_encoding(cls, encoding : np.ndarray):
    display_str = ""
    for i in range(0, len(encoding), 14):
      planes = encoding[i : i + 14]
      flattened = np.logical_xor.reduce(planes)
      display_str += f"State {i}:\n{flattened.reshape(*flattened.shape)}\n"

    return display_str

  @classmethod
  def flip_encoding(cls, encoding : np.ndarray):
    flipped_encoding = np.zeros(encoding.shape)

    for i in range(0, len(encoding), 14):
      planes = encoding[i : i + 14]
      flipped_planes = np.flip(planes, axis=2)
      flipped_encoding[i : i + 14] = flipped_planes

      red = flipped_planes[:7]
      black = flipped_planes[7:14]

      flipped_planes[:7] = black
      flipped_planes[7:14] = red

    return flipped_encoding

  def encode(self) -> np.ndarray:
    encoded_board = np.zeros((self.planes, self.n, self.m))

    for i in range(0, min(self.history_planes, len(self.moves) + 1)):
      for piece in self.pieces:
        colour_plane = COLOUR_MAPPING[piece.colour]
        piece_plane = PLANE_MAPPING[type(piece)]

        logger.debug(f"Piece: {piece} | Colour: {piece.colour} | Plane: {piece_plane + colour_plane + 14 * i} | Piece Plane: {piece_plane} | Colour Plane: {colour_plane} | i: {i}")

        encoded_board[piece_plane + colour_plane + 14 * i][piece.coord.x][piece.coord.y] = 1

      if len(self.moves) > 0:
        last_move = self.moves.pop()

        logger.debug(f"Last move: {last_move}")
        self.undo_move(last_move)

    logger.debug(f"Encoded board: {XiangqiBoard.display_encoding(encoded_board)}")

    return encoded_board.astype(bool)

  def setup(self, piece_coords : dict = DEFAULT_PIECE_COORDS):
    for piece_cls, coords in piece_coords.items():
      for colour, coords in coords.items():
        for coord in coords:
          piece = piece_cls(colour)
          self.add_piece(Coord(*coord), piece)

  def kings_exist(self):
    return self._red_king != None and self._black_king != None and self._red_king.coord != None and self._black_king.coord != None

  def is_check(self, colour : Colour, move : Move = None) -> bool:
    logger.debug(f"is_check({self}, {colour}, {move})")

    if move:
      move, _ = self.move(move)

    if not self.kings_exist():
      logger.error(f"Kings not on board: {self._red_king}, {self._black_king}")
      if move:
        self.undo_move(move)
      return True

    king = self._red_king if colour == Colour.RED else self._black_king
    oppositeColour = colour.opposite()

    # Check if the opposite colour's pieces can attack the king
    opponent_pieces = list(filter(lambda piece : piece.colour == oppositeColour, self.pieces))

    is_check = any(map(lambda piece : piece.is_legal_move(self, king.coord), opponent_pieces))
    if move:
      self.undo_move(move)

    logger.debug(f"is_check({colour}, {move}) -> {is_check}")
    return is_check

  def is_checkmate(self, colour : Colour):
    logger.debug(f"is_checkmate({self}, {colour})")
    return self.is_check(colour) and len(list(self.get_legal_moves(colour))) == 0

  def kings_facing(self, move : Move = None) -> bool:
    if move:
      move, _ = self.move(move)

    if not self.kings_exist():
      logger.error(f"Kings not on board: {self._red_king}, {self._black_king}")
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

  def get_piece(self, coord : Coord) -> XiangqiPiece:
    return self.get_cell(coord).piece or XiangqiPiece("..", Colour.NONE)

  def add_piece(self, coord : Coord, piece : XiangqiPiece):
    super().add_piece(coord, piece)

    if type(piece) == King:
      if piece.colour == Colour.RED:
        if self._red_king:
          logger.error(f"Red king already exists: {self._red_king}")
        self._red_king = piece
      else:
        if self._black_king:
          logger.error(f"Black king already exists: {self._black_king}")
        self._black_king = piece

  def threefold_repetition(self, move : Move) -> bool:
    logger.debug(f"threefold_repetition({move})")

    for dbg_move in self.moves:
      logger.debug(f"Move: {dbg_move}")
      # print(move)

    # Parse the previous board states
    # and check if the current board state has been seen before
    if (len(self.moves) < self.history_planes - 1):
      logger.debug(f"Not enough moves to check for threefold repetition | Len: {len(self.moves)}")
      return False

    prev_moves = deque()
    compare_move = move
    opponent_move = self.moves.pop()

    prev_moves.append(opponent_move)

    for i in range(0, (self.history_planes - 1) // 2):
      logger.debug(f"Compare move: {compare_move} | Opponent move: {opponent_move}")
      prev_move = self.moves.pop()
      prev_opponent_move = self.moves.pop()
      logger.debug(f"Prev move: {prev_move} | Prev opponent move: {prev_opponent_move}")

      prev_moves.append(prev_move)
      prev_moves.append(prev_opponent_move)

      if compare_move.opposite() != prev_move.move or opponent_move.move.opposite() != prev_opponent_move.move:
        logger.debug("Not a threefold repetition")

        self.moves.extend(reversed(prev_moves))
        return False

      compare_move = prev_move.move
      opponent_move = prev_opponent_move

    self.moves.extend(reversed(prev_moves))

    logger.debug(f"Threefold repetition: {move}")
    return True

  def is_legal_move(self, move : Move, colour : Colour) -> bool:
    logger.debug(f"is_legal_move({move}, {colour}, {self})")
    return self.is_valid_move(move) and \
      self.get_piece(move.src).colour == colour and \
      self.get_piece(move.dest).colour != colour and \
      not self.is_check(colour, move) and \
      not self.kings_facing(move) and \
      not self.threefold_repetition(move)

  def get_legal_moves(self, colour : Colour):
    logger.info(f"get_legal_moves({colour}, {self})")

    if not self.kings_exist():
      logger.error(f"Kings not on board: {self._red_king}, {self._black_king}")
      return []

    for piece in list(filter(lambda piece : piece.colour == colour, self.pieces)):
      logger.debug(f"{piece.display(piece)}")
      # logger.debug(f"{piece} moves:")
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