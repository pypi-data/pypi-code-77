import math
import copy
from .. import constants
from .. import tree
from .. import shape
from .. import solid
from .. import boolean
from .. import transform
from ..attributes import Attributes
from ..util import differentialdrawing
from ..util import matrix
from ..util import hash
from ..util import cache



class Geometry:
    """
    Basic geometry of a gear part.
    """
    def __init__ (self,
                    n = 20,                         # number of tooth               (de: Zahnanzahl)
                    m = None,                       # module                        (de: Modul)
                    d0 = None,                      # base circle diameter          (de: Teilkreisdurchmesser)
                    da = None,                      # addendum circle diameter      (de: Kopfkreisdurchmesser)
                    p0 = None,                      # circular pitch                (de: Umfangsteilung)
                    x = None,                       # profile shift factor          (de: Profilverschiebungsfaktor)
                    a = 20,                         # standard pressure angle       (de: Normaleingriffswinkel)
                    b = 0,                          # helix angle                   (de: Schrägungswinkel)
                    innerGear = False               # create shape for inner gears  (de: Umriss für innenverzahnung erzeugen)
        ):

        #: Number of tooth.
        self.n = n

        # calculate m, d0, da and p0
        if m != None:
            assert p0 == None, "parameter p0 is not accepted when parameter m is used"
            assert d0 == None, "parameter d0 is not accepted when parameter m is used"
            assert da == None, "parameter da is not accepted when parameter m is used"
            _m = m
            _p0 = math.pi * m
            _d0 = _m * self.n
            _da = _m * (self.n + 2)
        else:
            if (p0 != None):
                assert d0 == None, "parameter d0 is not accepted when parameter p0 is used"
                assert da == None, "parameter da is not accepted when parameter p0 is used"
                _m = p0 / math.pi
                _p0 = p0
                _d0 = _m * self.n
                _da = _m * (self.n + 2)
            else:
                if d0 != None:
                    assert da == None, "parameter da is not accepted when parameter d0 is used"
                    _m = d0 / self.n
                    _p0 = _m * math.pi
                    _d0 = d0
                    _da = _m * (self.n + 2)
                elif da != None:
                    _m = da / (self.n + 2)
                    _p0 = _m * math.pi
                    _d0 = _m * self.n
                    _da = da
                else:
                    pStr = "n = " + str (n) + ", "
                    pStr += "m = " + str (m) + ", "
                    pStr += "d0 = " + str (d0) + ", "
                    pStr += "da = " + str (da) + ", "
                    pStr += "p0 = " + str (p0) + ", "
                    pStr += "x = " + str (x) + ", "
                    pStr += "a = " + str (a) + ", "
                    pStr += "b = " + str (b)
                    assert False, "can not calculate parameter m: " + pStr

        #: Module of gear.
        self.m = _m

        #: Circular pitch.
        self.p0 = _p0

        #: Base circle diameter.
        self.d0 = _d0

        #: Addendum circle diameter.
        self.da = _da

        # profile shift
        if x == None:
            if self.n < 16:
                _x = 1 - (self.n / 17)
            else:
                _x = 0
        else:
            _x = x

        #: Profile shifting factor.
        self.x = _x

        # TODO: rewirte values alpha and beta to be in degree.
        degToRad = math.pi / 180.0

        _alpha = 20 * degToRad
        if a != None:
            _alpha = a * degToRad

        #: Standard pressure angle.
        self.a = _alpha

        _beta = 0
        if b != None:
            _beta = b * degToRad

        #: Helix angle.
        self.b = _beta

        # Create geometry for inner gear
        self.innerGear = innerGear


    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            'n',
            'm',
            'x',
            'a',
            'b'
        )



