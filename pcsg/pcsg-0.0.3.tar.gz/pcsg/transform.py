from . import tree
from .attributes import Attributes




class Transform:
    """
    Informational base class of :ref:`Transform<Transform>` objects. This empty class is implemented for type matching purposes.
    """
    def __init__ (self):
        #: The number of dimensions is determined from the child instance.      
        self.dimensions = None




class Translate(tree.Node, Transform):
    """
    Translates a :ref:`Shape<Shape>` or :ref:`Solid<Solid>`.

    A translation can be constructed by a vector of the parameters x, y, and z.

    When translating :ref:`Shapes<Shape>` only the x and y parameters must be used, z must be 0 (default value).
    """
    def __init__ (self,
                    children: object = None,
                    vector: tuple = None,
                    x: float = None,
                    y: float = None,
                    z: float = None,
                    name: str = None,
                    attributes: Attributes = None    
        ):

        # assert children are valid
        if isinstance (children, (list, tuple)):
            assert len (children) == 1, "Expected exactly one children object."
            assert isinstance (children[0], tree.Item), "Expected a csg tree item as child."
        else:
            assert isinstance (children, tree.Item), "Expected a csg tree item as child."
            children = (children,)
        dimensions = children[0].dimensions
        if not isinstance (children[0], tree.Empty):
            assert dimensions in (2, 3), "Expected a two or three dimensional child element."
    
        super ().__init__ (children = children, name = name, attributes = attributes)

        # parameter assignments
        if vector != None:
            assert isinstance (vector, (list, tuple)), "Expected vector to be a translation vector."
            assert len (vector) in (0, 1, 2, 3), "Expected vector to be a translation vector."
            assert x == None, "Can not use parameters x and vector together."
            assert y == None, "Can not use parameters y and vector together."
            assert z == None, "Can not use parameters z and vector together."
            x = vector[0] if len (vector) > 0 else 0
            y = vector[1] if len (vector) > 1 else 0
            z = vector[2] if len (vector) > 2 else 0
        if x == None:
            x = 0
        if y == None:
            y = 0
        if z == None:
            z = 0
        assert isinstance (x, (int, float)), "Expected parameter x to be a number"
        assert isinstance (y, (int, float)), "Expected parameter y to be a number"
        assert isinstance (z, (int, float)), "Expected parameter z to be a number"

        # TODO: reactivate this check, currently breaks the resorting in openscad exporter.
#        if dimensions == 2:
#            assert z == 0, "When translating two dimensional objects, parameter z must be 0."

        #: Translation in direction of the x-axis.
        self.x = x

        #: Translation in direction of the y-axis.
        self.y = y

        #: Translation in direction of the z-axis.
        self.z = z

        # The number of dimensions is determined from the child instance.      
        self.dimensions = dimensions

        #: Tuple containing a single :ref:`Shape<Shape>` or :ref:`Solid<Solid>`.
        self.children = self.children


    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            tree.Node,
            'x',
            'y',
            'z'
        )




