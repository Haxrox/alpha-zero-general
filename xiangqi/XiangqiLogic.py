from Boardgame import Board, Coord
from Xiangqi import King, Advisor, Colour

class XiangqiBoard(Board):
  def __init__(self):
    super().__init__(9, 10)
    self.setup()

  def setup(self):
    self._red_king = King(Colour.RED)
    self._black_king = King(Colour.BLACK)

    self.add_piece(Coord(4, 0), self._red_king)
    self.add_piece(Coord(4, 9), self._black_king)

    self.add_piece(Coord(3, 0), Advisor(Colour.RED))
    self.add_piece(Coord(5, 0), Advisor(Colour.RED))

    self.add_piece(Coord(3, 9), Advisor(Colour.BLACK))
    self.add_piece(Coord(5, 9), Advisor(Colour.BLACK))




if __name__ == "__main__":
  board = XiangqiBoard()
  print(board)