# TODO: make methods and variables private
# TODO: add base class shape.Shape (and add function getDimensions)
class Profile (shape.Complex, Geometry):
    """
    Profile of a gear wheel.
    """
    def __init__(self, 
                    n = 20,                         # number of tooth               (de: Zahnanzahl)
                    m = None,                       # module                        (de: Modul)
                    d0 = None,                      # base circle diameter          (de: Teilkreisdurchmesser)
                    da = None,                      # addendum circle diameter      (de: Kopfkreisdurchmesser)
                    p0 = None,                      # circular pitch                (de: Umfangsteilung)
                    x = None,                       # profile shift factor          (de: Profilverschiebungsfaktor)
                    a = 20,                         # standard pressure angle       (de: Normaleingriffswinkel)
                    b = 0,                          # helix angle                   (de: Schrägungswinkel)
                    mhf = 0.2,                      # factor of minimum tooth width (de: Faktor für minimale Zahnkopfbreite)
                    rot = 0,                        # rotate gear wheel             (de: Rotation des Zahnrads)
                    innerGear = False,              # create shape for inner gears  (de: Umriss für innenverzahnung erzeugen)
                    name: str = None,               # name of shape
                    attributes:Attributes = None,   # attributes of shape
        ):
        """
        Creates a basic gear wheel geometrie.

        Possible combination of parameters:
        n & m,
        n & d0,
        n & da,
        n & p0

        All other parameters will be calculated
        """
        shape.Complex.__init__ (self, name = name, attributes = attributes)
        Geometry.__init__ (
            self,
            n = n,
            m = m,
            d0 = d0,
            da = da,
            p0 = p0,
            x = x,
            a = a,
            b = b
        )

        #: Boolean flag: is inner gear.
        self.innerGear = innerGear

        # Clearance value.
        self.c = 0.167 * self.m

        #: Rotation of gear wheel in degree.
        self.rot = rot

        # Absolute helix angle.
        betaAbs = self.b if self.b > 0 else -self.b

        #: Base circle diameter
        self.db = self.d0 * math.cos (math.atan (math.tan (self.a) / math.cos (betaAbs)))

        # Precalculated profile shift offset
        self.v = self.x * self.m

        # Correct addendum circle with profile shift
        self.da += 2 * self.v

        # Tip shortening
        maxDa = (self._centerDistanceToNonCorrected () - ((self.d0 / 2) - self.m)) * 2
        if self.da > maxDa:
            self.da = maxDa

        headTopWidth = self._toothWidthAtDiameter (self.da) / 2
        self.mhf = mhf
        if headTopWidth < (mhf * self.m):
            self.da = self._findDiameterForWidth (self.d0, self.da, mhf * self.m * 2)

        # Pre calculations
        # TODO: make names private
        self.rb = self.db / 2
        self.r0 = self.d0 / 2
        self.ra = self.da / 2
        self.p0 = math.pi * self.m
        self.rho_ra = math.acos (self.rb / self.ra)
        self.rho_r0 = math.acos (self.rb / self.r0)
        self.headAngleExtend = self._toothAngleAtDiameter (self.da)
        self.toothAngleAtD0 = self._toothAngleAtDiameter (self.d0)
        self.toothAngleAtBase = self._toothAngleAtDiameter (self.db)


    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            shape.Complex,
            Geometry,
            'mhf',
            'innerGear',
            'rot',
            'name',
            'attributes'
        )


    def _involute (self, a):
        """
        Involute function.
        """
        return math.tan (a) - a


    def _solveInvolute (self, invA):
        """
        Solve involute function.
        """
        if (invA < -2) or (invA > 2):
            aLast = math.atan (invA)
        else:
            aLast = math.pow (3 * invA, 1.0 / 3.0) - (2.0 / 5.0) * invA
        maxIterations = 50
        while (maxIterations > 0):
            at = math.tan (aLast)
            aNext = aLast + ((invA - at + aLast) / (at * at))
            absError = aNext - aLast
            if absError < 0:
                absError = -absError
            if absError < 0.00000000001:
                return aNext
            aLast = aNext
            maxIterations -= 1
        assert False, "solver not converging"


    def centerDistance (self, other):
        """
        Calculates the center distance between two gear wheels.
        """
        assert (self.m == other.m), "gear wheels must have the same module"
        assert (self.a == other.a), "gear wheels must have the same module"
        if self.innerGear and other.innerGear:
            assert False, "can not pair two inner gear wheels"
        if other.innerGear:
            return self._centerDistanceWithInner (other)
        if self.innerGear:
            return other._centerDistanceWithInner (self)
        assert (self.b == -other.b), "gear wheels must have opposit helix angles"
        return self._centerDistanceNonInner (other)


    def _centerDistanceNonInner (self, other):
        invAb = 2 * ((self.x + other.x) / (self.n + other.n)) * math.tan (self.a) + self._involute (self.a)
        ab = self._solveInvolute (invAb)
        return self.m * (self.n + other.n) * (math.cos (self.a) / (2 * math.cos (ab)))


    def _centerDistanceWithInner (self, inner):
        """
        Calculate the center distance between a gear and an inner gear.
        """
        if inner.x < self.x:
            assert False, "inner gear must have at least the same profile shift factor than gear"
        innerDist = inner._centerDistanceNonInner (inner)
        gearDist = self._centerDistanceNonInner (inner)
        return innerDist - gearDist


    def _centerDistanceToNonCorrected (self):
        """
        Calculates the center distance between this gear wheel and non corrected gear wheel with same parameters.
        """
        invAb = 2 * (self.x / (2 * self.n)) * math.tan (self.a) + self._involute (self.a)
        ab = self._solveInvolute (invAb)
        return self.m * (2 * self.n) * (math.cos (self.a) / (2 * math.cos (ab)))


    def _toothWidthAtDiameter (self, diameter):
        """
        Calculate width of tooth for a diameter.
        """
        ac = (self.d0 / diameter) * math.cos (self.a)
        if ac > 1:
            ac = 1
        a = math.acos (ac)
        invA = self._involute (a)
        invA0 = self._involute (self.a)
        x = self.x
        s0 = self.m * ((math.pi / 2) + (2 * x * math.tan (self.a)))
        return diameter * ((s0 / self.d0) + invA0 - invA)


    def _findDiameterForWidth (self, min, max, width):
        """
        Find the gear wheels diameter for a tooth width.
        """
        center = (min + max) / 2
        if (max - min) < 0.0000000000001:
            return center
        d = self._toothWidthAtDiameter (center)
        if d < width:
            return self._findDiameterForWidth (min, center, width)
        else:
            return self._findDiameterForWidth (center, max, width)


    def _toothAngleAtDiameter (self, diameter):
        """
        Calculate angle of tooth at a diameter.
        """
        if self.innerGear:
            if diameter < self.d0:
                mirroredDiameter = 2 * self.d0 - diameter
                a = (self._toothWidthAtDiameter (mirroredDiameter) / 2) / (mirroredDiameter / 2)
                return (2 * self.toothAngleAtD0 - a)
        else:
            if diameter < self.db:
                mirroredDiameter = 2 * self.db - diameter
                a = (self._toothWidthAtDiameter (mirroredDiameter) / 2) / (mirroredDiameter / 2)
                return (2 * self.toothAngleAtBase - a)
        return (self._toothWidthAtDiameter (diameter) / 2) / (diameter / 2)


    def _toothFlankDDA (self, diameter, leftSide, rotate = 0):
        """
        Caclulate evolvent point for a diameter.
        """
        r = diameter / 2
        a = self._toothAngleAtDiameter (diameter)
        return (
            -math.sin (a + rotate) * r if leftSide else math.sin (a + rotate) * r,
            math.cos (a + rotate) * r
        )


    def _undercut (self, angle, mirror = False):
        """
        Calculate undercut point for an angle.
        """
        toothWidth = (self.p0 / 2) - ((self.m + self.c / 2) * math.tan (self.a) * 2)
        toothWidthHalf = toothWidth / 2
        abroll = self.r0 * angle
        if angle > 0:
            cpX = abroll + toothWidthHalf
        else:
            cpX = abroll - toothWidthHalf
        cpY = self.r0 + self.v - (self.m + self.c / 2)
        cp = (-cpX, cpY)
        rot = matrix.AffineRotate2D (-angle * 180 / math.pi)
        rp = matrix.transformPoint2D (rot, cp)
        if mirror:
            return (-rp[0], rp[1])
        else:
            return rp


    def _undercutToEvolventDist (self, angle):
        """
        Calculate distance between undercut and evolvent for an angle.
        """
        up = self._undercut (angle)
        distFromCenter = math.sqrt (up[0] * up[0] + up[1] * up[1])
        upAngle = math.atan2 (up[0], up[1])
        toothAngle = self._toothAngleAtDiameter (distFromCenter * 2) - math.pi / self.n
        angleDiff = upAngle - toothAngle
        return angleDiff * distFromCenter


    def _findUndercutEvolventCuttingAngleNearest (self, min = 0, max = math.pi):
        """
        Find nearest cutting point between undercut and evolvent.
        """
        center = (max + min) / 2
        if (max - min) < 0.0000000000001:
            return center
        distLeft = self._undercutToEvolventDist ((min + center) / 2)
        distRight = self._undercutToEvolventDist ((max + center) / 2)
        if distLeft < distRight:
            return self._findUndercutEvolventCuttingAngleNearest (min, center)
        else:
            return self._findUndercutEvolventCuttingAngleNearest (center, max)


    def _findUndercutEvolventCuttingAngle (self, min = 0, max = math.pi):
        """
        Find cutting point between undercut and evolvent.
        """
        center = (max + min) / 2
        dist = self._undercutToEvolventDist (center)
        if (max - min) < 0.0000000000001:
            absDist = dist if dist > 0 else -dist
            if absDist > 0.000000001:
                return None
            return center
        if dist > 0:
            return self._findUndercutEvolventCuttingAngle (min, center)
        else:
            return self._findUndercutEvolventCuttingAngle (center, max)


    def _calculateUndercutAngle (self, phi):
        """
        Calculate undercut line angle for a angle on the gear wheel.
        """
        p1 = self._undercut (phi + 0.0000000000001, True)
        p2 = self._undercut (phi + 0.000000001, True)
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        return math.atan2 (dy, dx)


    def _findUndercutInnerAngleLimit (self, min, max):
        """
        Find angle on gear wheel where the undercut line sould switch to a circle.
        """
        center = (min + max) / 2
        if (max - min) < 0.0000000000001:
            return center
        angle = self._calculateUndercutAngle (center)
        if angle < (math.pi / 4):
            return self._findUndercutInnerAngleLimit (center, max)
        else:
            return self._findUndercutInnerAngleLimit (min, center)


    def _generateDDA(self):
        """
        Create a differential drawing analyzer for a single tooth.
        """
        # build gear wheel or inner gear wheel
        if self.innerGear:
            toothStartDiameter = self.d0 - self.m
        else:
            # calculate undercut start position
            undercutAngle = self._findUndercutEvolventCuttingAngle ()
            if undercutAngle == None:
                undercutAngle = self._findUndercutEvolventCuttingAngleNearest ()
            assert undercutAngle != None, "undercut doesn't cross evolvent"
            undercutBeginPoint = self._undercut (undercutAngle)
            toothStartDiameter = math.sqrt (undercutBeginPoint[0] * undercutBeginPoint[0] + undercutBeginPoint[1] * undercutBeginPoint[1]) * 2
            undercutInnerAngleLimit = self._findUndercutInnerAngleLimit (0, undercutAngle)

            # create undercut
            undercutDDARight = differentialdrawing.Element(undercutAngle, undercutInnerAngleLimit, lambda a: self._undercut (a, True))
            undercutDDALeft = differentialdrawing.Element(-undercutInnerAngleLimit, -undercutAngle, lambda a: self._undercut (a, True))

            # create tooth clearance
            toothClearanceAnchestorAngle = self._calculateUndercutAngle (undercutInnerAngleLimit)

            # width of clearance area
            clearancePoint1 = undercutDDARight.pointAt (1)
            clearancePoint2 = undercutDDALeft.pointAt (0)
            tcDX = clearancePoint1[0] - clearancePoint2[0]
            tcDY = clearancePoint1[1] - clearancePoint2[1]
            toothClearanceAnchestorWidth = math.sqrt (tcDX * tcDX + tcDY * tcDY)
            toothClearanceDDA = _ToothClearanceDDA (self, toothClearanceAnchestorAngle, toothClearanceAnchestorWidth, clearancePoint1[1])

        toothEndDiameter = self.da
        toothRot = math.pi / self.n

        # create tooth with head
        leftFlankDDA = differentialdrawing.Element (toothEndDiameter, toothStartDiameter, lambda d: self._toothFlankDDA (d, True, -toothRot))
        rightFlankDDA = differentialdrawing.Element (toothStartDiameter, toothEndDiameter, lambda d: self._toothFlankDDA (d, False, toothRot))
        if self.innerGear:
            # create head clearance (inverse)
            innerCleareanceBeginPoint = leftFlankDDA.pointAt (0)
            innerCleareanceEndPoint = rightFlankDDA.pointAt (1)
            icDX = innerCleareanceBeginPoint[0] - innerCleareanceEndPoint[0]
            icDY = innerCleareanceBeginPoint[1] - innerCleareanceEndPoint[1]
            innerClearanceAnchestorWidth = math.sqrt (icDX * icDX + icDY * icDY)
            innerCleareanceAngleP1 = self._toothFlankDDA (self.da, True)
            innerCleareanceAngleP2 = self._toothFlankDDA (self.da - 0.000000001, True)
            innerClearanceAnchestorDx = innerCleareanceAngleP1[0] - innerCleareanceAngleP2[0]
            innerClearanceAnchestorDy = innerCleareanceAngleP1[1] - innerCleareanceAngleP2[1]
            innerClearanceAnchestorAngle = math.atan2 (innerClearanceAnchestorDy, innerClearanceAnchestorDx)
            headDDA = _InnerToothClearanceDDA(self, innerClearanceAnchestorAngle, innerClearanceAnchestorWidth, innerCleareanceAngleP1[1], toothRot)
        else:
            headDDA = differentialdrawing.Element (self.headAngleExtend, -self.headAngleExtend, lambda a: (math.sin (a + toothRot) * self.ra, math.cos (a + toothRot) * self.ra))

        # rasterize points of a single tooth
        if self.innerGear:
            innerRadius = self.r0 - (self.m / 2)
            innerBeginAngle = self._toothAngleAtDiameter (innerRadius * 2) - toothRot
            innerToothBase = differentialdrawing.Element (-innerBeginAngle, innerBeginAngle, lambda a: (math.sin (a) * innerRadius, math.cos (a) * innerRadius))
            dda = differentialdrawing.Path ([rightFlankDDA, headDDA, leftFlankDDA, innerToothBase])
        else:
            dda = differentialdrawing.Path ([rightFlankDDA, headDDA, leftFlankDDA, undercutDDARight, toothClearanceDDA, undercutDDALeft])
        return dda


    def _rasterize(self, resolvedAttributes, asBezier):

        """
        Create rasterized shape of gear wheel.
        """
        # get rasterizing attributes
        minAngle, minSize, fixedCount, minSlices = resolvedAttributes.rasterizingAttributes ()

        # compute element hash and try to load from cache
        ownHash = hash ("rasterized-gearwheel-profile", self, minSize, asBezier)
        cached = cache.load (ownHash, 'item')
        if cached != None:
            return cached

        # create DDA and rasterize element
        ddas = self._generateDDA ()
        if asBezier:
            toothPoints = ddas._rasterizeBezier (2, minSize, False)
        else:
            toothPoints = ddas._rasterize (2, minSize)

        # copy for each tooth
        points = []
        for tooth in range (0, self.n):
            rotAngle = (360.0 / self.n) * tooth + self.rot
            if rotAngle < 180:
                rotAngle = rotAngle + 360
            rotateMatrix = matrix.AffineRotate2D (rotAngle)
            if (len (points) > 0) and asBezier:
                # create closing element between last tooth and current one
                closingEndCurve = []
                for pindex in range (0, 4):
                    closingEndCurve.append (matrix.transformPoint2D(rotateMatrix, toothPoints[pindex]))
                closingCurve = differentialdrawing.Path._createConnectionBezier (points, closingEndCurve)
                if closingCurve != None:
                    points = points + closingCurve
            for pindex in range (0, len (toothPoints)):
                # process current tooth
                points.append (matrix.transformPoint2D(rotateMatrix, toothPoints[pindex]))
        if asBezier:
            # close curve
            closingCurve = differentialdrawing.Path._createConnectionBezier (points, points)
            if closingCurve != None:
                points = points + closingCurve

        # TODO: need to copy attributes?
        if asBezier:
            # TODO: get curves in right format
            assert False
            curves = None
            generated = shape.Bezier (curves)
        else:
            generated = shape.Polygon (points = points, name = self.name, attributes = self.attributes)

        # store to cache an return
        cache.store (generated, ownHash, 'item')
        return generated


    def _toPolygon (self, rasterizingAttributes: Attributes):
        """
        Rasterize gear profile to Polygon.
        """
        return self._rasterize (rasterizingAttributes, False)


    def _toBezier (self, rasterizingAttributes: Attributes):
        """
        Rasterize gear profile to Bezier shape.
        """
        return self._rasterize (rasterizingAttributes, True)




