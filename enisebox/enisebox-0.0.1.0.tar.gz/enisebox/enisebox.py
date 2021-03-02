from guizero import App, Drawing
from PIL import Image, ImageTk
from Box2D import *
from random import randint

from .rectangle import ebRectangle
from .circle import ebCircle
from .image import ebImage

class enisebox():
    def __init__(self, canvas, *args, **kwargs):
        # paramètres pour le canvas
        canvas.update()
        self._scale     = kwargs.pop('scale', 20)
        self.canvas    = canvas
        self._width     = canvas.winfo_width()/self._scale
        self._height    = canvas.winfo_height()/self._scale
        # contactListener
        self._contact   = kwargs.pop('contact', None)
        if self._contact is not None:
            contactListener = ebContactListener(self._contact)
            kwargs['contactListener'] = contactListener
        # le monde box2d
        self.world     = b2World(**kwargs)

        # les objets du monde
        self.things   = []

    def create_rectangle(self, *args, **kwargs):
        obj = ebRectangle(self, *args, **kwargs)
        self.things.append(obj)
        return obj

    def create_circle(self, *args, **kwargs):
        obj = ebCircle(self, *args, **kwargs)
        self.things.append(obj)
        return obj

    def create_image(self, *args, **kwargs):
        obj = ebImage(self, *args, **kwargs)
        self.things.append(obj)
        return obj

    def itemconfigure(self, thing, **kwargs):
        item = thing.item
        self.canvas.itemconfigure(item, **kwargs)

    def Step(self, *args):
        self.world.Step(*args)
        for obj in self.things:
            obj.update_item()

    def CreateDistanceJoint(self, thingA, thingB, **kwargs):
        self.world.CreateDistanceJoint(
            bodyA=thingA.body,
            bodyB=thingB.body,
            **kwargs,
        )

    def CreateRopeJoint(self, thingA, thingB, **kwargs):
        self.world.CreateRopeJoint(
            bodyA=thingA.body,
            bodyB=thingB.body,
            **kwargs,
        )

    def CreateFrictionJoint(self, thingA, thingB, **kwargs):
        self.world.CreateFrictionJoint(
            bodyA=thingA.body,
            bodyB=thingB.body,
            **kwargs,
        )

    def CreateGearJoint(self, thingA, thingB, **kwargs):
        self.world.CreateGearJoint(
            bodyA=thingA.body,
            bodyB=thingB.body,
            **kwargs,
        )

    def CreateMouseJoint(self, thingA, thingB, **kwargs):
        self.world.CreateMouseJoint(
            bodyA=thingA.body,
            bodyB=thingB.body,
            **kwargs,
        )

    def CreatePrismaticJoint(self, thingA, thingB, **kwargs):
        self.world.CreatePrismaticJoint(
            bodyA=thingA.body,
            bodyB=thingB.body,
            **kwargs,
        )

    def CreatePulleyJoint(self, thingA, thingB, **kwargs):
        self.world.CreatePulleyJoint(
            bodyA=thingA.body,
            bodyB=thingB.body,
            **kwargs,
        )

    def CreateRevoluteJoint(self, thingA, thingB, **kwargs):
        self.world.CreateRevoluteJoint(
            bodyA=thingA.body,
            bodyB=thingB.body,
            **kwargs,
        )

    def CreateWheelJoint(self, thingA, thingB, **kwargs):
        self.world.CreateWheelJoint(
            bodyA=thingA.body,
            bodyB=thingB.body,
            **kwargs,
        )

    def CreateWeldJoint(self, thingA, thingB, **kwargs):
        self.world.CreateWeldJoint(
            bodyA=thingA.body,
            bodyB=thingB.body,
            **kwargs,
        )

    def DestroyThing(self, thing):
        self.canvas.delete(thing.item)
        self.world.DestroyBody(thing.body)
        thing.body = None

class ebContactListener(b2ContactListener):
    def __init__(self, contactManagement):
        b2ContactListener.__init__(self)
        self._contactManagement = contactManagement
    def BeginContact(self, contact):
        thingA = contact.fixtureA.body.userData
        thingB = contact.fixtureB.body.userData
        self._contactManagement(thingA, thingB, 'begin', contact)
    def EndContact(self, contact):
        thingA = contact.fixtureA.body.userData
        thingB = contact.fixtureB.body.userData
        self._contactManagement(thingA, thingB, 'end', contact)
    def PreSolve(self, contact, oldManifold):
        pass
    def PostSolve(self, contact, impulse):
        pass

