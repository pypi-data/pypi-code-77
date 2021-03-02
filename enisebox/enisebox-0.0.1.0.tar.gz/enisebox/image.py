from guizero import Drawing
from PIL import Image, ImageTk
from Box2D import *
from .thing import *
from math import pi,sqrt
from time import time

class ebImage(ebThing):
    def __init__(self, box, x, y, width, height, **kwargs):
        world  = box.world
        canvas = box.canvas

        # mémorisation de la box
        self.box   = box

        # paramètres
        self._visible   = kwargs.pop('visible', True)
        self._static    = kwargs.pop('static', False)

        file            = kwargs.pop('image', None)

        angle           = kwargs.pop('angle', 0)
        dens            = kwargs.pop('density', 1)
        fric            = kwargs.pop('friction', 0)
        rest            = kwargs.pop('restitution', 0)

        # body box2d
        if self._static:
            constructor = world.CreateStaticBody
        else:
            constructor = world.CreateDynamicBody
        body = constructor(position = (x/box._scale, y/box._scale))
        body.CreatePolygonFixture(
            box=(width/box._scale/2, height/box._scale/2),
            density=dens,
            friction=fric,
            restitution=rest,
        )
        # item canvas
        if self._visible and file:
            # calcul des dimensions de l'image
            shape  = body.fixtures[0].shape
            coords = shape.vertices
            width,height = coords[2][0]-coords[0][0], coords[2][1]-coords[0][1]
            # lecture de l'image
            img = Image.open(file)
            w,h = img.size
            ratio = (width/w, height/h)
            side  = int(sqrt(w**2+h**2))
            # on étend l'image avec des pixels transparents
            # pour pouvoir la tourner sans perdre de pixels
            new = Image.new('RGBA', (side, side), (0, 0, 0, 0))
            new.paste(img,
                        (int((side-w)/2), int((side-h)/2)),
                        img.convert('RGBA'))
            img = new
            w,h = img.size
            # stockage de l'image
            self._ratio = ratio
            self._img = []
            t0 = time()
            for angle in range(360):
                # rotation
                new = img.rotate(angle)
                # redimensionnement
                new = new.resize(
                        (int(w*ratio[0]*box._scale),int(h*ratio[1]*box._scale)),
                        # Image.NEAREST,
                        # Image.BICUBIC,
                        Image.LANCZOS,
                )
                # stockage
                self._img.append(ImageTk.PhotoImage(new))
            print('{} : {}s'.format(file,
                            str(int(100*(time()-t0))/100))
                )
            # placement de l'image dans le Canvas
            pos  = body.position
            item = canvas.create_image(
                                pos[0]*box._scale,
                                (box._height - pos[1])*box._scale,
                                image=self._img[0]
                    )
        else:
            item   = None

        # on garde les liens
        self.body = body
        body.userData = self
        self.item = item

    def update_item(self):
        if self._visible:
            box    = self.box
            body   = self.body
            canvas = box.canvas
            pos    = body.position
            shape  = body.fixtures[0].shape
            angle  = int(body.transform.angle*180/pi)

            canvas.itemconfigure(self.item, image=self._img[angle])
            canvas.coords(self.item, pos[0]*box._scale, (box._height - pos[1])*box._scale)