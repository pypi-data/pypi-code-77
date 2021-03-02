from guizero import Drawing
from Box2D import *
from .thing import *

class ebRectangle(ebThing):
    def __init__(self, box, *args, **kwargs):
        world  = box.world
        canvas = box.canvas

        # mémorisation de la box
        self.box   = box

        # paramètres enisebox
        self._visible   = kwargs.pop('visible', True)
        self._static    = kwargs.pop('static', False)

        # paramètres body
        angle           = kwargs.pop('angle', 0)

        # paramètres fixture
        dens            = kwargs.pop('density', 1)
        fric            = kwargs.pop('friction', 0)
        rest            = kwargs.pop('restitution', 0)

        if len(args)==4:
            x0, y0, x1, y1 = args

        width  = (x1-x0)/box._scale
        height = (y1-y0)/box._scale

        # body box2d
        if self._static:
            constructor = world.CreateStaticBody
        else:
            constructor = world.CreateDynamicBody
        x,y = (    min(x0,x1)/box._scale+width/2,
                            box._height-max(y0,y1)/box._scale+height/2  )
        body = constructor(
            position = (x,y),
            angle = angle,
        )
        body.CreatePolygonFixture(
            box=(width/2, height/2),
            # box=(width/2, height/2, (0,0), angle),
            density=dens,
            friction=fric,
            restitution=rest,
        )
        # on garde le lien
        self.body = body
        body.userData = self

        # item canvas
        if self._visible:
            shape  = body.fixtures[0].shape
            coords = [ body.transform * v for v in shape.vertices ]
            coords = [(c[0]*box._scale, (box._height - c[1])*box._scale) for c in coords]
            self.item = canvas.create_polygon(coords, **kwargs)
        else:
            self.item = None

    def update_item(self):
        if self._visible:
            box    = self.box
            body   = self.body
            canvas = box.canvas
            shape  = body.fixtures[0].shape
            coords = [ body.transform * v for v in shape.vertices ]
            new    = []
            for c in coords:
                new += [int(c[0]*box._scale), int((box._height - c[1])*box._scale)]
            canvas.coords(self.item, new)