class _ToothClearanceDDA (differentialdrawing.Element):
    """
    DDA for creating tooth clearance.
    """
    def __init__(self, gearwheel, anchestorAngle, anchestorWidth, anchestorDistance):
        super ().__init__ (-1, 1)
        self.gearwheel = gearwheel
        self.radius = anchestorWidth / (2 * math.sin (anchestorAngle))
        self.anchestorAngle = anchestorAngle
        self.centerDist = anchestorDistance + math.cos (anchestorAngle) * self.radius


    def pointAt (self, t):
        nt = (t - 0.5) * 2
        at = -self.anchestorAngle * nt
        distFromZero = nt
        if distFromZero < 0:
            distFromZero = -distFromZero
        yt = math.cos (at) * self.radius
        if yt < 0:
            yt = -yt
        y = self.centerDist - yt
        x = -math.sin (at) * self.radius
        return (-x, y)




class _InnerToothClearanceDDA (differentialdrawing.Element):
    """
    DDA for creating tooth clearance for inner gears.
    """
    def __init__(self, gearwheel, anchestorAngle, anchestorWidth, anchestorDistance, toothRot):
        super ().__init__ (-1, 1)
        self.gearwheel = gearwheel
        self.radius = anchestorWidth / (2 * math.sin (anchestorAngle))
        self.anchestorAngle = anchestorAngle
        self.centerDist = anchestorDistance - math.cos (self.anchestorAngle) * self.radius
        self.rotMatrix = matrix.AffineRotate2D (-toothRot * 180 / math.pi)


    def pointAt (self, t):
        nt = -(t - 0.5) * 2
        at = nt * self.anchestorAngle
        atAbs = at if at > 0 else -at
        cp = (
            math.sin (at) * self.radius,
            math.cos (atAbs) * self.radius + self.centerDist
        )
        return matrix.transformPoint2D (self.rotMatrix, cp)




