import subprocess
import os
import math
import threading
from ... import tree
from ... import solid
from ... import shape
from ... import scene
from ... import transform
from ... import boolean
from ... import material
from .. import textwriter
from .. import downsample
from .. import cmath
from .. import matrix
from ...algorithms import reducegroups




# WARNING: PovRay swaps X/Z dimensions compared to OpenScad - this is the reason, we are swapping it back here.
# Also rotations are in reverse direction.




# Can be replaced with an absolute path to the povray executable
PovRayExecutable = "povray"




# Constant for generating distances
LargeEpsilon = 0.1




# TODO: move bezier type to other class
class PovSolidPrism(tree.Node):
    """
    Prism rendering primitive for PovRay.
    """
    # TODO: smoothing
    def __init__(self,
                    polygon,
                    height,
                    centerOffset = 0,
                    name: str = "",
                    attributes: dict = None
        ):
        super().__init__(name = name, attributes = attributes)
        self.polygon = polygon
        self.height = height
        self.centerOffset = centerOffset

        if isinstance (polygon, shape.Polygon):
            type_ = "linear_spline"
        elif isinstance (polygon, shape.QuadraticSpline):
            type_ = "quadratic_spline"
        elif isinstance (polygon, shape.CubicSpline):
            type_ = "cubic_spline"
        elif isinstance (polygon, shape.BezierSpline):
            type_ = "bezier_spline"
        else:
            assert False, "unexpected shape type"
        
        #: interpolation type
        self.type_ = type_



class _PovRayLinearExtrudeRewriter(tree.Visitor):
    """
    Iterate a tree, find all linear extrusions and replace them...
    """
    def __init__(self):
        super().__init__()
        self._rule (tree.Generator, self.enterGenerator)
        self._rule (solid.LinearExtrude, self.enterExtrusion, self.leaveExtrusion)
        self._rule (shape.Circle, self.enterCircle)
        self._rule (shape.Square, self.enterSquare)
        self._rule (shape.Polygon, self.enterPolygon)
        self._rule (shape.QuadraticSpline, self.enterPolygon)
        self._rule (shape.CubicSpline, self.enterPolygon)
        self._rule (shape.BezierSpline, self.enterPolygon)
        self._rule (shape.PolarShape, self.enterPolarShape, self.leaveTransformedShape)
        self._rule (transform.Translate, self.enterTransform, self.leaveTransform)
        self._rule (transform.Rotate, self.enterTransform, self.leaveTransform)
        self._rule (transform.Scale, self.enterTransform, self.leaveTransform)


    def execute(self, node, defaultAttributes):
        ctx = tree.VisitorContext (defaultAttributes)
        ctx.extrusionData = None
        return self.visit (node, ctx)


    def _enterDefault(self, node, ctx):
        """
        Enter default node type.
        """
        assert (ctx.extrusionData == None), "found unhandled type in extrusion"
        return True


    def enterGenerator(self, node, ctx):
        self.visit (node.generate (ctx.getResolvedAttributes ()), ctx)


    def enterCircle(self, node, ctx):
        """
        Enter a circle.
        """
        if ctx.extrusionData == None:
            return True

        height=ctx.extrusionData["extrudeRoot"].evaluate ("height", ctx.getResolvedAttributes ())
        radius=node.evaluate ("radius", ctx.getResolvedAttributes ())
        mergedAttributs=node.attributes
        ctx.extrusionData["generated"] = self.applyTransformStack (solid.Cylinder (height=height, radius=radius, attributes=mergedAttributs), ctx)
        return False


    def enterSquare(self, node, ctx):
        """
        Enter a square.
        """
        if ctx.extrusionData == None:
            return True

        height=ctx.extrusionData["extrudeRoot"].evaluate ("height", ctx.getResolvedAttributes ())
        size=node.evaluate ("size", ctx.getResolvedAttributes ())
        mergedAttributs=node.attributes
        ctx.extrusionData["generated"] = self.applyTransformStack (solid.Cube ([size[0], size[1], height], attributes=mergedAttributs), ctx)
        return False


    def enterPolygon(self, node, ctx):
        """
        Enter a polygon.
        """
        if ctx.extrusionData == None:
            return True
        mergedAttributs=node.attributes
        height=ctx.extrusionData["extrudeRoot"].evaluate ("height", ctx.getResolvedAttributes ())
        ctx.extrusionData["generated"] = self.applyTransformStack (PovSolidPrism (node, height, attributes=mergedAttributs), ctx)
        return False


    # TODO: Need this? Generate class should do the magic here.
    def enterPolarShape(self, node, ctx):
        """
        Enter a polar shape, transform to a simple shape and re-run on visitor (self)
        """
        transformed = node.toQuadraticSpline (ctx.getResolvedAttributes ())
        if transformed == None:
            transformed = node.toCubicSpline (ctx.getResolvedAttributes ())
        if transformed == None:
            transformed = node.toPolygon (ctx.getResolvedAttributes ())
        assert transformed != None, "can not transform to a simple shape geometry"
        self.visit (transformed, ctx)
        return False


    def leaveTransformedShape(self, node, ctx):
        """
        Leave transformed shape.
        """
        return node


    def applyTransformStack(self, node, ctx):
        """
        Apply transform stack to newly created node (2D -> 3D)
        """
        transformStack = ctx.extrusionData["transformStack"]
        newNode = node
        for index in range (len (transformStack) - 1, -1, -1):
            t = transformStack[index]
            if isinstance (t, transform.Translate):
                tv = t.evaluate ("vector", ctx.getResolvedAttributes ())
                x = tv[0]
                y = tv[1]
                newNode = transform.Translate (newNode, [x, y, 0])
            elif isinstance (t, transform.Rotate):
                tv = t.evaluate ("vector", ctx.getResolvedAttributes ())
                x = tv[0]
                newNode = transform.Rotate (newNode, [0, 0, x])
            elif isinstance (t, transform.Scale):
                tv = t.evaluate ("vector", ctx.getResolvedAttributes ())
                x = tv[0]
                y = tv[1]
                newNode = transform.Scale (newNode, [x, y, 1])
            else:
                assert False, "transformation type not handled."
        return newNode


    def enterTransform(self, node, ctx):
        """
        Enter a transformation.
        """
        if ctx.extrusionData == None:
            return True

        ctx.extrusionData["transformStack"].append (node)
        return True


    def leaveTransform(self, node, ctx):
        """
        Leave a transformation.
        """
        return node


    def enterExtrusion(self, node, ctx):
        """
        Enter extrusion.
        """
        assert ctx.extrusionData == None, "found extrusion in extrusion."
        twist = node.parameter ("twist")
        if twist in (None, 0):
            ctx.extrusionData = {
                "extrudeRoot": node,
                "transformStack": [],
                "generated": None
            }
            return True
        else:
            attrs = ctx.getResolvedAttributes ()
            poly = node.asPolyhedron (attrs)
            assert poly != None, "can not convert twisted linear extrusion in polyhedron"
            # TODO: smoothing
            smoothing = False if not 'smoothing' in attrs else attrs['smoothing']
            if smoothing:
                smoothingAngle = tree.DefaultAttributes['smoothing.thresholdAngle'] if not 'smoothing.thresholdAngle' in attrs else attrs['smoothing.thresholdAngle']
                poly = poly.optimize ().smoothEdgeNormals (angleThreshold = smoothingAngle)
            ctx.extrusionData = {
                "extrudeRoot": node,
                "transformStack": [],
                "generated": poly
            }
            return False


    def leaveExtrusion(self, node, ctx):
        """
        Leave extrusion.
        """
        newItem = ctx.extrusionData["generated"]
        ctx.extrusionData = None
        return newItem

