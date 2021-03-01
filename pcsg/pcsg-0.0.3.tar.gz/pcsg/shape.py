import math
import inspect
from enum import Enum
from . import tree
from .attributes import Attributes
from .util import cache
from .util import hash




class Shape:
    """
    Informational base class of :ref:`Shape<Shape>` objects. This empty class is implemented for type matching purposes.
    """
    def __init__ (self):
        #: Number of dimensions is always 2 for :ref:`Shapes<Shape>`.
        self.dimensions = 2




class Circle(tree.Item, Shape):
    """
    A Circle is a basic :ref:`Shape<Shape>` class.
    
    The Circle can be definied with the parameter *radius* or *diameter*. Only the radius will be stored.
    The Circles center is at coordinate (0, 0).
    """
    def __init__ (self,
                    radius: float = None,
                    diameter: float = None,
                    name: str = None,
                    attributes: Attributes = None    
        ):
        super ().__init__ (name = name, attributes = attributes)

        # check for valid arguments
        assert (radius != None) or (diameter != None), "Expected parameter radius or diameter"
        assert (radius == None) or (diameter == None), "Parameters radius and diameter can not be used together"
        if diameter != None:
            radius = diameter / 2

        # Number of dimensions is always 2 for :ref:`Shapes<Shape>`.
        self.dimensions = 2

        #: Radius of the circle
        self.radius = radius

    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            tree.Item,
            'radius'
        )




class Square(tree.Item, Shape):
    """
    A Square is a basic :ref:`Shape<Shape>` class.
    
    The Square is defined by a two dimensional size tuple.
    The Squares center is at coordinate (0, 0).
    """
    def __init__ (self,
                    size: tuple = (1, 1),
                    name: str = None,
                    attributes: Attributes = None    
        ):
        super ().__init__ (name = name, attributes = attributes)

        # check for valid size parameter
        assert size != None, "Expected parameter size to be defined"
        if isinstance (size, (int, float)):
            size = (size, size)
        elif isinstance (size, list):
            size = tuple (size)
        elif not isinstance (size, tuple):
            assert False, "Expected size to be a number or a 2 dimensional vector"
        assert len (size) == 2, "Expected size to be a number or a 2 dimensional vector"
        assert isinstance (size[0], (int, float)), "Expected size to be a tuple containing 2 numbers"
        assert isinstance (size[1], (int, float)), "Expected size to be a tuple containing 2 numbers"

        # Number of dimensions is always 2 for :ref:`Shapes<Shape>`.
        self.dimensions = 2

        #: Size of Square as tuple containing (width: float, height: float).
        self.size = size

    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            tree.Item,
            'size'
        )
    



class PolygonInterpolation (Enum):
    """
    .. Interpolation type for :ref:`Polygon<Polygon>` rendering.
    """
    #: The polygon will be redered by connecting all points by straight lines.
    Linear = 1

    #: The polygon will be redered by a quadratic interpolation. For calculating the interpolated curve the following point will be taken into account.
    Quadratic = 2

    #: The polygon will be redered by a cubic interpolation. For calculating the interpolated curve the preceeding and following point will be taken into account.
    Cubic = 3