class Scale(tree.Node, Transform):
    """
    Scales a :ref:`Shape<Shape>` or :ref:`Solid<Solid>`.

    A scale can be constructed by a vector of the parameters sx, sy, and sz.

    When scaling :ref:`Shapes<Shape>` only the sx and sy parameters must be used, sz must be 1 (default value).
    """
    def __init__ (self,
                    children: object = None,
                    vector: tuple = None,
                    sx: float = None,
                    sy: float = None,
                    sz: float = None,
                    name: str = None,
                    attributes: Attributes = None    
        ):

        # assert children are valid
        if isinstance (children, (list, tuple)):
            assert len (children) == 1, "Expected exactly one children object."
            assert isinstance (children[0], tree.Item), "Expected a csg tree item as child."
        else:
            assert isinstance (children, tree.Item), "Expected a csg tree item as child."
            children = (children,)
        dimensions = children[0].dimensions
        if not isinstance (children[0], tree.Empty):
            assert dimensions in (2, 3), "Expected a two or three dimensional child element."
    
        super ().__init__ (children = children, name = name, attributes = attributes)

        # parameter assignments
        if vector != None:
            assert isinstance (vector, (list, tuple)), "Expected vector to be a scale vector."
            assert len (vector) in (0, 1, 2, 3), "Expected vector to be a scale vector."
            assert sx == None, "Can not use parameters sx and vector together."
            assert sy == None, "Can not use parameters sy and vector together."
            assert sz == None, "Can not use parameters sz and vector together."
            sx = vector[0] if len (vector) > 0 else 1
            sy = vector[1] if len (vector) > 1 else 1
            sz = vector[2] if len (vector) > 2 else 1
        if sx == None:
            sx = 1
        if sy == None:
            sy = 1
        if sz == None:
            sz = 1
        assert isinstance (sx, (int, float)), "Expected parameter sx to be a number"
        assert isinstance (sy, (int, float)), "Expected parameter sy to be a number"
        assert isinstance (sz, (int, float)), "Expected parameter sz to be a number"

        if dimensions == 2:
            assert sz == 1, "When translating two dimensional objects, parameter sz must be 1."

        #: Scale in direction of the x-axis.
        self.sx = sx

        #: Scale in direction of the y-axis.
        self.sy = sy

        #: Scale in direction of the z-axis.
        self.sz = sz

        # The number of dimensions is determined from the child instance.      
        self.dimensions = dimensions

        #: Tuple containing a single :ref:`Shape<Shape>` or :ref:`Solid<Solid>`.
        self.children = self.children


    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            tree.Node,
            'sx',
            'sy',
            'sz'
        )




class Rotate(tree.Node, Transform):
    """
    Rotates a :ref:`Shape<Shape>` or :ref:`Solid<Solid>`.

    A rotation can be constructed by a vector of the parameters rx, ry, and rz.
    The rotation applies the 3 angles by rotating around the z axis, followed by a rotation around the y axis, finally a rotation around the x axis will be applied.

    When rotating :ref:`Shapes<Shape>` only the rz parameter is allowed to use, rx and ry must be 0 (default value).
    """
    def __init__ (self,
                    children: object = None,
                    vector: tuple = None,
                    rx: float = None,
                    ry: float = None,
                    rz: float = None,
                    name: str = None,
                    attributes: Attributes = None    
        ):

        # assert children are valid
        if isinstance (children, (list, tuple)):
            assert len (children) == 1, "Expected exactly one children object."
            assert isinstance (children[0], tree.Item), "Expected a csg tree item as child."
        else:
            assert isinstance (children, tree.Item), "Expected a csg tree item as child."
            children = (children,)
        dimensions = children[0].dimensions
        if not isinstance (children[0], tree.Empty):
            assert dimensions in (2, 3), "Expected a two or three dimensional child element."
    
        super ().__init__ (children = children, name = name, attributes = attributes)

        # parameter assignments
        if vector != None:
            assert isinstance (vector, (list, tuple)), "Expected vector to be a rotate vector."
            assert len (vector) in (0, 1, 2, 3), "Expected vector to be a rotate vector."
            assert rx == None, "Can not use parameters rx and vector together."
            assert ry == None, "Can not use parameters ry and vector together."
            assert rz == None, "Can not use parameters rz and vector together."
            rx = vector[0] if len (vector) > 0 else 0
            ry = vector[1] if len (vector) > 1 else 0
            rz = vector[2] if len (vector) > 2 else 0
        if rx == None:
            rx = 0
        if ry == None:
            ry = 0
        if rz == None:
            rz = 0
        assert isinstance (rx, (int, float)), "Expected parameter rx to be a number"
        assert isinstance (ry, (int, float)), "Expected parameter ry to be a number"
        assert isinstance (rz, (int, float)), "Expected parameter rz to be a number"

        if dimensions == 2:
            assert rx == 0, "When translating two dimensional objects, parameter rx must be 0."
            assert ry == 0, "When translating two dimensional objects, parameter ry must be 0."

        #: Rotation around the x-axis in degrees.
        self.rx = rx

        #: Rotation around the y-axis in degrees.
        self.ry = ry

        #: Rotation around the z-axis in degrees.
        self.rz = rz

        # The number of dimensions is determined from the child instance.      
        self.dimensions = dimensions

        #: Tuple containing a single :ref:`Shape<Shape>` or :ref:`Solid<Solid>`.
        self.children = self.children


    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            tree.Node,
            'rx',
            'ry',
            'rz'
        )
