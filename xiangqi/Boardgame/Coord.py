class Coord():
  def __init__(self, x : int, y : int):
    self._x = x
    self._y = y

  @property
  def x(self):
    return self._x

  @x.setter
  def x(self, value : int):
    self._x = value

  @property
  def y(self):
    return self._y

  @y.setter
  def y(self, value : int):
    self._y = value

  def __str__(self):
    return f"({self.x}, {self.y})"