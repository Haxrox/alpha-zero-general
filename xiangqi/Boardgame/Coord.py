class Coord():
  def __init__(self, x : int, y : int):
    self._x = x
    self._y = y

    assert type(x) == int, f"x: {x} | type(x): {type(x)}"
    assert type(y) == int, f"y: {y} | type(y): {type(y)}"

  @property
  def x(self):
    return self._x

  @x.setter
  def x(self, value : int):
    self._x = value

    assert type(self._x) == int, f"x: {self._x} | type(x): {type(self._x)}"

  @property
  def y(self):
    return self._y

  @y.setter
  def y(self, value : int):
    self._y = value

    assert type(self._y) == int, f"y: {self._y} | type(y): {type(self._y)}"

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  def __ne__(self, other):
    return self.x != other.x or self.y != other.y

  def __lt__(self, other):
    return self.x < other.x and self.y < other.y

  def __le__(self, other):
    return self.x <= other.x and self.y <= other.y

  def __gt__(self, other):
    return self.x > other.x and self.y > other.y

  def __ge__(self, other):
    return self.x >= other.x and self.y >= other.y

  def __add__(self, other):
    return Coord(self.x + other.x, self.y + other.y)

  def __sub__(self, other):
    return Coord(self.x - other.x, self.y - other.y)

  def __str__(self):
    return f"({self.x}, {self.y})"