PovRayLinearExtrudeRewriter = _PovRayLinearExtrudeRewriter()






class PovSolidExtrudedTorus(tree.Tree):
    """
    Torus rendering primitive for PovRay.
    """
    # TODO: smoothing
    def __init__(self,
                    points,
                    angle,
                    transform,
                    type_: str = "linear_spline",
                    name: str = "",
                    attributes: dict = None
        ):
        super().__init__(name = name, attributes = attributes)
        self.points = points
        self.angle = angle
        self.transform = transform
        self.type_ = type_
        self.applyTransform ()
        self.calculateBoundingBox ()

    
    def applyTransform(self):
        """
        Applies the affinite transform to all control points.
        """
        for i in range(0, len (self.points)):
            self.points[i] = matrix.transformPoint2D (self.transform, self.points[i])


    def calculateBoundingBox(self):
        """
        Calculates the bounding of a rotate extrude object.
        """
        # calculate bounding box as cylinder around rotated shape.
        radius = 0
        heightMin = None
        heightMax = None
        for p in self.points:
            if p[0] < 0:
                if radius < -p[0]:
                    radius = -p[0]
            else:
                if radius < p[0]:
                    radius = p[0]
            if heightMin == None:
                heightMin = p[1]
            elif heightMin > p[1]:
                heightMin = p[1]
            if heightMax == None:
                heightMax = p[1]
            elif heightMax < p[1]:
                heightMax = p[1]
        self.bbHeightMin = heightMin if heightMin != None else 0
        self.bbHeightMax = heightMax if heightMax != None else 0
        self.bbRadius = radius





# TODO: move to cmath
def warpAngle(angle):
    """
    Return angle in range 0..360
    """
    # TODO: optimize, remove loop on negative angles
    while (angle < 0):
        angle = angle + 360.0
    return angle % 360.0



def createRotateAngleLimiter(rotShape, se, sa = None, inverse = False):
    """
    Create angle limiter for rotation extrude. 
    """
    # calculate angles and apply defaults
    if sa == None:
        sa = 0

    # clamp angles and swap if required
    se = warpAngle (se)
    sa = warpAngle (sa)
    if se < sa:
        t = sa
        sa = se
        se = t

    # get geometry of bouding box
    sr = math.sqrt (rotShape.bbRadius * rotShape.bbRadius) + LargeEpsilon
    h1 = rotShape.bbHeightMin
    h2 = rotShape.bbHeightMax

    # quadrant control points (counter clock wise)
    qccw = [
            [sr, 0],
            [sr, sr],
            [0, sr],
            [-sr, sr],
            [-sr, 0],
            [-sr, -sr],
            [0, -sr],
            [sr, -sr],
            [sr, 0],
            [sr, 0]
        ]

    # quadrant control points (clock wise)
    qcw = [
            [sr, 0],
            [sr, -sr],
            [0, -sr],
            [-sr, -sr],
            [-sr, 0],
            [-sr, sr],
            [0, sr],
            [sr, sr],
            [sr, 0],
            [sr, 0]
        ]

    # select quadrant control points
    q = qccw if inverse == False else qcw

    # calculate control point on quadrant
    cp = lambda angle, cp1, cp2: [
            (cp2[0] * math.tan (angle * math.pi / 180)) + (cp1[0] * (1 - math.tan (angle * math.pi / 180))),
            (cp2[1] * math.tan (angle * math.pi / 180)) + (cp1[1] * (1 - math.tan (angle * math.pi / 180)))
        ]

    # get quadrant of first sa, se
    saq = int (math.floor (sa / 45.0))
    seq = int (math.floor (se / 45.0))
    sar = sa - (saq * 45)
    ser = se - (seq * 45)

    # calculate points for polygon
    points = [[0, 0]]
    points.append (cp (sar, q[saq], q[saq + 1]))
    for qi in range (saq, seq):
        points.append (q[qi + 1])
    points.append (cp (ser, q[seq], q[seq + 1]))

    # calculate prism
    h = (2 * LargeEpsilon) + h2 - h1
    ch = (h1 + h2) / 2
    return PovSolidPrism (shape.Polygon (points), h, centerOffset = ch)