class Wheel (solid.LinearExtrude, Geometry):
    """
    Gear wheel as :ref:`Solid<Solid>`.
    """
    def __init__ (self,
                    n = 20,                         # number of tooth               (de: Zahnanzahl)
                    m = None,                       # module                        (de: Modul)
                    height = 1,                     # height of wheel               (de: Hoehe)
                    d0 = None,                      # base circle diameter          (de: Teilkreisdurchmesser)
                    da = None,                      # addendum circle diameter      (de: Kopfkreisdurchmesser)
                    p0 = None,                      # circular pitch                (de: Umfangsteilung)
                    x = None,                       # profile shift factor          (de: Profilverschiebungsfaktor)
                    a = 20,                         # standard pressure angle       (de: Normaleingriffswinkel)
                    b = 0,                          # helix angle                   (de: Schrägungswinkel)
                    mhf = 0.2,                      # factor of minimum tooth width (de: Faktor für minimale Zahnkopfbreite)
                    rot = 0,                        # rotate gear wheel             (de: Rotation des Zahnrads)
                    children: list = None,          # shape of gearwheel, only for deserialization, will be generated otherwise
                    name: str = None,               # name of shape
                    attributes:Attributes = None,   # attributes of shape
        ):

        # init geometry
        Geometry.__init__ (
            self,
            n = n,
            m = m,
            d0 = d0,
            da = da,
            p0 = p0,
            x = x,
            a = a,
            b = b
        )

        # pre calculate parameters
        twist = self.b * height / m
        postRot = twist / 2

        #: Profile of gear
        self.profile = Profile (
                n = n, 
                m = m,
                d0 = d0,
                da = da,
                p0 = p0,
                x = x,
                a = a,
                b = b,
                mhf = mhf,
                rot = postRot + rot,
                innerGear = False,
                name = name,
                attributes = attributes
            )

        # Create shape if no children are supplied
        if children == None:
            children = (self.profile,)

        # Create linear extruded gear wheel
        solid.LinearExtrude.__init__ (self, children, height = height, twist = twist, name = name, attributes = attributes)

        # TODO: clean up rest of attributes
        self.mhf = mhf
        self.rot = rot

        #: Height of wheel.
        self.height = height


    def axisDistance (self, other):
        """
        Cacluclates the axis distance from this wheel to another.
        """
        return self.profile.centerDistance (other)


    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            Geometry,
            'children',
            'mhf',
            'rot',
            'name',
            'attributes',
            'height'
        )





