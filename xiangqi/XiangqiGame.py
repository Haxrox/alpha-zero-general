import sys
sys.path.append('..')
from Game import Game


class XiangqiGame(Game):
  def __init__(self, rows, cols):
    self.n = rows
    self.m = cols

  def getInitBoard(self):
    # return initial board (numpy board)
    b = Board(self.n, self.m)
    return b

  def getBoardSize(self):
    # (a,b) tuple
    return (self.n, self.m)

  def getActionSize(self):
    # return number of actions
    return self.n * self.m + 1

  def getValidMoves(self, board, player):
    # return a fixed size binary vector
    pass

  def getNextState(self, board, player, action):
    # if player takes action on board, return next (board,player)
    # action must be a valid move
    pass

  def getGameEnded(self, board, player):
    # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
    # player = 1
    pass

  def getCanonicalForm(self, board, player):
    # return state if player==1, else return -state if player==-1
    pass

  def getSymmetries(self, board, pi):
    # mirror, rotational
    pass

  def stringRepresentation(self, board):
    return board.__str__()

  def getScore(self, board, player):
    pass

  @staticmethod
  def display(board):
    return board.display(board)