class _PovRayRotateExtrudeRewriter(tree.Visitor):
    """
    Iterate a tree, find all rotatory extrusions and replace them...
    """
    #special case: normal torus if circle and not scaled / rotated (decide rules)
    def __init__(self):
        super().__init__()
        self._rule (solid.RotateExtrude, self.enterExtrusion, self.leaveExtrusion)
        self._rule (shape.Circle, self.enterCircle)
        self._rule (shape.Square, self.enterSquare)
        self._rule (shape.Polygon, self.enterPolygon)
        self._rule (shape.QuadraticSpline, self.enterPolygon)
        self._rule (shape.CubicSpline, self.enterPolygon)
        self._rule (shape.BezierSpline, self.enterPolygon)
        self._rule (shape.PolarShape, self.enterPolarShape, self.leaveTransformedShape)
        self._rule (transform.Translate, self.enterTransform, self.leaveTransform)
        self._rule (transform.Rotate, self.enterTransform, self.leaveTransform)
        self._rule (transform.Scale, self.enterTransform, self.leaveTransform)


    def execute(self, node, defaultAttributes):
        ctx = tree.VisitorContext (defaultAttributes)
        ctx.extrusionData = None
        return self.visit (node, ctx)


    def _enterDefault(self, node, ctx):
        """
        Enter default node type.
        """
        assert (ctx.extrusionData == None), "found unhandled type in extrusion"
        return True


    def enterSquare(self, node, ctx):
        """
        Enter a square.
        """
        if ctx.extrusionData == None:
            return True

        angle=ctx.extrusionData["extrudeRoot"].evaluate ("angle", ctx.getResolvedAttributes ())
        size=node.evaluate ("size", ctx.getResolvedAttributes ())
        mergedAttributs=node.attributes
        sx = size[0] / 2.0
        sy = size[1] / 2.0
        points = [
            [-sx, -sy],
            [sx, -sy],
            [sx, sy],
            [-sx, sy]
        ]
        transform = self.createTransformFromStack (ctx)
        newItem = PovSolidExtrudedTorus (points, angle, transform, attributes=mergedAttributs)
        ctx.extrusionData["generated"] = self.limitExtrusionAngle (newItem, angle, ctx)
        return False


    def enterCircle(self, node, ctx):
        """
        Enter a circle.
        """
        # control point for center of quadrant of circle        
        c = 0.55191502449

        # split cirlcle into 4 quadrants of qubic bezier curves
        qbPoints = [
            [0, 1],
            [c, 1],
            [1, c],
            [1, 0],
            [1, 0],
            [1, -c],
            [c, -1],
            [0, -1],
            [0, -1],
            [-c, -1],
            [-1 , -c],
            [-1, 0],
            [-1, 0],
            [-1, c],
            [-c, 1],
            [0, 1]
        ]

        # apply own size as scale to transform stack
        radius=node.evaluate ("radius", ctx.getResolvedAttributes ())
        ctx.extrusionData["transformStack"].append (transform.Scale (vector = [radius, radius]))
        gt = self.createTransformFromStack (ctx)
        ctx.extrusionData["transformStack"].pop ()
        angle=ctx.extrusionData["extrudeRoot"].evaluate ("angle", ctx.getResolvedAttributes ())
        mergedAttributs=node.attributes
        newItem = PovSolidExtrudedTorus (qbPoints, angle, gt, type = "bezier_spline", attributes=mergedAttributs)
        ctx.extrusionData["generated"] = self.limitExtrusionAngle (newItem, angle, ctx)
        return False


    def enterPolygon(self, node, ctx):
        """
        Enter a polygon.
        """
        if ctx.extrusionData == None:
            return True
        angle=ctx.extrusionData["extrudeRoot"].evaluate ("angle", ctx.getResolvedAttributes ())
        points=node.getData ()
        mergedAttributs=node.attributes
        transform = self.createTransformFromStack (ctx)
        if isinstance (node, shape.QuadraticSpline):
            type_ = "quadratic_spline"
        elif isinstance (node, shape.CubicSpline):
            type_ = "cubic_spline"
        elif isinstance (node, shape.BezierSpline):
            type_ = "bezier_spline"
        elif isinstance (node, shape.Polygon):
            type_ = "linear_spline"
        else:
            assert False, "unexpected shape type"
        newItem = PovSolidExtrudedTorus (points, angle, transform, attributes=mergedAttributs, type_=type_)
        ctx.extrusionData["generated"] = self.limitExtrusionAngle (newItem, angle, ctx)
        return False


    def enterPolarShape(self, node, ctx):
        """
        Enter a polar shape, transform to a simple shape and re-run on visitor (self)
        """
        transformed = node.toQuadraticSpline (ctx.getResolvedAttributes ())
        if transformed == None:
            transformed = node.toCubicSpline (ctx.getResolvedAttributes ())
        if transformed == None:
            transformed = node.toPolygon (ctx.getResolvedAttributes ())
        assert transformed != None, "can not transform to a simple shape geometry"
        self.visit (transformed, ctx)
        return False


    def leaveTransformedShape(self, node, ctx):
        """
        Leave transformed shape.
        """
        return node


    def limitExtrusionAngle(self, node, angle, ctx):
        """
        Limit angle of rotate extrude.
        """
        if angle < 0:
            if angle > -360:
                rotLimit = createRotateAngleLimiter (node, 0, -angle, inverse = True).intersect (node)
                return rotLimit
        elif angle < 360:
            rotLimit = createRotateAngleLimiter (node, 0, angle).intersect (node)
            return rotLimit
        return node


    def createTransformFromStack(self, ctx):
        """
        Create affinite transform from transform stack
        """
        transformStack = ctx.extrusionData["transformStack"]
        m = matrix.AffineIdentical2D ()
        for index in range (len (transformStack) - 1, -1, -1):
            se = transformStack[index]
            nt = None
            if isinstance (se, transform.Translate):
                tv = se.evaluate ("vector", ctx.getResolvedAttributes ())
                x = tv[0]
                y = tv[1]
                nt = matrix.AffineTranslate2D (x, y)
            elif isinstance (se, transform.Scale):
                tv = se.evaluate ("vector", ctx.getResolvedAttributes ())
                x = tv[0]
                y = tv[1]
                nt = matrix.AffineScale2D (x, y)
            elif isinstance (se, transform.Rotate):
                tv = se.evaluate ("vector", ctx.getResolvedAttributes ())
                x = tv[0]
                nt = matrix.AffineRotate2D (x)
            else:
                assert False, "transformation type not handled."
            m = matrix.multiply (nt, m)
        return m


    def enterTransform(self, node, ctx):
        """
        Enter a transformation.
        """
        if ctx.extrusionData == None:
            return True

        ctx.extrusionData["transformStack"].append (node)
        return True


    def leaveTransform(self, node, ctx):
        """
        Leave a transformation.
        """
        return node


    def enterExtrusion(self, node, ctx):
        """
        Enter extrusion.
        """
        assert ctx.extrusionData == None, "found extrusion in extrusion."
        angle = node.parameter ("angle")
        # TODO: move assert to tree node
        assert (angle >= -360) and (angle <= 360)
        ctx.extrusionData = {
            "extrudeRoot": node,
            "transformStack": [],
            "generated": None
        }
        return True


    def leaveExtrusion(self, node, ctx):
        """
        Leave extrusion.
        """
        newItem = ctx.extrusionData["generated"]
        ctx.extrusionData = None
        return newItem

PovRayRotateExtrudeRewriter = _PovRayRotateExtrudeRewriter ()





class _PovRaySceneWriter (tree.Visitor):
    """
    Write scene items like lights to PovRay script.
    """
    # TODO: also allow translations on lights
    def __init__(self):
        super().__init__()
        self._rule (scene.Scene, self.unhandledSceneElement)
        self._rule (scene._Light, self.enterSkip)
        self._rule (scene.PovCameraRefinement, self.enterSkip)
        self._rule (scene.PhotonSettings, self.enterSkip)
        self._rule (scene.RadiositySettings, self.enterSkip)


    def enterSkip(self, node, ctx):
        """
        Skip scene item.
        """
        return True


    def unhandledSceneElement(self, node, ctx):
        """
        Enter a un handled scene element.
        """
        assert False, "scene element not handled"
        return True
        

    def execute(self, node, parentContext):
        """
        Execute scene writer.
        """
        ctx = tree.VisitorContext ()
        ctx.parentContext = parentContext
        ctx.writer = parentContext.writer
        self.visit (node, ctx)


PovRaySceneWriter = _PovRaySceneWriter ()





class _PovRayIncludeCollector (tree.Visitor):
    """
    Collect include files of for povray
    """
    def __init__(self):
        super().__init__ ()
        self._rule (solid.Solid, self.enterMaterial)
        self._rule (scene._Light, self.enterMaterial)


    def execute(self, node, defaultAttributes):
        """
        Run collection of include files
        """
        ctx = tree.VisitorContext ()
        ctx.includeFiles = []
        self.visit (node, ctx)
        return ctx.includeFiles


    def enterMaterial(self, node, ctx):
        """
        Collect include files from material parameters.
        """
        includes = ctx.getAttribute ("material.povincludes")
        if includes != None:
            if isinstance (includes, list):
                for include in includes:
                    if not include in ctx.includeFiles:
                        ctx.includeFiles.append (include)
            if isinstance (includes, str):
                if not includes in ctx.includeFiles:
                    ctx.includeFiles.append (includes)
        return True


PovRayIncludeCollector = _PovRayIncludeCollector ()





class _PovRayCameraRefinementCollector (tree.Visitor):
    """
    Collect include files of for povray
    """
    def __init__(self):
        super().__init__ ()
        self._rule (scene.PovCameraRefinement, self.enterRefinement)


    def execute(self, node, defaultAttributes):
        """
        Run collection of include files
        """
        ctx = tree.VisitorContext ()
        ctx.refinements = ""
        self.visit (node, ctx)
        return ctx.refinements


    def enterRefinement(self, node, ctx):
        """
        Collect camera refinement parameters.
        """
        ctx.refinements = ctx.refinements + node.format () + "\n"
        return True


PovRayCameraRefinementCollector = _PovRayCameraRefinementCollector ()