class HerringboneWheel (boolean.Union, Geometry):
    """
    Herringbone gear wheel as :ref:`Solid<Solid>`.
    """
    def __init__ (self,
                    n = 20,                         # number of tooth               (de: Zahnanzahl)
                    m = None,                       # module                        (de: Modul)
                    height = 1,                     # height of wheel               (de: Hoehe)
                    d0 = None,                      # base circle diameter          (de: Teilkreisdurchmesser)
                    da = None,                      # addendum circle diameter      (de: Kopfkreisdurchmesser)
                    p0 = None,                      # circular pitch                (de: Umfangsteilung)
                    x = None,                       # profile shift factor          (de: Profilverschiebungsfaktor)
                    a = 20,                         # standard pressure angle       (de: Normaleingriffswinkel)
                    b = 0,                          # helix angle                   (de: Schrägungswinkel)
                    mhf = 0.2,                      # factor of minimum tooth width (de: Faktor für minimale Zahnkopfbreite)
                    children: list = None,          # shape of gearwheel, only for deserialization, will be generated otherwise
                    name: str = None,               # name of shape
                    attributes:Attributes = None,   # attributes of shape
        ):

        assert m != None

        # init geometry
        Geometry.__init__ (
            self,
            n = n,
            m = m,
            d0 = d0,
            da = da,
            p0 = p0,
            x = x,
            a = a,
            b = b
        )

        # pre calculate parameters
        twist = self.b * height / m
        postRot = twist / 2

        #: Profile of gear
        self.profile = Profile (
                n = n, 
                m = m,
                d0 = d0,
                da = da,
                p0 = p0,
                x = x,
                a = a,
                b = b,
                mhf = mhf,
                rot = postRot,
                innerGear = False,
                name = name,
                attributes = attributes
            )

        # Create shape if no children are supplied
        if children == None:
            profile1 = self.profile
            profile2 = Profile (
                n = n, 
                m = m,
                d0 = d0,
                da = da,
                p0 = p0,
                x = x,
                a = a,
                b = -b,
                mhf = mhf,
                rot = -postRot,
                innerGear = False,
                name = name,
                attributes = attributes
            )
            h2 = (height / 2) + constants.Epsilon
            h4 = height / 4
            twist = self.b * height / m
            s1 = transform.Translate (
                solid.LinearExtrude (profile1, h2, twist = twist, name = name, attributes = attributes),
                z = h4
            )
            s2 = transform.Translate (
                solid.LinearExtrude (profile2, h2, twist = -twist, name = name, attributes = attributes),
                z = -h4
            )
            children = (s1, s2)

        # Create linear extruded gear wheel
        boolean.Union.__init__ (self, children, name = name, attributes = attributes)

        # TODO: clean up rest of attributes
        self.mhf = mhf

        #: Height of wheel.
        self.height = height


    def axisDistance (self, other):
        """
        Cacluclates the axis distance from this wheel to another.
        """
        return self.profile.centerDistance (other)


    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            Geometry,
            'children',
            'mhf',
            'name',
            'attributes',
            'height'
        )




