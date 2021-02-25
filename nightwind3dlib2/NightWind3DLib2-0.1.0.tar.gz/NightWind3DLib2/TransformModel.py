from panda3d.core import *
pickerRay = CollisionRay()


def model_position(model):
    if base.mouseWatcherNode.hasMouse():
        mpos = base.mouseWatcherNode.getMouse()
        pickerRay.setFromLens(base.camNode, mpos)
        nearPoint = render.getRelativePoint(base.cam, pickerRay.getOrigin())
        nearVec = render.getRelativeVector(base.cam, pickerRay.getDirection())
        model.setPos(nearPoint + nearVec *((110 - nearPoint.getZ()) / nearVec.getZ()))