class Polygon(tree.Item, Shape):
    """
    A Polygon is a basic :ref:`Shape<Shape>` class. 

    The Polygon is defined by a list of point forming a closed shape.
    """
    def __init__ (self,
                    points: object = None,
                    outer: list = None,
                    cutouts: list = None,
                    interpolation: PolygonInterpolation = PolygonInterpolation.Linear,
                    name: str = None,
                    attributes: Attributes = None    
        ):
        super ().__init__ (name = name, attributes = attributes)

        # check for valid points
        assert isinstance (points, (list, tuple)), "Expected parameter points to be a tuple of two dimensional vectors"
        newList = []
        for point in points:
            assert isinstance (point, (list, tuple)), "Expected a point to be a list or tuple-"
            assert len (point) == 2, "Expected a point to have 2 dimensions."
            newList.append (tuple (point))
        points = tuple (newList)

        # check outer shape parameter
        if outer == None:
            assert cutouts == None, "Can not use cutouts when no outer shape is specified."
            outer = tuple (range (0, len (points)))
            cutouts = ()
        else:
            # assert points are valid
            assert isinstance (outer, (list, tuple)), "Outer shape must be a list of point indices."
            for point in outer:
                assert isinstance (point, int), "Expected outer shape to consist of point indices."
                assert (point >= 0) and (point < len (points)), "Invalid point index in outer shape."
            outer = tuple (outer)

            # parse in parameter cutouts
            if cutouts == None:
                cutouts = ()
            else:
                # process cutouts
                assert isinstance (cutouts, (list, tuple)), "Expected cutouts to be a list."
                immutableCutouts = []
                for cutout in cutouts:
                    assert isinstance (cutout, (list, tuple)), "Expected each cutout to be a list of point indices."
                    for point in cutout:
                        assert isinstance (point, int), "Expected each cutout be be a list of point indices."
                        assert (point >= 0) and (point < len (points)), "Invalid point index in cutout shape."
                    immutableCutouts.append (tuple (cutout))
                cutouts = tuple (immutableCutouts)


        # Number of dimensions is always 2 for :ref:`Shapes<Shape>`.
        self.dimensions = 2

        #: Tuple of two dimensional vectors describing all points of the Polygon.
        self.points = points

        #: Point indices used for outer shape.
        self.outer = outer

        #: Point array of tuples containing point indices used for cut out shapes.
        self.cutouts = cutouts

        #: Interpolation type used for rendering.
        self.interpolation = interpolation


    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            tree.Item,
            'points',
            'interpolation',
            'cutouts',
            'outer'
        )
    

    @staticmethod
    def fromShape (shape: tree.Item, rasterizingAttributes: Attributes = None, name: str = None, attributes: Attributes = None):
        """
        Create a Polygon by rasterizing a two dimensional csg tree :ref:`Item<Item>`.
        The accuracy for rasterizing is calculated from *rasterizingAttributes*.
        When the shape has disjunct areas, a :ref:`Group<Group>` of Polygons will be returned.
        When the shape has no renderable items, :ref:`Empty<Empty>` will be returned.
        """
        # check if node is already cached
        newHash = hash (shape, "polygon from shape", rasterizingAttributes)
        loaded = cache.load (newHash, "rsh")
        if loaded != None:
            return loaded.copy (name = name, attributes = attributes)
        
        # compute polygon and add to cache
        poly = _toPolygonsWrapper (shape, rasterizingAttributes)
        cache.store (poly, newHash, "rsh")
        return poly.copy (name = name, attributes = attributes)




class Bezier(tree.Item, Shape):
    """
    A Bezier shape is a basic :ref:`Shape<Shape>` class. 

    The Bezier shape is defined by a list of bezier curves forming a closed shape.
    Each bezier curve is a tuple containing the start point, two control points and the end point of the segment.
    """
    def __init__ (self,
                    curves: object = None,
                    name: str = None,
                    attributes: Attributes = None    
        ):
        super ().__init__ (name = name, attributes = attributes)

        # check for valid points
        assert isinstance (curves, (list, tuple)), "Expected parameter curves to be a tuple of four 2-dimensional vectors."
        if isinstance (curves, list):
            curves = tuple (curves)

        # Number of dimensions is always 2 for :ref:`Shapes<Shape>`.
        self.dimensions = 2

        #: List containing a tuple of 4 points for each bezier segment. A segment consists of four 2-dimensional points: a start point, two control points and an end point.
        self.curves = curves

    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            tree.Item,
            'curves'
        )

    @staticmethod
    def _compareEndToStart (p1, p2):
        """
        Compare the end of a path to the start of the next one
        """

    def isClosed (self):
        """
        Returns True when the Bezier shape has a closed outline, False otherwise.
        """
        # already cached?
        if 'isClosed' in self._cache:
            return self._cache['isClosed']

        # check if shape is closed
        closed = True
        if len (self.curves) > 0:
            for cId in range (0, len (self.curves)):
                nId = cId + 1
                if nId == len (self.curves):
                    nId = 0
                if not Bezier._compareEndToStart (self.curves[cId], self.curves[nId]):
                    closed = False
                    break
        else:
            closed = False

        # store to cache and return
        self._cache['isClosed'] = closed
        return closed




class Projection (tree.Node, Shape):
    """
    Create a :ref:`Shape<Shape>` by projection of a :ref:`Solid<Solid>` on the x/y plane.
    """
    def __init__ (self,
                    children: object = None,
                    cut: bool = True,
                    name: str = None,
                    attributes: Attributes = None    
        ):
        # assert child is valid
        if isinstance (children, (list, tuple)):
            assert len (children) == 1, "Expected exactly one child"
            assert isinstance (children[0], tree.Item), "Expected a csg tree item as child"
        else:
            assert isinstance (children, tree.Item), "Expected a csg tree item as child"
            children = (children,)
        assert children[0].dimensions == 3, "Expected a three dimensional child"
    
        super ().__init__ (children = children, name = name, attributes = attributes)
      
        #: Tuple containing a single child. The child must be a three dimensional csg tree item.
        self.children = children

        # Number of dimensions is always 2 for :ref:`Shapes<Shape>`.
        self.dimensions = 2

        #: When cut is True, the intersection of the child object with the x/y plane with z=0 will be calculated.
        #: When cut is False, an orthogonal projection will be calculated.
        self.cut = cut == True

    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            tree.Node,
            'cut'
        )




