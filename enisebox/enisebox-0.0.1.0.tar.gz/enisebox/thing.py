from Box2D import *
from math import pi

class ebThing():
    def __init__(self, *args, **kwargs):
        pass

    def ApplyLinearImpulse(self, a, b):
        body = self.body
        body.ApplyLinearImpulse(
                impulse=b2Vec2(a,-b),
                point=body.position,
                wake=True,
        )

    def ApplyAngularImpulse(self, imp):
        body = self.body
        self.body.ApplyAngularImpulse(
                impulse=imp,
                wake=True,
        )

    @property
    def worldCenter(self):
        return self.body.worldCenter

    @property
    def position(self):
        return self.body.position

    @property
    def angle(self):
        # angle en radian
        return self.body.transform.angle

    @property
    def angularDamping(self):
        return self.body.angularDamping

    @angularDamping.setter
    def angularDamping(self, damping):
        self.body.angularDamping = damping
