from enum import Enum
from .util import vmath




class PathType(Enum):
    """
    Interpolation type of Path.
    """
    #: Stop animation. Length of the path must be zero.
    STOP = 0

    #: Stop the animation if path length is zero. Curve interpolation else.
    MAY_STOP = 1

    #: Create smooth curve as path.
    CURVE = 2

    #: Create straight line as path.
    LINEAR = 3

    #: Create step response.
    STEP = 4




class Path:
    """
    Path element of an Animation.
    """
    def __init__ (self, relativeTime = None, absolutePosition = None, pathType = PathType.CURVE, absoluteTime = None, relativePosition = None, rounding = None, damping = None):
        assert isinstance (pathType, PathType), "pathType is invalid"
        
        #: Interpolation type of Path.
        self.pathType = pathType

        # Begin position, assigned by Animation from predecessor. When None (default), the value will be taken from the parent Animation.
        self.beginPosition = None

        #: Rounding factor (range 0 to 1). Higher rounding factors look smoother.
        self.rounding = rounding
        if rounding != None:
            assert isinstance (rounding, (int, float)), "rounding must be a number"

        #: Acceleration damping factor (range 0 to 1). Higher damping factors look smoother. When None (default), the value will be taken from the parent Animation.
        self.damping = damping
        if damping != None:
            assert isinstance (damping, (int, float)), "damping must be a number"

        if absoluteTime != None:
            assert relativeTime == None, "not allowed to use absoluteTime together with relativeTime"
            assert isinstance (absoluteTime, (int, float)), "absoluteTime must be a number"
            _absTime = absoluteTime
            _relTime = None
        else:
            assert relativeTime != None, "absoluteTime or relativeTime must be provided"
            assert isinstance (relativeTime, (int, float)), "relativeTime must be a number"
            _absTime = None
            _relTime = relativeTime

        if absolutePosition != None:
            assert relativePosition == None, "not allowed to use absolutePosition together with relativePosition"
            _absPos = absolutePosition
            _relPos = None
        else:
            assert relativePosition != None, "absolutePosition or relativePosition must be provided"
            _absPos = None
            _relPos = relativePosition

        #: Absolute end time of this Path.
        self.absoluteTime = _absTime

        #: Duration of this Path.
        self.relativeTime = _relTime

        #: Absolute end position of this Path.
        self.absolutePosition = _absPos

        #: Relative end position of this Path.
        self.relativePosition = _relPos