class PovRayTransformStack:
    """
    Transform stack for PovRay writer.
    """
    def __init__(self):
        self.stacks = [[]]


    def pushLayer(self):
        """
        Push a new transform layer to the stack.
        """
        self.stacks.append ([])


    def popAndWriteLayer(self, ctx):
        """
        Pops a transform layer from the stack and writes it.
        """
        assert len (self.stacks) > 1
        self.stacks.pop ()
        stack = self.stacks[-1]
        for ti in range (len (stack) - 1, -1, -1):
            t = stack[ti]
            self.writeTransform(t, ctx)


    def writeTransform(self, node, ctx):
        """
        Writes a single transform to the povray script.
        """
        if isinstance (node, transform.Translate):
            tv = node.evaluate ("vector", ctx.getResolvedAttributes ())
            ctx.writer.write ("translate <" + str (tv[0]) + ", " + str (tv[2]) + ", " + str (tv[1]) + ">\n")
        elif isinstance (node, transform.Rotate):
            tv = node.evaluate ("vector", ctx.getResolvedAttributes ())
            ctx.writer.write ("rotate <" + str (-tv[0]) + ", " + str (-tv[2]) + ", " + str (-tv[1]) + ">\n")
        elif isinstance (node, transform.Scale):
            tv = node.evaluate ("vector", ctx.getResolvedAttributes ())
            ctx.writer.write ("scale <" + str (tv[0]) + ", " + str (tv[2]) + ", " + str (tv[1]) + ">\n")
        else:
            assert False, "unexpected transform type"


    def pushTransform(self, node, ctx):
        """
        Push a transform to the stack.
        """
        assert len (self.stacks) > 0
        self.stacks[len (self.stacks) - 1].append (node)


    def popTransform(self, node, ctx):
        """
        Pop a transform from the stack.
        """
        assert len (self.stacks) > 0
        oldNode = self.stacks[len (self.stacks) - 1].pop ()