class InnerWheel (boolean.Difference, Geometry):
    """
    Inner gear wheel as :ref:`Solid<Solid>`.
    """
    def __init__ (self,
                    n = 20,                         # number of tooth               (de: Zahnanzahl)
                    m = None,                       # module                        (de: Modul)
                    height = 1,                     # height of wheel               (de: Hoehe)
                    rimSize = 1,                    # thickness of rim              (de: Randbreite)
                    d0 = None,                      # base circle diameter          (de: Teilkreisdurchmesser)
                    da = None,                      # addendum circle diameter      (de: Kopfkreisdurchmesser)
                    p0 = None,                      # circular pitch                (de: Umfangsteilung)
                    x = None,                       # profile shift factor          (de: Profilverschiebungsfaktor)
                    a = 20,                         # standard pressure angle       (de: Normaleingriffswinkel)
                    b = 0,                          # helix angle                   (de: Schrägungswinkel)
                    mhf = 0.2,                      # factor of minimum tooth width (de: Faktor für minimale Zahnkopfbreite)
                    rot = 0,                        # rotate gear wheel             (de: Rotation des Zahnrads)
                    children: list = None,          # shape of gearwheel, only for deserialization, will be generated otherwise
                    name: str = None,               # name of shape
                    attributes:Attributes = None,   # attributes of shape
        ):

        # init geometry
        Geometry.__init__ (
            self,
            n = n,
            m = m,
            d0 = d0,
            da = da,
            p0 = p0,
            x = x,
            a = a,
            b = b
        )

        # pre calculate parameters
        twist = self.b * height / n
        postRot = twist / 2

        #: Profile of gear
        self.profile = Profile (
                n = n, 
                m = m,
                d0 = d0,
                da = da,
                p0 = p0,
                x = x,
                a = a,
                b = b,
                mhf = mhf,
                rot = postRot + rot,
                innerGear = True,
                name = name,
                attributes = attributes
            )

        # Create shape if no children are supplied
        if children == None:
            outerDiameterMin = self.da + 0.167 * self.m
            outerDiameter = outerDiameterMin + 2 * rimSize

            # outer shape
            cyl = solid.Cylinder (height = height, radius1 = outerDiameter / 2)

            # shape of inner gear wheel
            cutProfile = (self.profile,)

            # inner shape
            inner = solid.LinearExtrude (
                cutProfile,
                height + constants.Epsilon,
                twist
            )

            # create children
            children = (cyl, inner)

        #: Width of rim.
        self.rimSize = rimSize

        # Create linear extruded gear wheel
        boolean.Difference.__init__ (self, children, name = name, attributes = attributes)

        # TODO: clean up rest of attributes
        self.mhf = mhf
        self.rot = rot

        #: Height of wheel.
        self.height = height


    def axisDistance (self, other):
        """
        Cacluclates the axis distance from this wheel to another.
        """
        return self.profile.centerDistance (other)


    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            boolean.Difference,
            Geometry,
            'rimSize',
            'mhf',
            'rot',
            'name',
            'attributes',
            'height'
        )




