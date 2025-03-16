class Piece():
  def __init__(self, name : str):
    self._name = name
    self._icon = f"{name[0].lower()}{name[1].upper()}"

  def __str__(self):
    return self._icon

  @property
  def name(self):
    return self._name

  @property
  def icon(self):
    return self._icon