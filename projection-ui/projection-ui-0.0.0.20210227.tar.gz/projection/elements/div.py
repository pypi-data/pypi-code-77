from .base import Base


class Div(Base):
  _content = None
  _appended = False
  element = 'div'

  def __init__(self, content = None):
    super(Div, self).__init__()
    self._content = content

  @property
  def content(self):
    return self._content

  @content.setter
  def content(self, value: str) -> None:
    self._content = value
    if self._appended:
      self.update({'value': self._content})

  def render(self):
    self.inject({'value': self._content})
    self._appended = True


class Container(Base):
  _children = None
  _appended = False
  element = 'container'

  def __init__(self, row = None, column = None, height = 1, width = 1):
    super(Container, self).__init__()
    self._children = []
    self._positioning = [row, column, height, width]

  def append(self, element):
    self._children.append(element)
    if self._appended:
      element.attach(self.viewer, self)
      element.render()

  def render(self):
    self.inject({'position': self._positioning})
    if not self._appended:
      for child in self._children:
        child.attach(self.viewer, self)
        child.render()
    self._appended = True