class Animation:
    """
    An animation interpolates a control parameter between key frames. The interpolated value can be a vector or a float number.
    """
    def __init__(self, name: str, initialPosition: list, pathes: list = None, rounding: float = 1.0, damping: float = 1.0):
        assert initialPosition != None, "initialPosition must be provided"
        if vmath.isVector (initialPosition) == False:
            assert isinstance (initialPosition, (int, float)), "initialPosition must be a number or vector"

        #: Name of the animation. The name is used to create a key in the :ref:`Attributes<Attributes>` object.
        self.name = name

        #: The initial position of the animation as number or vector.
        self.initialPosition = initialPosition

        # List of pathes
        self.pathes = []

        #: Rounding factor (range 0 to 1). Higher rounding factors look smoother. Default is 1.
        self.rounding = rounding

        #: Acceleration damping factor (range 0 to 1). Higher damping factors look smoother. Default is 1.
        self.damping = damping

        # precomputed values
        self.curveCache = None

        # add pathes
        if pathes != None:
            for path in pathes:
                self.addPath (path)


    def getPosition(self, time):
        """
        Get animation position for a time stamp.
        """
        if time <= 0:
            return self.initialPosition
        if len (self.pathes) == 0:
            return self.initialPosition
        timeLeft = time
        for i in range (0, len (self.pathes)):
            if timeLeft <= self.pathes[i].relativeTime:
                return self._getPathPosition (i, timeLeft)
            timeLeft = timeLeft - self.pathes[i].relativeTime
        return self.getEndPosition ()


    def getAnimationTime(self):
        """
        Get time of animation.
        """
        if len (self.pathes) > 0:
            return self.pathes[len (self.pathes) - 1].absoluteTime
        return 0

    
    def getInitialPosition(self):
        """
        Get initial position of animation.
        """
        return self.initialPosition

    
    def getEndPosition(self):
        """
        Get end position of animation.
        """
        if len (self.pathes) > 0:
            return self.pathes[len (self.pathes) - 1].absolutePosition
        return self.initialPosition


    def path(self, relativeTime = None, absolutePosition = None, pathType = PathType.CURVE, absoluteTime = None, relativePosition = None, rounding = None, damping = None):
        """
        Convenience method to add pathes.
        """
        path = Path (relativeTime, absolutePosition, pathType, absoluteTime, relativePosition, rounding, damping)
        self.addPath (path)
        return self


    def addPath(self, path):
        """
        Adds a path to this animation.
        """
        assert isinstance (path, Path)
        if isinstance (self.initialPosition, (int, float)):
            if path.absolutePosition != None:
                assert isinstance (path.absolutePosition, (int, float)), "absolutePosition of path must match type of initialPosition"
            if path.relativePosition != None:
                assert isinstance (path.relativePosition, (int, float)), "relativePosition of path must match type of initialPosition"
        else:
            if path.absolutePosition != None:
                assert len (path.absolutePosition) == len (self.initialPosition), "absolutePosition of path must match type of initialPosition"
            if path.relativePosition != None:
                assert len (path.relativePosition) == len (self.initialPosition), "relativePosition of path must match type of initialPosition"
        if path.relativeTime == None:
            path.relativeTime = path.absoluteTime - self.getAnimationTime ()
        elif path.absoluteTime == None:
            path.absoluteTime = path.relativeTime + self.getAnimationTime ()
        if path.relativePosition == None:
            path.relativePosition = vmath.vsSub (path.absolutePosition, self.getEndPosition ())
        elif path.absolutePosition == None:
            path.absolutePosition = vmath.vsAdd (path.relativePosition, self.getEndPosition ())
        if path.pathType == PathType.MAY_STOP:
            if path.relativeTime <= 0:
                return
        assert path.relativeTime >= 0, "relativeTime of path must be >= 0"
        path.beginPosition = self.getEndPosition ()
        self.pathes.append (path)
        self._invalidateCaches ()


    def _invalidateCaches(self):
        """
        Animation changed, release cached elements.
        """
        self.curveCache = None


    def _getPathPredecessor(self, index, roundRunning = True):
        """
        Returns the index of a path's neigbour without stop pathes.
        """
        beginIndex = index
        candidate = index - 1
        if candidate < 0:
            candidate = len (self.pathes) - 1
        while candidate != beginIndex:
            path = self.pathes[candidate]
            if not path.pathType in (PathType.STOP, PathType.MAY_STOP):
                return candidate
            candidate = candidate - 1
            if candidate < 0:
                candidate = len (self.pathes) - 1
        return None


    def _getPathSuccessor(self, index, roundRunning = True):
        """
        Returns the index of a path's neigbour without stop pathes.
        """
        beginIndex = index
        candidate = index + 1
        if candidate >= len (self.pathes):
            candidate = 0
        while candidate != beginIndex:
            path = self.pathes[candidate]
            if not path.pathType in (PathType.STOP, PathType.MAY_STOP):
                return candidate
            candidate = candidate + 1
            if candidate >= len (self.pathes):
                candidate = 0
        return None


    def _calculateControlPoint(self, start, end, anchestorStart, anchestorEnd, rounding):
        """
        Compute a control point for a curve
        """
        ownLength = vmath.vsLength (vmath.vsSub (end, start))
        center = vmath.vsMulScalar (vmath.vsAdd (start, end), 0.5)
        direction = vmath.vsNormalize (vmath.vsSub (start, anchestorStart))
        distance = ownLength * rounding * 0.5
        return vmath.vsMulScalar (vmath.vsAdd (vmath.vsAdd (start, vmath.vsMulScalar (direction, distance)), center), 0.5)


    def _createCurve(self, index, predecessor, successor):
        """
        Create curve for a path.
        """
        # TODO: handle special cases like STOP, LINEAR and STEP
        # get local points
        path = self.pathes[index]
        begin = path.beginPosition
        end = path.absolutePosition
        # TODO: need two center points to emulate a line
        center = vmath.vsMulScalar (vmath.vsAdd (begin, end), 0.5)

        # get rounding value
        rounding = self.rounding
        if path.rounding != None:
            rounding = path.rounding

        # compute control points
        p2 = center
        p3 = center
        curved = path.pathType == PathType.CURVE
        if curved:
            # get points of adjacent pathes
            pre = self.pathes[predecessor] if predecessor != None else None
            succ = self.pathes[successor] if successor != None else None
            preBegin = pre.beginPosition if pre != None else None
            preEnd = pre.absolutePosition if pre != None else None
            succBegin = succ.beginPosition if succ != None else None
            succEnd = succ.absolutePosition if succ != None else None
            if (succBegin != None) and (succEnd != None):
                p3 = self._calculateControlPoint(end, begin, succEnd, succBegin, rounding)
            if (preBegin != None) and (preEnd != None):
                p2 = self._calculateControlPoint(begin, end, preBegin, preEnd, rounding)
        return [begin, p2, p3, end]


    def _getCurves(self):
        """
        Get or compute curves for animator.
        """
        if self.curveCache != None:
            return self.curveCache
        curves = []
        roundRunning = True
        for index in range (0, len (self.pathes)):
            predecessor = self._getPathPredecessor (index, roundRunning)
            successor = self._getPathSuccessor (index, roundRunning)
            curves.append (self._createCurve (index, predecessor, successor))
        self.curveCache = curves
        return curves


    def _getPathPosition(self, pathId, timeInPath):
        """
        Get animation position inside path.
        """
        path = self.pathes[pathId]
        relTime = 0
        if path.relativeTime > 0.0001:
            relTime = timeInPath / path.relativeTime
        if path.pathType == PathType.CURVE:
            # bezier interpolation
            curves = self._getCurves ()
            return vmath.bezier (curves[pathId], relTime)
        elif path.pathType == PathType.STOP:
            return path.absolutePosition
        elif path.pathType == PathType.MAY_STOP:
            return path.absolutePosition
        elif path.pathType == PathType.STEP:
            return path.absolutePosition
        else:
            # linear interpolation
            return vmath.vsAdd (vmath.vsMulScalar (path.absolutePosition, relTime), vmath.vsMulScalar (path.beginPosition, 1.0 - relTime))
