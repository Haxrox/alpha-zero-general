import random
import sys
import logging
sys.path.append('..')
from Game import Game

from .XiangqiLogic import XiangqiBoard, COLOUR_MAPPING, PLANE_MAPPING
from .Xiangqi import Colour, Advisor, King, Elephant, Knight, Rook, Cannon, Soldier

from .Boardgame import Piece, Move, Coord
# from Xiangqi import Colour, Rook, Advisor, King, Knight, Elephant, Cannon, Pawn

import numpy as np

logger = logging.getLogger(__name__)

class XiangqiGame(Game):
  def __init__(self, rows, cols):
    self.n = rows
    self.m = cols

  def getInitBoard(self):
    # return initial board (numpy board)
    b = XiangqiBoard(self.n, self.m)
    b.setup()
    return b.encode()

  def getBoardSize(self):
    # (a,b) tuple
    return (14 * 6, self.n, self.m)

  def getActionSize(self):
    # return number of actions
    # All combinations of moves for each piece
    # +1 for pass
    D1 = self.n # + 1
    D2 = self.m # + 1
    D3 = self.n # + 1
    D4 = self.m # + 1

    return D1 * D2 * D3 * D4 + 1
    # Rooks: self.n + self.m moves (self.n vertical squares, self.m horizontal squares)
    # Knights: 8 moves
    # Elephants: 4 moves
    # Advisors: 4 moves
    # General: 4 moves
    # Cannons: self.n + self.m moves (same as rook)
    # Soldiers: 3 moves (forward, left, right)

    ROOK_MOVES = self.n + self.m
    ROOK_COUNT = 2
    KNIGHT_MOVES = 8
    KNIGHT_COUNT = 2
    ELEPHANT_MOVES = 4
    ELEPHANT_COUNT = 2
    ADVISOR_MOVES = 4
    ADVISOR_COUNT = 2
    GENERAL_MOVES = 4
    GENERAL_COUNT = 1
    CANNON_MOVES = self.n + self.m
    CANNON_COUNT = 2
    SOLDIER_MOVES = 3
    SOLDIER_COUNT = 5

    # +1 for number of legal moves
    return  ROOK_MOVES * ROOK_COUNT + \
            KNIGHT_MOVES * KNIGHT_COUNT + \
            ELEPHANT_MOVES * ELEPHANT_COUNT + \
            ADVISOR_MOVES * ADVISOR_COUNT + \
            GENERAL_MOVES * GENERAL_COUNT + \
            CANNON_MOVES * CANNON_COUNT + \
            SOLDIER_MOVES * SOLDIER_COUNT + 1

  def getValidMoves(self, board, player):
    logger.debug(f"getValidMoves({board}, {player})")
    # return a fixed size binary vector
    valids = [0]*self.getActionSize()
    # get all legal moves
    decoded_board = XiangqiBoard.from_encoding(board)
    legalMoves = list(decoded_board.get_legal_moves(Colour.to_colour(player)))

    logger.info(f"getValidMoves({decoded_board}, {Colour.to_colour(player)})")
    logger.info(f"Legal Moves:")
    for move in legalMoves:
      logger.info(f"{move}")

    # if no legal moves, pass
    if len(legalMoves) == 0:
      valids[-1] = 1
      return np.array(valids)

    # for each legal move, set the index to 1
    for move in legalMoves:
      move_index = self.moveToAction(move)
      # move_index = (move.src.x * self.m + move.src.y) * self.n * self.m + (move.dest.x * self.m + move.dest.y)
      valids[move_index] = 1

    logger.debug(f"Valids: {valids}")
    return np.array(valids)

  def moveToAction(self, move):
    # Encode move to get source and destination coordinates
    # https://stackoverflow.com/questions/29142417/4d-position-from-1d-index
    D1 = self.n # + 1
    D2 = self.m # + 1
    D3 = self.n # + 1
    D4 = self.m # + 1

    src_x = move.src.x
    src_y = move.src.y
    dest_x = move.dest.x
    dest_y = move.dest.y
    action = src_x + src_y * D1 + dest_x * D1 * D2 + dest_y * D1 * D2 * D3

    logger.debug(f"moveToAction({move}) -> {action}")
    # print(f"moveToAction({move}) -> {action}")

    return action

  def actionToMove(self, action):
    # Decode action to get source and destination coordinates
    # https://stackoverflow.com/questions/29142417/4d-position-from-1d-index
    D1 = self.n # + 1
    D2 = self.m # + 1
    D3 = self.n # + 1
    D4 = self.m # + 1

    src_x = action % D1
    src_y = ((action - src_x) // D1) % D2
    dest_x = ((action - src_y * D1 - src_x) // (D1 * D2)) % D3
    dest_y = ((action - dest_x * D1 * D2 - src_y * D1 - src_x) // (D1 * D2 * D3)) % D4
    logger.debug(f"actionToMove({action}) -> src: ({src_x}, {src_y}), dest: ({dest_x}, {dest_y})")
    # print(f"actionToMove({action}) -> src: ({src_x}, {src_y}), dest: ({dest_x}, {dest_y})")

    return Move(Coord(int(src_x), int(src_y)), Coord(int(dest_x), int(dest_y)))

  def getNextState(self, board, player, action):
    # if player takes action on board, return next (board,player)
    # action must be a valid move
    if action == self.getActionSize() - 1:
      # Pass action
      return (board, -player)

    decoded_board = XiangqiBoard.from_encoding(board)
    logger.info(f"getNextState({decoded_board}, {Colour.to_colour(player)}, {action})")

    # Move the piece
    move = self.actionToMove(action)
    board_move, _ = decoded_board.move(move)
    decoded_board.add_history(board_move)
    logger.info(f"Move: {move}")
    logger.info(f"Next state: {decoded_board}")

    decoded_board.flip()
    logger.info(f"Flipped board: {decoded_board}")

    # Encode the new board state
    new_board = decoded_board.encode()

    return (new_board, -player)

  def getGameEnded(self, board, player):
    logger.info(f"getGameEnded({board}, {player})")
    # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
    # player = 1
    decoded_board = XiangqiBoard.from_encoding(board)
    # return random.randint(0, 500) > 100
    if decoded_board.is_checkmate(Colour.to_colour(player)):
      return -1
    elif decoded_board.is_checkmate(Colour.to_colour(player).opposite()):
      return 1
    else:
      return 0

  def getCanonicalForm(self, board, player):
    # return state if player==1, else return -state if player==-1
    # 7 boards, 1 for each piece
    #   Rook, Knight, Elephant, Advisor, General, Cannon, Soldier
    # *3 for 3 fold repeitiion
    # *2 for both sides
    # +1 for we are red
    # +1 for assistance
    # 3d matrix of size 7x3x2
    logger.info(f"getCanonicalForm(board, {Colour.to_colour(player)})")
    if Colour.to_colour(player) == Colour.RED:
      logger.debug(f"Red player")

      decoded_board = XiangqiBoard.from_encoding(board)
      logger.info(f"Decoded board: {decoded_board}")
      return board
    else:
      logger.info(f"Black player. Inverting colours...")

      decoded_board = XiangqiBoard.from_encoding(board)

      # decoded_board.flip()

      for piece in decoded_board.pieces:
        piece.colour = piece.colour.opposite()

      return decoded_board.encode()

  def getSymmetries(self, board, pi):
    # mirror, rotational
    return [(board, pi)]

  def stringRepresentation(self, board):
    # return board.tostring()
    decoded_board = XiangqiBoard.from_encoding(board)
    return decoded_board.stringRepresentation()

  def getScore(self, board, player):
    pass

  @staticmethod
  def display(board):
    logger.debug(f"display({board})")

    return XiangqiBoard.display_encoding(board)

def main():
  game = XiangqiGame(9, 10)
  board = game.getInitBoard()
  logger.info(game.display(board))

  decoded_board = XiangqiBoard.from_encoding(board)
  logger.info(decoded_board)
  for piece in decoded_board.pieces:
    piece.display(piece)

  assert len(decoded_board.pieces) == 32, f"Pieces: {len(decoded_board.pieces)}"

  logger.info("Kings:")
  decoded_board._red_king.display(decoded_board._red_king)
  decoded_board._black_king.display(decoded_board._black_king)

  logger.info("Red pieces:")
  red_pieces = list(filter(lambda piece: piece.colour == Colour.RED, decoded_board.pieces))
  for piece in red_pieces:
    logger.info(piece.display(piece))

  assert len(red_pieces) == 16, f"Red pieces: {len(red_pieces)}"

  logger.info("Red legal moves")
  red_legal_moves = list(decoded_board.get_legal_moves(Colour.RED))

  for move in red_legal_moves:
    logger.info(move)

  # Rook moves: 2
  # Knight moves: 2
  # Elephant moves: 2
  # Advisor moves: 1
  # General moves: 1
  # Cannon moves: 12
  # Soldier moves: 1
  assert len(red_legal_moves) == 2 * 2 + 2 * 2 + 2 * 2 + 1 * 2 + 1 * 1 + 12 * 2 + 1 * 5, f"Red legal moves: {len(red_legal_moves)}"

  logger.info("Black pieces:")
  black_pieces = list(filter(lambda piece: piece.colour == Colour.BLACK, decoded_board.pieces))
  for piece in black_pieces:
    logger.info(piece.display(piece))

  assert len(black_pieces) == 16, f"Black pieces: {len(black_pieces)}"

  logger.info("Black legal moves")
  black_legal_moves = list(decoded_board.get_legal_moves(Colour.BLACK))
  for move in black_legal_moves:
    logger.info(move)

  assert len(black_legal_moves) == 2 * 2 + 2 * 2 + 2 * 2 + 1 * 2 + 1 * 1 + 12 * 2 + 1 * 5, f"Black legal moves: {len(black_legal_moves)}"

  logger.info("Pieces:")
  for piece in decoded_board.pieces:
    logger.info(piece.display(piece))

  logger.info(game.getBoardSize())
  logger.info(game.getActionSize())
  logger.info(game.getValidMoves(board, Colour.RED.value))

  canonical_board = game.getCanonicalForm(board, Colour.RED.value)
  logger.info(f"Red Canonical_board:\n{XiangqiBoard.from_encoding(canonical_board)}")

  canonical_board = game.getCanonicalForm(board, Colour.BLACK.value)
  logger.info(f"Black Canonical_board:\n{XiangqiBoard.from_encoding(canonical_board)}")

  red_valid_moves = game.getValidMoves(board, Colour.RED.value)
  logger.info(red_valid_moves)
  action = red_valid_moves[np.random.choice(np.where(red_valid_moves == 1)[0])]
  logger.info(f"Action: {action} | Move: {game.actionToMove(action)}")
  next_board, next_player = game.getNextState(board, Colour.RED.value, action)

  canonical_board = game.getCanonicalForm(next_board, Colour.RED.value)
  logger.info(f"Red Canonical_board:\n{XiangqiBoard.from_encoding(canonical_board)}")

  canonical_board = game.getCanonicalForm(next_board, Colour.BLACK.value)
  logger.info(f"Black Canonical_board:\n{XiangqiBoard.from_encoding(canonical_board)}")

  next_decoded_board = XiangqiBoard.from_encoding(next_board)
  logger.info(f"Next board:\n{next_decoded_board}")

  cannon = next_decoded_board.get_piece(Coord(1, 2))
  assert cannon is not None
  assert type(cannon) == Cannon
  assert cannon.colour == Colour.BLACK # Rotated board

  logger.info(f"{cannon} Moves:")
  cannon_moves = list(cannon.get_moves(next_decoded_board))
  for move in cannon_moves:
    logger.info(move)
  assert len(cannon_moves) == 12

  rook = next_decoded_board.get_piece(Coord(0, 0))
  assert rook is not None
  assert type(rook) == Rook
  assert rook.colour == Colour.BLACK # Rotated board

  logger.info(f"{rook} Moves:")
  rook_moves = list(rook.get_moves(next_decoded_board))
  for move in rook_moves:
    logger.info(move)
  assert len(rook_moves) == 2

  # logger.info(canonical_board[3])
  # logger.info(canonical_board[4])
  # logger.info(canonical_board[5])
  # logger.info(canonical_board[4 + 7])
  # logger.info(canonical_board[5 + 7])
  # logger.info(f"String representation:\n{game.stringRepresentation(board)}")

if __name__ == "__main__":
  main()