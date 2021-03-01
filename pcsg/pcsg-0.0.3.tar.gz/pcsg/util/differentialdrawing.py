import math
from . import vmath
from .. import util
from ..attributes import Attributes
from .. import shape




class Segment:
    """
    A differential drawing Segment maps a value **t** in range *0 .. 1* to a two dimensional position vector.
    The segment shall be a continiously differentiable curve.
    """
    def __init (self):
        pass


    def pointAt(self, t):
        """
        Calculates a point for t [0..1].
        """
        assert False, "To be implemented by child"




class Element (Segment):
    """
    A differential drawing element maps a function with a ramge *minT .. maxT* to a two dimensional position vector.
    The segment shall be a continiously differentiable curve.
    """
    def __init__(self, minT = 0, maxT = 1, func = None):
        super ().__init__ ()

        #: Mininal **t** passed to function.
        self.minT = minT

        #: Maximal **t** passed to function.
        self.maxT = maxT

        #: Function to calculate a two dimensional position vector for **t**.
        self.func = func
        pass

    def pointAt(self, t):
        """
        Calculates a point for t [0..1] mapped to range [minT..maxT].
        """
        mt = self.minT + t * (self.maxT - self.minT)
        return self._calculate (mt)

    def _calculate(self, mt):
        """
        Calculates a point for t [minT .. maxT].
        """
        if self.func != None:
            return self.func (mt)
        assert False, "To be implemented by child class, optional use func= parameter"