class InnerHerringboneWheel (boolean.Difference, Geometry):
    """
    Inner Herringbone gear wheel as :ref:`Solid<Solid>`.
    """
    def __init__ (self,
                    n = 20,                         # number of tooth               (de: Zahnanzahl)
                    m = None,                       # module                        (de: Modul)
                    height = 1,                     # height of wheel               (de: Hoehe)
                    rimSize = 1,                    # thickness of rim              (de: Randbreite)
                    d0 = None,                      # base circle diameter          (de: Teilkreisdurchmesser)
                    da = None,                      # addendum circle diameter      (de: Kopfkreisdurchmesser)
                    p0 = None,                      # circular pitch                (de: Umfangsteilung)
                    x = None,                       # profile shift factor          (de: Profilverschiebungsfaktor)
                    a = 20,                         # standard pressure angle       (de: Normaleingriffswinkel)
                    b = 0,                          # helix angle                   (de: Schrägungswinkel)
                    mhf = 0.2,                      # factor of minimum tooth width (de: Faktor für minimale Zahnkopfbreite)
                    children: list = None,          # shape of gearwheel, only for deserialization, will be generated otherwise
                    name: str = None,               # name of shape
                    attributes:Attributes = None,   # attributes of shape
        ):

        # init geometry
        Geometry.__init__ (
            self,
            n = n,
            m = m,
            d0 = d0,
            da = da,
            p0 = p0,
            x = x,
            a = a,
            b = b
        )

        # pre calculate parameters
        twist = self.b * height / m
        postRot = twist / 2

        #: Profile of gear
        self.profile = Profile (
                n = n, 
                m = m,
                d0 = d0,
                da = da,
                p0 = p0,
                x = x,
                a = a,
                b = b,
                mhf = mhf,
                rot = postRot,
                innerGear = True,
                name = name,
                attributes = attributes
            )

        # Create shape if no children are supplied
        if children == None:
            # outer shape
            outerDiameterMin = self.da + 0.167 * self.m
            outerDiameter = outerDiameterMin + 2 * rimSize
            cyl = solid.Cylinder (height = height, radius1 = outerDiameter / 2)

            # inner shapes
            profile1 = self.profile
            profile2 = Profile (
                n = n, 
                m = m,
                d0 = d0,
                da = da,
                p0 = p0,
                x = x,
                a = a,
                b = -b,
                mhf = mhf,
                rot = -postRot,
                innerGear = True,
                name = name,
                attributes = attributes
            )
            h2 = (height / 2) + constants.Epsilon
            h4 = height / 4
            twist = self.b * height / m
            s1 = transform.Translate (
                solid.LinearExtrude (profile1, h2, twist = twist, name = name, attributes = attributes),
                z = h4
            )
            s2 = transform.Translate (
                solid.LinearExtrude (profile2, h2, twist = -twist, name = name, attributes = attributes),
                z = -h4
            )
            children = (cyl, boolean.Union((s1, s2)))

        # Create linear extruded gear wheel
        boolean.Difference.__init__ (self, children = children, name = name, attributes = attributes)

        # TODO: clean up rest of attributes
        self.mhf = mhf

        #: Height of wheel.
        self.height = height


    def axisDistance (self, other):
        """
        Cacluclates the axis distance from this wheel to another.
        """
        return self.profile.centerDistance (other)


    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            boolean.Difference,
            Geometry,
            'rimSize',
            'mhf',
            'name',
            'attributes',
            'height'
        )
