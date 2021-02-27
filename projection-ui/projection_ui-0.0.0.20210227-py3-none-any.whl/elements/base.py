
class Base(object):
  _border = None
  viewer = None
  parent = None

  def attach(self, viewer, parent):
    self.viewer = viewer
    self.parent = parent

  def inject(self, data):
    payload = {
        'type': 'inject', 'element': self.element,
        'data': {'id': id(self), 'parent': id(self.parent)}
    }
    payload['data'].update(data)
    self.viewer.write_payload(payload)
    if self._border:
      self.update({'border': self._border})

  def update(self, data):
    payload = {'type': 'update', 'id': id(self), 'data': data}
    self.viewer.write_payload(payload)

  @property
  def border(self):
    return self._border

  @border.setter
  def border(self, value: str) -> None:
    self._border = value
    if self.viewer:
      self.update({'border': self._border})
