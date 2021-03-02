from guizero import Drawing
from Box2D import *
from .thing import *

class ebCircle(ebThing):
    def __init__(self, box, x, y, r, **kwargs):
        world  = box.world
        canvas = box.canvas

        # mémorisation de la box
        self.box   = box

        # paramètres
        self._visible   = kwargs.pop('visible', True)
        self._static    = kwargs.pop('static', False)

        dens            = kwargs.pop('density', 1)
        fric            = kwargs.pop('friction', 0)
        rest            = kwargs.pop('restitution', 0)

        # body box2d
        if self._static:
            constructor = world.CreateStaticBody
        else:
            constructor = world.CreateDynamicBody
        body = constructor(position=(x/box._scale, box._height - y/box._scale))
        body.CreateCircleFixture(
            radius=r/box._scale,
            density=dens,
            friction=fric,
            restitution=rest,
        )
        # item canvas
        if self._visible:
            pos = body.position
            x = pos[0]*box._scale
            y = (box._height - pos[1])*box._scale
            r = body.fixtures[0].shape.radius*box._scale
            item = canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)
        else:
            item = None

        # on garde les liens vers ce qui vient d'être créé
        self.body  = body
        body.userData = self
        self.item  = item

    def update_item(self):
        if self._visible:
            box    = self.box
            body   = self.body
            canvas = box.canvas
            pos  = body.position
            x = pos[0]*box._scale
            y = (box._height - pos[1])*box._scale
            r = body.fixtures[0].shape.radius*box._scale
            canvas.coords(self.item, x - r, y - r, x + r, y + r)
