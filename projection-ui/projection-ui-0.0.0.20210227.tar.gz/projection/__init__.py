import os
import sys
import logging
import json
import importlib.resources

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.autoreload

from typing import Dict

import projection
from .externals.stdout import handler as stdout_handler


class statics(tornado.web.StaticFileHandler):
  pass

#        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'projection', 'static'),


class Websocket_handler(tornado.websocket.WebSocketHandler):
  def __init__(self, *args, **tkargs):
    super(Websocket_handler, self).__init__(*args)
    self.projection_app = tkargs["projection_app"]
    # print(f'{args=}')
    # print(f'{tkargs=}')

  @classmethod
  def unbound_repr(cls):
      return "<Websocket " + cls.__module__.split('.')[-1] + "." + cls.__name__ + ">"

  def open(self):
    self.projection_app.viewer(self.projection_app, self)


class Projection(object):
  def __init__(self, viewer, port = 8086, tornado_opts = None):
    super(Projection, self).__init__()
    self.viewer = viewer
    self.port = port
    if not tornado_opts:
      tornado_opts = {
          "xsrf_cookies": False,
          "debug": True,
          "xheaders": False,
          "cookie_secret": ""
      }
    self.tornado_opts = tornado_opts

    self.routes = []
    with importlib.resources.path(projection, 'static') as irp:
      self.routes.append(
          tornado.web.URLSpec("/()", statics, {
              "path": irp,
              "default_filename": "index.html"
          }))
      self.routes.append(
          tornado.web.URLSpec("/projection/(.*)", statics, {
              "path": irp,
              "default_filename": "index.html"
          }))

    self.routes.append(tornado.web.URLSpec(
        "/websocket", Websocket_handler, {
            "projection_app": self
        }))

    self.logger = logger = logging.getLogger('projection.main')
    logger.setLevel(logging.DEBUG)
    self.log_sh = sh = stdout_handler("projection")
    logging.getLogger('').addHandler(sh)
    logging.getLogger('').setLevel(logging.INFO)

  def start(self):
    ta = tornado.web.Application(self.routes, **self.tornado_opts)
    ta.listen(self.port, xheaders=self.tornado_opts.get("xheaders"))
    self.tornado_application = ta
    ta.settings['static_path'] = ''
    # print(f'{self.routes=}')
    tornado.ioloop.IOLoop.instance().start()


class Viewer(object):
  def __init__(self, application, websocket):
    self.application = application
    self.websocket = websocket
    self._title = None
    self._children = []
    self.write_payload({'type': 'update', 'id': 0, 'data': {'id': id(self)}})

  def write_payload(self, payload: Dict) -> None:
    self.websocket.write_message(json.dumps(payload))

  @property
  def title(self):
    return self._title

  @title.setter
  def title(self, title: str) -> None:
    self._title = title
    self.write_payload({'type': 'update', 'id': id(self), 'data': {'title': title}})

  def append(self, element):
    element.attach(self, self)
    self._children.append(element)
    element.render()