class PovRayWriter (tree.Visitor):
    # TODO: try to reduce building of objects, seems to be slow on rendering...
    """
    Write CSG Tree to PovRay script.
    """
    def __init__(self):
        super ().__init__()
        self._rule (tree.Generator, enter = self.generator)
        self._rule (solid.Sphere, enter = self.sphere)
        self._rule (solid.Cube, enter = self.cube)
        self._rule (solid.Cylinder, enter = self.cylinder)
        self._rule (PovSolidPrism, enter = self.prism)
        self._rule (PovSolidExtrudedTorus, enter = self.torus)
        self._rule (solid.Polyhedron, enter = self.polyhedron)
        self._rule (transform.Translate, enter = self.enterTransform, leave = self.leaveTransform)
        self._rule (transform.Rotate, enter = self.enterTransform, leave = self.leaveTransform)
        self._rule (transform.Scale, enter = self.enterTransform, leave = self.leaveTransform)
        self._rule (boolean.Union, enter = self.enterUnion, leave = self.leaveBoolean)
        self._rule (boolean.Difference, enter = self.enterDifference, leave = self.leaveBoolean)
        self._rule (boolean.Intersection, enter = self.enterIntersection, leave = self.leaveBoolean)
        self._rule (tree.Group, enter = self.enterGroup, leave = self.leaveGroup)
        self._rule (part.Part, enter = self.enterPart, leave = self.leavePart)
        self._rule (scene.PointLight, enter = self.enterPointLight, leave = self.leaveLight)
        self._rule (scene.PovCameraRefinement, enter = self.enterSkipScene, leave = self.leaveSkipScene)
        self._rule (scene.PhotonSettings, enter = self.enterSceneElement, leave = self.leaveSkipScene)
        self._rule (scene.RadiositySettings, enter = self.enterSceneElement, leave = self.leaveSkipScene)


    def execute(self, filename: str, node: object, defaultAttributes: dict = None, cameraVector: list = None, width = 1, height = 1) -> None:
        """
        Run writer on tree, generate items before writing.
        """
        ctx = self.createContext (filename)
        ctx.transformStack = PovRayTransformStack ()
        if defaultAttributes == None:
            ctx.defaultArguments = tree.DefaultAttributes
        else:
            ctx.defaultArguments = defaultAttributes
        ctx.cameraVector = cameraVector
        ctx.width = width
        ctx.height = height
        includeFiles = PovRayIncludeCollector.execute (node, ctx.defaultArguments)
        self.writeIncludes (ctx, includeFiles)
        cameraRefinements = PovRayCameraRefinementCollector.execute (node, ctx.defaultArguments)
        self.writeCameraVector (ctx, cameraRefinements)
        PovRaySceneWriter.execute (node, ctx)
        node = reducegroups.ReduceGroups.execute (node, False)
        node = PovRayLinearExtrudeRewriter.execute (node, ctx.defaultArguments)
        node = PovRayRotateExtrudeRewriter.execute (node, ctx.defaultArguments)
        self.visit (node, ctx, False)
        ctx.writer.close ()


    def _enterDefault(self, node: object, context: object) -> bool:
        """
        Catch nodes without matching rule.
        """
        assert False, "node type not handled"


    def createContext(self, filename: str):
        """
        Create context for writer.
        """
        ctx = tree.VisitorContext ()
        ctx.filename = filename
        ctx.writer = textwriter.TextWriter (textwriter.FileWriter (filename))
        ctx.colorStack = []
        return ctx


    def writeIncludes(self, ctx, includeFiles: list):
        """
        Write required include files.
        """
        for i in includeFiles:
            ctx.writer.write ("#include \"" + i + "\"\n")


    def writeCameraVector(self, ctx, cameraRefinements):
        """
        Write camera vector.
        """
        if ctx.cameraVector == None:
            cv = [50, 50, 0, 0, 0, 0]
        else:
            cv = ctx.cameraVector
            assert cmath.isVector (ctx.cameraVector), "Camera vector has invalid format"

        # check which camera format is used:
        #   [location X, Y Z, lookat X, Y, Z]
        #   [translate X, Y, Z, rotate X, Y, T, distance]
        if len (ctx.cameraVector) == 6:
            locationVector = (cv[0], cv[1], cv[2])
            lookAtVector = (cv[3], cv[4], cv[5])
            rotateVector = (0, 0, 0)
            translateVector = (0, 0, 0)
        elif len (ctx.cameraVector) == 7:
            locationVector = (0, 0, cv[6])
            lookAtVector = (0, 0, 0)
            rotateVector = (-cv[3], -cv[4], -cv[5])
            translateVector = [cv[0], cv[1], cv[2]] 
        else:
            assert False, "Camera vector has invalid format"

        # write camera format
        ctx.writer.write ("camera {\n")
        ctx.writer.increaseIndent ()
        aspectRatio = (ctx.width / ctx.height)
        angle = (23.0 - 0.85 * aspectRatio) * aspectRatio
        ctx.writer.write ("angle " + str (angle) + "\n")
        ctx.writer.write ("right <" + str (aspectRatio) + ", 0, 0>\n")
        ctx.writer.write ("up <0, 1, 0>\n")
        ctx.writer.write ("location <" + str (locationVector[0]) + ", " + str (locationVector[2]) + ", " + str (locationVector[1]) + ">\n")
        ctx.writer.write ("look_at <" + str (lookAtVector[0]) + ", " + str (lookAtVector[2]) + ", " + str (lookAtVector[1]) + ">\n")
        ctx.writer.write ("rotate <" + str (rotateVector[0]) + ", 0, 0>\n") # x
        ctx.writer.write ("rotate <0, 0, " + str (rotateVector[1]) + ">\n") # y
        ctx.writer.write ("rotate <0, " + str (rotateVector[2]) + ", 0>\n") # z
        ctx.writer.write ("translate <" + str (translateVector[0]) + ", " + str (translateVector[2]) + ", " + str (translateVector[1]) + ">\n")
        ctx.writer.write (cameraRefinements)
        ctx.writer.decreaseIndent ()
        ctx.writer.write ("}\n")


    def writeTexture(self, node, ctx):
        """
        Write texture data.
        """
        # TODO: encapsulate into texture block

        # get color attribute
        color = ctx.getAttribute ("material.color")
        if color != None:
            assert isinstance (color, material.Color)

        # format pigment setting
        pigment = ctx.getAttribute ("material.pigment")
        if (pigment == None) or (pigment == ""):
            pigment = color
        if (pigment != None) and (pigment != ""):
            ctx.writer.write ("pigment {\n")
            ctx.writer.increaseIndent ()
            if isinstance (pigment, material.Color):
                # write color as pigment
                ctx.writer.write (self.formatColor (pigment) + "\n")
            else:
                # write pigment
                ctx.writer.write (str (pigment) + "\n")
            ctx.writer.decreaseIndent ()
            ctx.writer.write ("}\n")

        # format normal setting
        normal = ctx.getAttribute ("material.normal")
        if (normal != None) and (normal != ""):
            ctx.writer.write ("normal {\n")
            ctx.writer.increaseIndent ()
            ctx.writer.write (str (normal) + "\n")
            ctx.writer.decreaseIndent ()
            ctx.writer.write ("}\n")

        # finish settings
        finishedOpened = False

        # format ambient setting
        if self.writeColorOrFloat (ctx, "material.ambient", "ambient", "finish", finishedOpened, 0.2):
            finishedOpened = True

        # format emission setting
        if self.writeColor (ctx, "material.emission", "emission", "finish", finishedOpened, ""):
            finishedOpened = True

        # format diffuse setting
        if self.writeFloat (ctx, "material.diffuse", "diffuse", "finish", finishedOpened, 0.6, albedoFlag="material.diffuse.albedo"):
            finishedOpened = True

        # format brilliance setting
        if self.writeFloat (ctx, "material.brilliance", "brilliance", "finish", finishedOpened, 1):
            finishedOpened = True

        # format phong setting
        if self.writeFloat (ctx, "material.phong", "phong", "finish", finishedOpened, 0, albedoFlag="material.phong.albedo"):
            finishedOpened = True

        # format phongsize setting
        if self.writeFloat (ctx, "material.phongsize", "phong_size", "finish", finishedOpened, 40):
            finishedOpened = True

        # format specular setting
        if self.writeFloat (ctx, "material.specular", "specular", "finish", finishedOpened, 0, albedoFlag="material.specular.albedo"):
            finishedOpened = True

        # format conserve energy setting
        if self.writeBool (ctx, "material.conserveenergy", "conserve_energy", "finish", finishedOpened, False):
            finishedOpened = True

        # format useaplha energy setting
        if self.writeBool (ctx, "material.usealpha", "use_alpha", "finish", finishedOpened, False):
            finishedOpened = True

        # write reflection parameters
        refAttr = ctx.getAttribute ("material.reflection")
        reflectionWritten = False
        if (refAttr != None) and (refAttr != "") and (refAttr != 0):
            reflectionWritten = True
            if finishedOpened == False:
                ctx.writer.write ("finish {\n")
                ctx.writer.increaseIndent ()
                finishedOpened = True
            assert isinstance (refAttr, (int, float, material.Color))
            refMinAttr = ctx.getAttribute ("material.reflection.min")
            if (refMinAttr != None) and (refMinAttr != ""):
                assert isinstance (refAttr, (int, float, material.Color))
            else:
                refMinAttr = None
            ctx.writer.write ("reflection {\n")
            ctx.writer.increaseIndent ()
            if refMinAttr != None:
                ctx.writer.write (self.formatColorFloat (refMinAttr) + ", " + self.formatColorFloat (refAttr) + "\n")
            else:
                ctx.writer.write (self.formatColorFloat (refAttr) + "\n")
            self.writeFloat (ctx, "material.reflection.fresnel", "fresnel", "reflection", True, 0)
            self.writeFloat (ctx, "material.reflection.falloff", "falloff", "reflection", True, 1)
            self.writeFloat (ctx, "material.reflection.exponent", "exponent", "reflection", True, 1)
            if ctx.getAttribute ("material.reflection.metallic") in (None, ""):
                self.writeFloat (ctx, "material.metallic", "metallic", "reflection", True, 0)
            else:
                self.writeFloat (ctx, "material.reflection.metallic", "metallic", "reflection", True, 0)
            ctx.writer.decreaseIndent ()
            ctx.writer.write ("}\n")


        # format metallic setting
        if reflectionWritten == False:
            if self.writeFloat (ctx, "material.metallic", "metallic", "finish", finishedOpened, 0):
                finishedOpened = True

        # format roughness setting
        if self.writeFloat (ctx, "material.roughness", "roughness", "finish", finishedOpened, 0.05):
            finishedOpened = True

        # format crand setting
        if self.writeFloat (ctx, "material.crand", "crand", "finish", finishedOpened, 0):
            finishedOpened = True

        # iridiscene
        iriAttr = ctx.getAttribute ("material.iridescene")
        if not (iriAttr in (None, "", 0)):
            assert isinstance (iriAttr, (int, float))
            if finishedOpened == False:
                ctx.writer.write ("finish {\n")
                ctx.writer.increaseIndent ()
                finishedOpened = True
            ctx.writer.write ("irid {\n")
            ctx.writer.increaseIndent ()
            ctx.writer.write (str (iriAttr) + "\n")
            self.writeFloat (ctx, "material.iridescene.thickness", "thickness", "irid", True, 0)
            self.writeFloat (ctx, "material.iridescene.turbulence", "turbulence", "irid", True, 0)
            ctx.writer.decreaseIndent ()
            ctx.writer.write ("}\n")

        # end finish settings
        if finishedOpened:
            ctx.writer.decreaseIndent ()
            ctx.writer.write ("}\n")

        # write interior
        interiorOpened = False

        if self.writeFloat (ctx, "material.interior.ior", "ior", "interior", interiorOpened, 1):
            interiorOpened = True

        if self.writeFloat (ctx, "material.interior.caustics", "caustics", "interior", interiorOpened, 0):
            interiorOpened = True

        if self.writeFloat (ctx, "material.interior.dispersion", "dispersion", "interior", interiorOpened, 1):
            interiorOpened = True

        if self.writeInteger (ctx, "material.interior.dispersionsamples", "dispersion_samples", "interior", interiorOpened, 7):
            interiorOpened = True

        if self.writeFloat (ctx, "material.interior.fadedistance", "fade_distance", "interior", interiorOpened, 0):
            interiorOpened = True

        if self.writeFloat (ctx, "material.interior.fadepower", "fade_power", "interior", interiorOpened, 0):
            interiorOpened = True

        if self.writeColor (ctx, "material.interior.fadecolor", "fade_color", "interior", interiorOpened, ""):
            interiorOpened = True

        if interiorOpened:
            ctx.writer.decreaseIndent ()
            ctx.writer.write ("}\n")

        # write photon mapping settings
        photonsOpened = False

        photonsTarget = ctx.getAttribute ("material.photons.target")
        if photonsTarget == True:
            if photonsOpened == False:
                ctx.writer.write ("photons {\n")
                ctx.writer.increaseIndent ()
                photonsOpened = True
            targetValStr = ""
            photonsTargetValue = ctx.getAttribute ("material.photons.targetvalue")
            if not photonsTargetValue in (None, 1.0):
                targetValStr = " " + str (photonsTargetValue)
            ctx.writer.write ("target" + targetValStr + "\n")


        if self.writeBool (ctx, "material.photons.refraction", "refraction", "photons", photonsOpened, False):
            photonsOpened = True

        if self.writeBool (ctx, "material.photons.reflection", "reflection", "photons", photonsOpened, False):
            photonsOpened = True

        if self.writeFloat (ctx, "material.photons.density", "density", "photons", photonsOpened, 1):
            photonsOpened = True

        if self.writeBool (ctx, "material.photons.collect", "collect", "photons", photonsOpened, True):
            photonsOpened = True

        if self.writeBool (ctx, "material.photons.passthrough", "passthrough", "photons", photonsOpened, False):
            photonsOpened = True

        if self.writeBool (ctx, "material.photons.arealight", "arealight", "photons", photonsOpened, False):
            photonsOpened = True

        if self.writeBool (ctx, "material.photons.splitunion", "splitunion", "photons", photonsOpened, True):
            photonsOpened = True

        if photonsOpened:
            ctx.writer.decreaseIndent ()
            ctx.writer.write ("}\n")


    def formatColorFloat(self, value):
        if isinstance (value, material.Color):
            return self.formatColor (value)
        if isinstance (value, (int, float)):
            return str (value)
        return ""


    def writeColor(self, ctx, attributeName, povName, group: str = None, groupOpened: bool = False, default = None):
        """
        Write color as attribute.
        """
        attr = ctx.getAttribute (attributeName)
        if (attr != None) and (attr != ""):
            if isinstance (attr, material.Color):
                # use color as attribute
                if (default == None) or (attr != default):
                    if groupOpened == False:
                        ctx.writer.write (group + " {\n")
                        ctx.writer.increaseIndent ()
                        groupOpened = True
                    ctx.writer.write (povName + " " + self.formatColor (attr) + "\n")
            else:
                assert False, "unexpected argument type"
        return groupOpened


    def writeColorOrFloat(self, ctx, attributeName, povName, group: str = None, groupOpened: bool = False, default = None):
        """
        Write color or float value as attribute.
        """
        attr = ctx.getAttribute (attributeName)
        if (attr != None) and (attr != ""):
            if isinstance (attr, material.Color):
                # use color as attribute
                if (default == None) or (attr != default):
                    if groupOpened == False:
                        ctx.writer.write (group + " {\n")
                        ctx.writer.increaseIndent ()
                        groupOpened = True
                    ctx.writer.write (povName + " " + self.formatColor (attr) + "\n")
            elif isinstance (attr, (int, float)):
                if (default == None) or (attr != default):
                    # use factor as attribute
                    if groupOpened == False:
                        ctx.writer.write (group + " {\n")
                        ctx.writer.increaseIndent ()
                        groupOpened = True
                    ctx.writer.write (povName + " " + str (attr) + "\n")
                else:
                    # ambient default value
                    pass
            else:
                assert False, "unexpected argument type"
        return groupOpened


    def writeInteger(self, ctx, attributeName, povName, group: str = None, groupOpened: bool = False, default = None):
        """
        Write integer value as attribute.
        """
        attr = ctx.getAttribute (attributeName)
        if (attr != None) and (attr != ""):
            if isinstance (attr, int):
                if (default == None) or (attr != default):
                    if groupOpened == False:
                        ctx.writer.write (group + " {\n")
                        ctx.writer.increaseIndent ()
                        groupOpened = True
                    ctx.writer.write (povName + " " + str (attr) + "\n")
            else:
                assert False, "unexpected argument type"
        return groupOpened


    def writeFloat(self, ctx, attributeName, povName, group: str = None, groupOpened: bool = False, default = None, albedoFlag = None):
        """
        Write float value as attribute.
        """
        albedoStr = ""
        albedoAttr = ctx.getAttribute (albedoFlag)
        if albedoAttr == True:
            albedoStr = " albedo"
        attr = ctx.getAttribute (attributeName)
        if (attr != None) and (attr != ""):
            if isinstance (attr, (int, float)):
                if (default == None) or (attr != default):
                    if groupOpened == False:
                        ctx.writer.write (group + " {\n")
                        ctx.writer.increaseIndent ()
                        groupOpened = True
                    ctx.writer.write (povName + albedoStr + " " + str (attr) + "\n")
            else:
                assert False, "unexpected argument type"
        return groupOpened


    def writeBool(self, ctx, attributeName, povName, group: str = None, groupOpened: bool = False, default = None):
        """
        Write boolean value as attribute.
        """
        attr = ctx.getAttribute (attributeName)
        if (attr != None) and (attr != ""):
            if isinstance (attr, bool):
                if (default == None) or (attr != default):
                    if groupOpened == False:
                        ctx.writer.write (group + " {\n")
                        ctx.writer.increaseIndent ()
                        groupOpened = True
                    val = "on" if attr else "off"
                    ctx.writer.write (povName + " " + val + "\n")
            else:
                assert False, "unexpected argument type"
        return groupOpened


    def formatColor(self, color):
        """
        Format color item.
        """
        assert isinstance (color, material.Color)
        return color.asString ()


    def enterSceneElement(self, node, ctx):
        """
        Write scene element settings
        """
        ctx.writer.write (node.format ())


    # handle generator node

    def generator(self, node, context):
        self.visit (node.generate (context.getResolvedAttributes ()), context)
        return True


    # handle solids

    def sphere(self, node, ctx):
        """
        Enter a sphere.
        """
        ctx.writer.write ("sphere {\n")
        ctx.writer.increaseIndent ()
        radius = node.evaluate ("radius", ctx.getResolvedAttributes ())
        ctx.writer.write ("<0, 0, 0>, " + str (radius) + "\n")
        self.writeTexture (node, ctx)
        ctx.transformStack.pushLayer ()
        ctx.transformStack.popAndWriteLayer (ctx)
        ctx.writer.decreaseIndent ()
        ctx.writer.write ("}\n")
        return False


    def cube(self, node, ctx):
        """
        Enter a cube.
        """
        ctx.writer.write ("box {\n")
        ctx.writer.increaseIndent ()
        size = node.evaluate ("size", ctx.getResolvedAttributes ())
        sz = [-size[0] / 2, -size[1] / 2, -size[2] / 2, size[0] / 2, size[1] / 2, size[2] / 2]
        ctx.writer.write ("<" + str (sz[0]) + ", " + str (sz[2]) + ", " + str (sz[1]) + ">" + "\n")
        ctx.writer.write ("<" + str (sz[3]) + ", " + str (sz[5]) + ", " + str (sz[4]) + ">" + "\n")
        self.writeTexture (node, ctx)
        ctx.transformStack.pushLayer ()
        ctx.transformStack.popAndWriteLayer (ctx)
        ctx.writer.decreaseIndent ()
        ctx.writer.write ("}\n")
        return False


    def cylinder(self, node, ctx):
        """
        Enter a cylinder.
        """
        ctx.writer.write ("cone {\n")
        ctx.writer.increaseIndent ()
        height = node.evaluate ("height", ctx.getResolvedAttributes ())
        radius = node.evaluate ("radius", ctx.getResolvedAttributes ())
        radius2 = node.evaluate ("radius2", ctx.getResolvedAttributes ())
        if radius2 == None:
            radius2 = radius
        ctx.writer.write ("<0, " + str (-height / 2.0) + ", 0>, " + str (radius) + "\n")
        ctx.writer.write ("<0, " + str (height / 2.0) + ", 0>, " + str (radius2) + "\n")
        self.writeTexture (node, ctx)
        ctx.transformStack.pushLayer ()
        ctx.transformStack.popAndWriteLayer (ctx)
        ctx.writer.decreaseIndent ()
        ctx.writer.write ("}\n")
        return False


    def prism(self, node, ctx):
        """
        Enter a prism.
        """
        ctx.writer.write ("prism {\n")
        ctx.writer.increaseIndent ()
        height = node.height
        polygon = node.polygon
        type_ = node.type_
        points = polygon.getData ()

        # here we go, got height and points, write the prism
        ctx.writer.write (type_ + "\n")
        h1 = (height * -0.5) + node.centerOffset
        h2 = (height * 0.5) + node.centerOffset
        pointCount = len (points)
        if type_ == "linear_spline":
            outPointCount = pointCount
        elif type_ == "quadratic_spline":
            outPointCount = len (points) + 1
        elif type_ == "cubic_spline":
            outPointCount = len (points) + 2
        elif type_ == "bezier_spline":
            outPointCount = pointCount
        else:
            assert False, "spline type not implemented"
        ctx.writer.write (str (h1) + ", " + str (h2) + ", " + str (outPointCount) + ",\n")

        # write points
        if type_ in ("linear_spline", "quadratic_spline", "cubic_spline"):
            if type_ in ("quadratic_spline", "cubic_spline"):
                ctx.writer.write ("<" + str (points[-1][0]) + ", " + str (points[-1][1]) + ">")
            if type_ in ("linear_spline", "quadratic_spline"):
                for pointId in range (0, pointCount):
                    point = points[pointId]
                    ctx.writer.write ("<" + str (point[0]) + ", " + str (point[1]) + ">")
                    if pointId < (pointCount - 1):
                        ctx.writer.write(",\n")
                    else:
                        ctx.writer.write("\n")
            else:
                for pointId in range (0, pointCount):
                    point = points[pointId]
                    ctx.writer.write ("<" + str (point[0]) + ", " + str (point[1]) + ">,\n")
                ctx.writer.write ("<" + str (points[0][0]) + ", " + str (points[0][1]) + ">\n")
        elif type_ == "bezier_spline":
            for pointId in range (0, pointCount):
                point = points[pointId]
                ctx.writer.write ("<" + str (point[0]) + ", " + str (point[1]) + ">")
                if pointId < (pointCount - 1):
                    ctx.writer.write(",\n")
                else:
                    ctx.writer.write("\n")
        else:
            assert False, "invalid spline type"

        # end wiring prism
        self.writeTexture (node, ctx)
        ctx.transformStack.pushLayer ()
        ctx.transformStack.popAndWriteLayer (ctx)
        ctx.writer.decreaseIndent ()
        ctx.writer.write ("}\n")
        return False


    def torus(self, node, ctx):
        """
        Enter a torus.
        """
        ctx.writer.write ("lathe {\n")
        ctx.writer.increaseIndent ()
        numPoints = len (node.points)
        if node.type_ == "bezier_spline":
            ctx.writer.write ("bezier_spline\n")
            ctx.writer.write (str (numPoints))
        elif node.type_ == "linear_spline":
            ctx.writer.write ("linear_spline\n")
            ctx.writer.write (str (numPoints + 1))
        elif node.type_ == "quadratic_spline":
            ctx.writer.write ("quadratic_spline\n")
            ctx.writer.write (str (numPoints + 2))
        elif node.type_ == "cubic_spline":
            ctx.writer.write ("cubic_spline\n")
            ctx.writer.write (str (numPoints + 3))
        else:
            assert False, "TODO: not handled yet"

        # write first control point
        if node.type_ in ("quadratic_spline", "cubic_spline"):
            ctx.writer.write (",\n<" + str (node.points[-1][0]) + ", " + str (node.points[-1][1]) + ">")

        # write points
        for point in node.points:
            ctx.writer.write (",\n<" + str (point[0]) + ", " + str (point[1]) + ">")

        # close polygon points
        if node.type_ in ("linear_spline", "quadratic_spline"):
            ctx.writer.write (",\n<" + str (node.points[0][0]) + ", " + str (node.points[0][1]) + ">\n")
        elif node.type_ == "cubic_spline":
            ctx.writer.write (",\n<" + str (node.points[0][0]) + ", " + str (node.points[0][1]) + ">")
            ctx.writer.write (",\n<" + str (node.points[1][0]) + ", " + str (node.points[1][1]) + ">\n")
        else:
            ctx.writer.write ("\n")

        # end wiring torus
        self.writeTexture (node, ctx)
        ctx.transformStack.pushLayer ()
        ctx.transformStack.popAndWriteLayer (ctx)
        ctx.writer.decreaseIndent ()
        ctx.writer.write ("}\n")
        return False


    def polyhedron(self, node, ctx):
        """
        Enter a polyhedron.
        """
        points, faces, normals, uvVectors = node.getData ()
        ctx.writer.write ("mesh2 {\n")
        ctx.writer.increaseIndent ()

        facesWithNormals = []
        facesWithoutNormals = []

        for face in faces:
            if len (face) >= 6:
                if (face[3] != None) or (face[4] != None) or (face[5] != None):
                    facesWithNormals.append (face)
                else:
                    facesWithoutNormals.append (face)
            else:
                facesWithoutNormals.append (face)
        processNormals = False
        if len (facesWithNormals) > 0:
            if normals != None:
                if len (normals) > 0:
                    processNormals = True

        # check if we need to process uv vectors
        processUvVectors = False
        if uvVectors != None:
            if len (uvVectors) > 0:
                for face in faces:
                    if len (face) >= 9:
                        if (face[6] != None) or (face[7] != None) or (face[8] != None):
                            processUvVectors = True

        # write points to mesh2 structure
        ctx.writer.write ("vertex_vectors {\n")
        ctx.writer.increaseIndent ()
        ctx.writer.write (str (len (points)) + ",\n")
        for pid in range (0, len (points)):
            point = points[pid]
            s = self.formatVector (point)
            if pid < (len (points) - 1):
                s = s + ","
            ctx.writer.write (s + "\n")
        ctx.writer.decreaseIndent ()
        ctx.writer.write ("}\n")

        # write list of normals
        if processNormals:
            ctx.writer.write ("normal_vectors {\n")
            ctx.writer.increaseIndent ()
            ctx.writer.write (str (len (normals)) + ",\n")
            for nid in range (0, len (normals)):
                normal = normals[nid]
                s = self.formatVector (normal)
                if nid < (len (normals) - 1):
                    s = s + ","
                ctx.writer.write (s + "\n")
            ctx.writer.decreaseIndent ()
            ctx.writer.write ("}\n")

        # write list of uv vectors
        if processUvVectors:
            ctx.writer.write ("uv_vectors {\n")
            ctx.writer.increaseIndent ()
            ctx.writer.write (str (len (uvVectors)) + ",\n")
            for uid in range (0, len (uvVectors)):
                uv = uvVectors[uid]
                s = self.formatUvVector (uv)
                if uid < (len (uvVectors) - 1):
                    s = s + ","
                ctx.writer.write (s + "\n")
            ctx.writer.decreaseIndent ()
            ctx.writer.write ("}\n")

        # write faces
        ctx.writer.write ("face_indices {\n")
        ctx.writer.increaseIndent ()
        allFaces = facesWithNormals + facesWithoutNormals
        ctx.writer.write (str (len (allFaces)) + ",\n")
        for fid in range (0, len (allFaces)):
            face = allFaces[fid]
            s = self.formatVectorIndices (face[0], face[1], face[2])
            if fid < (len (allFaces) - 1):
                s = s + ","
            ctx.writer.write (s + "\n")
        ctx.writer.decreaseIndent ()
        ctx.writer.write ("}\n")

        # write face normals
        if processNormals:
            ctx.writer.write ("normal_indices {\n")
            ctx.writer.increaseIndent ()
            ctx.writer.write (str (len (facesWithNormals)) + ",\n")
            for fid in range (0, len (facesWithNormals)):
                face = facesWithNormals[fid]
                s = self.formatVectorIndices (face[3], face[4], face[5])
                if fid < (len (facesWithNormals) - 1):
                    s = s + ","
                ctx.writer.write (s + "\n")
            ctx.writer.decreaseIndent ()
            ctx.writer.write ("}\n")

        # write face uv mappings
        if processUvVectors:
            ctx.writer.write ("uv_indices {\n")
            ctx.writer.increaseIndent ()
            ctx.writer.write (str (len (allFaces)) + ",\n")
            for fid in range (0, len (allFaces)):
                face = allFaces[fid]
                if len (face) < 9:
                    s = "<0, 0, 0>"
                else:
                    s = self.formatVectorIndices (face[6], face[7], face[8])
                if fid < (len (allFaces) - 1):
                    s = s + ","
                ctx.writer.write (s + "\n")
            ctx.writer.decreaseIndent ()
            ctx.writer.write ("}\n")

        # write inside vector
        ctx.writer.write ("inside_vector <0, 0, 1>\n")    

        # end of mash
        self.writeTexture (node, ctx)
        ctx.transformStack.pushLayer ()
        ctx.transformStack.popAndWriteLayer (ctx)
        ctx.writer.decreaseIndent ()
        ctx.writer.write ("}\n")


    def formatVector(self, vector):
        """
        Format a 3 dimensional vector.
        """
        return "<" + str (vector[0]) + ", " + str (vector[2]) + ", " + str (vector[1]) + ">"


    def formatVectorIndices(self, a, b, c):
        """
        Format vector indices.
        """
        astr = str (a) if a != None else 0
        bstr = str (b) if b != None else 0
        cstr = str (c) if c != None else 0
        return "<" + astr + ", " + bstr + ", " + cstr + ">"


    # handle transforms

    def enterGroup(self, node, ctx):
        """
        Enter an object.
        """
        return True


    def leaveGroup(self, node, ctx):
        """
        Leave a group.
        """
        return node


    def enterTransform(self, node, ctx):
        """
        Enter a transform operation.
        """
        ctx.transformStack.pushTransform (node, ctx)
        return True


    def leaveTransform(self, node, ctx):
        """
        Leave a transform operation.
        """
        ctx.transformStack.popTransform (node, ctx)
        return node


    # handle boolean operations

    def enterUnion(self, node, ctx):
        """
        Enter an union.
        """
        ctx.writer.write ("union {\n")
        ctx.writer.increaseIndent ()
        ctx.transformStack.pushLayer ()
        return True


    def enterDifference(self, node, ctx):
        """
        Enter an difference.
        """
        ctx.writer.write ("difference {\n")
        ctx.writer.increaseIndent ()
        ctx.transformStack.pushLayer ()
        return True


    def enterIntersection(self, node, ctx):
        """
        Enter an intersection.
        """
        ctx.writer.write ("intersection {\n")
        ctx.writer.increaseIndent ()
        ctx.transformStack.pushLayer ()
        return True


    def leaveBoolean(self, node, ctx):
        """
        Leave a boolean operation.
        """
        ctx.transformStack.popAndWriteLayer (ctx)
        ctx.writer.decreaseIndent ()
        ctx.writer.write ("}\n")
        return node


    # handle parts

    def enterPart(self, node, ctx):
        return True
        

    def leavePart(self, node, ctx):
        return node
            

    def enterSkipScene(self, node, ctx):
        return True
        

    def leaveSkipScene(self, node, ctx):
        return node
        

    # handle ligths
    # TODO: remove extra class - handle here
    def enterPointLight(self, node, ctx):
        ctx.writer.write ("light_source {\n")
        ctx.writer.increaseIndent ()
        position = node.evaluate ("position", ctx.getResolvedAttributes ())
        color = "rgb<1,1,1>" # TODO: from attributes
        ctx.writer.write ("<" + str (position[0]) + ", " + str (position[2]) + ", " + str (position[1]) + ">, " + color)
        ctx.writer.decreaseIndent ()
        ctx.writer.write ("}\n")
        return True


    def leaveLight(self, node, ctx):
        return node



