import numpy as np

from xiangqi.Boardgame import Move, Coord

class RandomPlayer():
  def __init__(self, game):
    self.game = game

  def play(self, board):
    a = np.random.randint(self.game.getActionSize())
    valids = self.game.getValidMoves(board, 1)
    while valids[a]!=1:
      a = np.random.randint(self.game.getActionSize())

    print(f"Random player: {a}")
    print(f"Move: {self.game.actionToMove(a)}")

    return a

class HumanXiangqiPlayer():
  def __init__(self, game):
    self.game = game

  def play(self, board):
    # display(board)
    valid = self.game.getValidMoves(board, 1)
    # for i in range(len(valid)):
    #   if valid[i]:
    #     move = self.game.actionToMove(i)
    #     print(move)
        # print(f"[{move}", end="] ")

    while True:
      input_move = input()
      input_a = input_move.split(" ")
      if len(input_a) == 4:
        coords = list(map(int, input_a))
        # Convert to action
        move = Move(Coord(coords[0], coords[1]), Coord(coords[2], coords[3]))

        a = self.game.moveToAction(move)

        print(f"Move: {move}")
        print(f"Action: {a}")

        break
          # try:
          #   x,y = [int(i) for i in input_a]
          #   if ((0 <= x) and (x < self.game.n) and (0 <= y) and (y < self.game.n)) or \
          #         ((x == self.game.n) and (y == 0)):
          #     a = self.game.n * x + y if x != -1 else self.game.n ** 2
          #     if valid[a]:
          #         break
          # except ValueError:
          #   # Input needs to be an integer
          #   'Invalid integer'
      else:
        print('Invalid move')
    return a