class Complex (tree.Item, Shape):
    """
    Base class for implementing complex :ref:`Shapes<Shape>`.
    """
    def __init__ (self,
                    name: str = None,
                    attributes: Attributes = None    
        ):
        super ().__init__ (name, attributes)

        # Number of dimensions is always 2 for :ref:`Shapes<Shape>`.
        self.dimensions = 2


    def _toPolygon (self, rasterizingAttributes: tree.Attributes):
        """
        To be implemented by child class: convert a Complex to a Polygon.
        """
        assert False, "To be implemented by child class"


    def _toBezier (self, rasterizingAttributes: tree.Attributes):
        """
        To be implemented by child class optionally: convert a Complex to a Bezier shape.
        This function may return None when a conversion to a Bezier shape is not possible.
        """
        return None


    def rasterize (self, rasterizingAttributes: tree.Attributes, tryAsBezierShape = False):
        """
        When *tryAsBezierShape* is True, the Complex is rendered as Bezier curve if possible, otherwise it will be rendered as a Polygon. 
        """
        # try to load from cache
        if tryAsBezierShape:
            fingerprint = hash ("complex-mayBezier", self)
        else:
            fingerprint = hash ("complex", self)
        cached = cache.load (fingerprint, 'item')
        if cached != None:
            return cached

        # generate rasterized bezier shape
        if tryAsBezierShape:
            generated = self._toBezierShape (rasterizingAttributes)
        else:
            generated = None

        # generate rasterized polygon
        if generated == None:
            generated = self._toPolygon (rasterizingAttributes)

        # store to cache and return
        cache.store (generated, fingerprint, 'item')
        return generated




class Polar (Complex):
    """
    A :ref:`Shape<Shape>` defined by a polar curve function.
    """
    def __init__ (self,
                    func = None,
                    name: str = None,
                    attributes: Attributes = None    
        ):
        super ().__init__ (name = name, attributes = attributes)

        # TODO: check if func parameter is valid
        assert inspect.isfunction (func), "Expected function as source of polar shape."

        # Number of dimensions is always 2 for :ref:`Shapes<Shape>`.
        self.dimensions = 2

        #: Function mapping a parameter phi in range 0 to 2\*pi to a a radius.
        self.func = func


    def _toPolygon (self, rasterizingAttributes: tree.Attributes):
        return _polarToPolygon (self, rasterizingAttributes)


    def _toBezier (self, rasterizingAttributes: tree.Attributes):
        return _polarToBezier (self, rasterizingAttributes)


    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            Complex,
            'func'
        )




# import algorithms
from . import algorithms
from .util import differentialdrawing




def _toPolygonsWrapper (item: tree.Item, rasterizingAttributes: tree.Attributes):
    """
    Delegate to algorithms.
    """
    return algorithms.toPolygons (item, rasterizingAttributes)




class PolarDDAElement (differentialdrawing.Element):
    """
    Differential drawing element for polar curves
    """
    def __init__ (self, func):
        super ().__init__ ()
        self.func = func

    def pointAt (self, t):
        """
        Calculate point on polar curve.
        """
        phi = t * 2 * math.pi
        radius = self.func (phi)
        return (
            math.sin (phi) * radius,
            math.cos (phi) * radius
        )




def _polarToPolygon (item: Polar, rasterizingAttributes: tree.Attributes):
    """
    Rasterize Polar as Polygon.
    """
    # get rasterizing settings
    minAngle, minSize, fixedCount, minSlices = rasterizingAttributes.rasterizingAttributes ()

    # rasterize bezier shape to polygon
    dda = differentialdrawing.Path ([PolarDDAElement (item.func)])
    return dda.toPolygon (initialSegmentCount = 2, maxStepSize = minSize, name = item.name, attributes = item.attributes)




def _polarToBezier (item: Polar, rasterizingAttributes: tree.Attributes):
    """
    Rasterize Polar as Bezier curve.
    """
    # get rasterizing settings
    minAngle, minSize, fixedCount, minSlices = rasterizingAttributes.rasterizingAttributes ()

    # rasterize bezier shape to polygon
    dda = differentialdrawing.Path ([PolarDDAElement (item.func)])
    return dda.toBezier (initialSegmentCount = 2, maxStepSize = minSize, name = item.name, attributes = item.attributes)
