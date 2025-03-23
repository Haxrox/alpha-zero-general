import sys
sys.path.append('..')
from Game import Game

from .XiangqiLogic import XiangqiBoard, COLOUR_MAPPING, PLANE_MAPPING
from .Xiangqi import Colour, Advisor, King, Elephant, Knight

from .Boardgame import Piece, Move, Coord
# Rook, Cannon, Pawn
# from Xiangqi import Colour, Rook, Advisor, King, Knight, Elephant, Cannon, Pawn

import numpy as np

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
    return (14, self.n, self.m)

  def getActionSize(self):
    # return number of actions
    # All combinations of moves for each piece
    # +1 for pass
    return self.n * self.m * self.n * self.m + 1
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
    # return a fixed size binary vector
    valids = [0]*self.getActionSize()
    # get all legal moves
    decoded_board = XiangqiBoard.from_encoding(board)
    legalMoves = list(decoded_board.get_legal_moves(player))
    # if no legal moves, pass
    if len(legalMoves) == 0:
      valids[-1] = 1
      return np.array(valids)

    # for each legal move, set the index to 1
    for move in legalMoves:
      move_index = (move.src.x * self.m + move.src.y) * self.n * self.m + (move.dest.x * self.m + move.dest.y)
      valids[move_index] = 1

    return valids

  def getNextState(self, board, player, action):
    # if player takes action on board, return next (board,player)
    # action must be a valid move
    if action == self.getActionSize() - 1:
      # Pass action
      return board, -player

    decoded_board = XiangqiBoard.from_encoding(board)

    # Decode action to get source and destination coordinates
    src_x = (action // (self.n * self.m)) // self.m
    src_y = (action // (self.n * self.m)) % self.m
    dest_x = (action % (self.n * self.m)) // self.m
    dest_y = (action % (self.n * self.m)) % self.m

    # Move the piece
    move = Move(Coord(src_x, src_y), Coord(dest_x, dest_y))
    decoded_board.move(move)

    # Encode the new board state
    new_board = decoded_board.encode()

    return new_board, -player

  def getGameEnded(self, board, player):
    # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
    # player = 1
    decoded_board = XiangqiBoard.from_encoding(board)
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
    return board
    if player == Colour.RED:
      return board
    else:
      decoded_board = XiangqiBoard.from_encoding(board)
      decoded_board.flip()
      return decoded_board.encode()

  def getSymmetries(self, board, pi):
    # mirror, rotational
    return [(board, pi)]

  def stringRepresentation(self, board):
    decoded_board = XiangqiBoard.from_encoding(board)
    return decoded_board.__str__()

  def getScore(self, board, player):
    pass

  @staticmethod
  def display(board):
    return board.display(board)

if __name__ == "__main__":
  game = XiangqiGame(9, 10)
  board = game.getInitBoard()
  print(board)

  decoded_board = XiangqiBoard.from_encoding(board)
  print(decoded_board)

  # decoded_board._red_king.display(decoded_board._red_king)
  # decoded_board._black_king.display(decoded_board._black_king)

  print("Red legal moves")
  red_legal_moves = decoded_board.get_legal_moves(Colour.RED)

  for move in red_legal_moves:
    print(move)

  print("Black legal moves")
  black_legal_moves = decoded_board.get_legal_moves(Colour.BLACK)
  for move in black_legal_moves:
    print(move)


  print(game.getBoardSize())
  print(game.getActionSize())
  print(game.getValidMoves(board, Colour.RED))

  canonical_board = game.getCanonicalForm(board, Colour.RED)

  print(canonical_board)
  # print(canonical_board[3])
  # print(canonical_board[4])
  # print(canonical_board[5])
  # print(canonical_board[4 + 7])
  # print(canonical_board[5 + 7])
  print(game.stringRepresentation(board))