class _PovRay:
    """
    PovRay plugin.
    """
    def __init__(self):
        self.silent = True
        self.writer = PovRayWriter ()
        self.instanceLock = threading.Lock ()


    def getScriptExtension(self):
        return "pov"


    def getImageExtension(self):
        return "png"


    def writeTree(self, filename: str, tree: object, defaultArgs: dict = None, cameraVector: list = None, width = 1, height = 1) -> None:
        """
        Write CSG Tree to povray script file.
        """
        self.writer.execute (filename, tree, defaultArgs, cameraVector, width, height)
        return True


    def render(self, scriptFile, outputFile, width, height, antialias, quality, tree: object, cameraVector: list = None, preview: bool = False):
        """
        Render image with antialiasing.
        """
        args = [PovRayExecutable, "+O" + outputFile, "+W" + str (int(width)), "+H" + str (int(height)), "+FN"]
        if preview != True:
            args.append ("-D")

        # render quality settings
        args.append ("+Q" + str (quality))

        # antialiasing settings
        anitaliasThresholds = [
            "+A0.2",
            "+A0.1",
            "+A0.05",
            "+A0.025",
            "+A0.0125",
            "+A0.00625",
            "+A0.05",
            "+A0.025",
            "+A0.0125",
            "+A0.00625",
            "+A0.003",
            "+A0.00015"
        ]
        if antialias > 0:
            if antialias >= 6:
                # adaptive
                args.append ("+AM2")
            else:
                # non adaptive
                args.append ("+AM1")
            args.append (anitaliasThresholds[antialias])

        args.append (scriptFile)
        # let povray instance not run in parallel!
        self.instanceLock.acquire ()
        cmd = subprocess.run (args, capture_output=self.silent)
        if self.silent and (cmd.returncode != 0):
            print (cmd.stderr)
            print (cmd.stdout)
        self.instanceLock.release ()
        return cmd.returncode == 0


    def canManufacture(self):
        """
        Check if manufacturing is supported.
        """
        return False


    def manufacture(self, scriptFile, outputFile):
        """
        Manufacture a part.
        """
        # not supported
        return False
        
        
    def scriptRequiresRenderingDetails(self):
        """
        PovRay scripts are dependent from the camera position and output image size.
        """
        return True


    def getAttributesOverrides (self):
        """
        Returns the override attributes of this materializer.
        """
        return {
            'materializer.supportsBezierCurves': True
        }
        




# single instance of povray extension
PovRay = _PovRay ()