class Path:
    """
    Path consisting of a list of Segments.
    """
    def __init__(self, segments: list = None):
        if segments == None:
            self.elements = []
        else:
            self.elements = segments


    def appendSegment (self, segment):
        """
        Appends a segment to this Path.
        """
        self.elements.append (segment)


    def pointAt(self, t):
        """
        Calculates a point for t [0..1].
        """
        assert len (self.elements) > 0, "no elements in list"
        ta = t * len (self.elements)
        ti = math.floor (ta)
        if ti >= len (self.elements):
            e = self.elements[-1]
            to = 1
        else:
            e = self.elements[ti]
            to = ta - ti
        return e.pointAt (to)


    @staticmethod
    def _append (points, point):
        """
        Append a point to the list of points, skip if duplicated
        """
        if len (points) > 0:
            if (point[0] == points[-1][0]) or (point[1] == points[-1][1]):
                return
        points.append (point)


    def _rasterizeLinearSegment (self, points, element, minT, maxT, minPos, maxPos, maxError):
        """
        Rasterize a segment of an element
        """
        centerT = (minT + maxT) / 2
        centerPoint = element.pointAt (centerT)
        centerOfLine = ((minPos[0] + maxPos[0]) / 2, (minPos[1] + maxPos[1]) / 2)
        dx = centerPoint[0] - centerOfLine[0]
        dy = centerPoint[1] - centerOfLine[1]
        dist = math.sqrt (dx * dx + dy * dy)
        if dist > (maxError / 2):
            self._rasterizeLinearSegment (points, element, minT, centerT, minPos, centerPoint, maxError)
            self._rasterizeLinearSegment (points, element, centerT, maxT, centerPoint, maxPos, maxError)
        else:
            Path._append (points, centerPoint)


    def _rasterize (self, initialSegmentCount = 10, maxStepSize = 0.1):
        """
        Rasterize elements to a path of point coordinates.
        """
        points = []
        for ei in range (0, len (self.elements)):
            element = self.elements[ei]
            initialStepSize = 1.0 / (initialSegmentCount)
            t = 0
            for step in range (0, initialSegmentCount):
                minPos = element.pointAt (t)
                maxPos = element.pointAt (t + initialStepSize)
                Path._append (points, minPos)
                self._rasterizeLinearSegment (points, element, t, t + initialStepSize, minPos, maxPos, maxStepSize)
                Path._append (points, maxPos)
                t += initialStepSize
        return points


    def toPolygon (self, initialSegmentCount = 10, maxStepSize = 0.1, name: str = None, attributes: Attributes = None):
        """
        Create a Polygon from Path.
        """
        points = self._rasterize (initialSegmentCount = initialSegmentCount, maxStepSize = maxStepSize)
        return shape.Polygon (points = points, name = name, attributes = attributes)



    def toBezier (self, initialSegmentCount = 10, maxStepSize = 0.1, name: str = None, attributes: Attributes = None):
        """
        Create a bezier shape from Path.
        """
        assert False, "TODO:"


    def _rasterizeBezier (self, initialSegmentCount = 10, maxStepSize = 0.1, close = True):
        """
        Rasterize elements to a set of bezier curves.
        """
        points = []
        for ei in range (0, len (self.elements)):
            element = self.elements[ei]
            initialStepSize = 1.0 / (initialSegmentCount)
            t = 0
            # create closing curve between last curve element and current curve element
            if len (points) > 0:
                closingNextCurve = []
                self._rasterizeBezierSegment (closingNextCurve, element, 0, 1, maxStepSize, True)
                closingBezier = Path._createConnectionBezier (points, closingNextCurve)
                if closingBezier != None:
                    points = points + closingBezier
                    pass
            for step in range (0, initialSegmentCount):
                # create bezier segments from path
                self._rasterizeBezierSegment (points, element, t, t + initialStepSize, maxStepSize)
                t += initialStepSize
        if close:
            # close bezier curve if requested
            closingBezier = Path._createConnectionBezier (points, points)
            if closingBezier != None:
                points = points + closingBezier
        return points


    @staticmethod
    def _createConnectionBezier (points1, points2, points1Index = None, points2Index = None):
        """
        Create connection between two bezier curves.
        """
        # calculate indices of points to use
        if points1Index == None:
            p1Index = len (points1) - 4
        else:
            p1Index = points1Index
        if points2Index == None:
            p2Index = 0
        else:
            p2Index = points2Index

        # check if we need a closing curve
        startPoint = points1[p1Index + 3]
        endPoint = points2[p2Index]
        seDist = vmath.vsLength (vmath.vsSub (startPoint, endPoint))
        if seDist == 0:
            return None

        # create smooth closing curve
        lastCp = points1[p1Index + 2]
        nextCp = points2[p2Index + 1]
        cp1Direction = vmath.vsSub (lastCp, startPoint)
        cp2Direction = vmath.vsSub (nextCp, endPoint)
        cpd1 = vmath.vsLength (cp1Direction)
        cpd2 = vmath.vsLength (cp2Direction)
        cpFactor = 0.5
        if cpd1 > 0:
            cp1Direction = vmath.vsMulScalar (cp1Direction, (seDist / cpd1) * cpFactor)
        if cpd2 > 0:
            cp2Direction = vmath.vsMulScalar (cp2Direction, (seDist / cpd2) * cpFactor)
        cp1 = vmath.vsAdd (startPoint, cp1Direction)
        cp2 = vmath.vsAdd (endPoint, cp2Direction)
        return [startPoint, cp1, cp2, endPoint]


    @staticmethod
    def _rasterizeBezierSegmentFindScale (startPoint, control1Direction, control2Direction, endPoint, elementCenter, minScale, maxScale):
        # abort recursion
        centerScale = (minScale + maxScale) / 2
        if (maxScale - minScale) < 0.0000001:
            return centerScale
        leftHalfScale = (minScale + centerScale) / 2
        errLeftHalf = vmath.vsLength (vmath.vsSub (elementCenter, vmath.bezier (
            (
                startPoint, 
                vmath.vsAdd (startPoint, vmath.vsMulScalar (control1Direction, leftHalfScale)), 
                vmath.vsAdd (endPoint, vmath.vsMulScalar (control2Direction, leftHalfScale)), 
                endPoint
            ), 0.5
        )))
        rightHalfScale = (centerScale + maxScale) / 2
        errRightHalf = vmath.vsLength (vmath.vsSub (elementCenter, vmath.bezier (
            (
                startPoint, 
                vmath.vsAdd (startPoint, vmath.vsMulScalar (control1Direction, rightHalfScale)), 
                vmath.vsAdd (endPoint, vmath.vsMulScalar (control2Direction, rightHalfScale)), 
                endPoint
            ), 0.5
        )))
        if errLeftHalf < errRightHalf:
            return Path._rasterizeBezierSegmentFindScale (startPoint, control1Direction, control2Direction, endPoint, elementCenter, minScale, centerScale)
        else:
            return Path._rasterizeBezierSegmentFindScale (startPoint, control1Direction, control2Direction, endPoint, elementCenter, centerScale, maxScale)


    @staticmethod
    def _findCurvePointNearestToBezier(bezierPoint, element, minT, maxT):
        centerT = (minT + maxT) / 2
        if (maxT - minT) < 0.0000001:
            return centerT
        
        leftHalfScale = (minT + centerT) / 2
        errLeftHalf = vmath.vsLength (vmath.vsSub (bezierPoint, element.pointAt (leftHalfScale)))
        rightHalfScale = (centerT + maxT) / 2
        errRightHalf = vmath.vsLength (vmath.vsSub (bezierPoint, element.pointAt (rightHalfScale)))

        if errLeftHalf < errRightHalf:
            return Path._findCurvePointNearestToBezier (bezierPoint, element, minT, centerT)
        else:
            return Path._findCurvePointNearestToBezier (bezierPoint, element, centerT, maxT)


    def _rasterizeBezierSegment (self, points, element, minT, maxT, maxError, noSplit = False):
        minDelta = 0.000000001
        angleDelta = 0.0000000001
        dist = maxT - minT
        centerT = (minT + maxT) / 2
        if dist < minDelta:
            # TODO: do not split segment anymore
            noSplit = True

        # create start and end points
        startPoint = element.pointAt (minT)
        endPoint = element.pointAt (maxT)
        seDist = vmath.vsLength (vmath.vsSub (startPoint, endPoint))
        
        # calculate control point distances to match the angles at the end points and scale
        if minT < angleDelta:
            cp1Direction = vmath.vsSub (element.pointAt (minT + angleDelta), startPoint)
        else:
            cp1Direction = vmath.vsSub (element.pointAt (minT + angleDelta), element.pointAt (minT - angleDelta))
        if maxT + angleDelta > 1.0:
            cp2Direction = vmath.vsSub (element.pointAt (maxT - angleDelta), endPoint)
        else:
            cp2Direction = vmath.vsSub (element.pointAt (maxT - angleDelta), element.pointAt (maxT + angleDelta))

        # scale control point directions
        cpd1 = vmath.vsLength (cp1Direction)
        cpd2 = vmath.vsLength (cp2Direction)
        assert cpd1 > 0
        assert cpd2 > 0
        cp1Direction = vmath.vsMulScalar (cp1Direction, (seDist / cpd1))
        cp2Direction = vmath.vsMulScalar (cp2Direction, (seDist / cpd2))
        scale = Path._rasterizeBezierSegmentFindScale (startPoint, cp1Direction, cp2Direction, endPoint, element.pointAt (centerT), 0, 1)
        cp1Direction = vmath.vsMulScalar (cp1Direction, scale)
        cp2Direction = vmath.vsMulScalar (cp2Direction, scale)
        controlPoint1 = vmath.vsAdd (startPoint, cp1Direction)
        controlPoint2 = vmath.vsAdd (endPoint, cp2Direction)

        # determine distance at 0.5, 0.25 and 0.75 ...
        if not noSplit:
            bezierCurve = (startPoint, controlPoint1, controlPoint2, endPoint)
            noSplit = True
            # check if we could match the center within accuracy limit
            if vmath.vsLength (vmath.vsSub (vmath.bezier (bezierCurve, 0.5), element.pointAt (centerT))) > maxError:
                noSplit = False        
            # check if we could match the left half within accuracy limit
            elif vmath.vsLength (vmath.vsSub (vmath.bezier (bezierCurve, 0.25), element.pointAt (Path._findCurvePointNearestToBezier(vmath.bezier (bezierCurve, 0.25), element, minT, maxT)))) > maxError:
                noSplit = False        
            # check if we could match the right half within accuracy limit
            elif vmath.vsLength (vmath.vsSub (vmath.bezier (bezierCurve, 0.75), element.pointAt (Path._findCurvePointNearestToBezier(vmath.bezier (bezierCurve, 0.75), element, minT, maxT)))) > maxError:
                noSplit = False        

        # need to split curves?
        if not noSplit:
                self._rasterizeBezierSegment (points, element, minT, centerT, maxError)                
                self._rasterizeBezierSegment (points, element, centerT, maxT, maxError)                
                return

        # add curve segment
        points.append (startPoint)
        points.append (controlPoint1)
        points.append (controlPoint2)
        points.append (endPoint)
