class Piece():
  def __init__(self, name : str):
    self._name = name
    self._icon = f"{name[0].lower()}{name[1].upper()}"
    self._coord = None

  def __str__(self):
    return f"{self._icon} {self.coord}"

  @property
  def name(self):
    return self._name

  @property
  def icon(self):
    return self._icon

  @property
  def coord(self):
    return self._coord

  @coord.setter
  def coord(self, coord):
    self._coord = coord

  @staticmethod
  def display(piece):
    return f"{piece}"
