from . import tree
from .attributes import Attributes




class Boolean:
    """
    Informational base class of :ref:`Boolean<Boolean>` objects. This empty class is implemented for type matching purposes.
    """
    def __init__ (self):
        #: The number of dimensions is determined from the child instance.
        self.dimensions = None




class Union(tree.Node, Boolean):
    """
    Combine two or more :ref:`Shapes<Shape>` or :ref:`Solids<Solid>`.
    """
    def __init__ (self,
                    children: object = None,
                    name: str = None,
                    attributes: Attributes = None    
        ):

        # assert children are valid
        if isinstance (children, (list, tuple)):
            assert len (children) >= 2, "Expected at least two children"
            for childId in range (0, len (children)):
                assert isinstance (children[childId], tree.Item), "Expected a csg tree item as child"
        else:
            assert isinstance (children, tree.Item), "Expected a csg tree item as child"
            children = (children,)
    
        tree.Node.__init__ (self, children = children, name = name, attributes = attributes)
      
        # calculate number of required dimensions
        dimensions = None
        for childId in range (0, len (children)):
            child = children[childId]
            if child != None:
                if not isinstance (child, tree.Empty):
                    if dimensions == None:
                        dimensions = child.dimensions
                    else:
                        if child.dimensions != None:
                            assert child.dimensions == dimensions, "Expected child nodes to have the same number of dimensions."

        # The number of dimensions is determined from the child instance.      
        self.dimensions = dimensions
      
        #: Tuple containing at least two :ref:`Shapes<Shape>` or :ref:`Solids<Solid>`.
        self.children = self.children


    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            tree.Node,
        # TODO:
        )




class Difference(tree.Node, Boolean):
    """
    Difference of two :ref:`Shapes<Shape>` or :ref:`Solids<Solid>`.
    """
    def __init__ (self,
                    children: object = None,
                    name: str = None,
                    attributes: Attributes = None    
        ):

        # assert children are valid
        if isinstance (children, (list, tuple)):
            assert len (children) == 2, "Expected two children"
            assert isinstance (children[0], tree.Item), "Expected a csg tree item as child"
            assert isinstance (children[1], tree.Item), "Expected a csg tree item as child"
        else:
            assert isinstance (children, tree.Item), "Expected a csg tree item as child"
            children = (children,)
    
        super ().__init__ (children = children, name = name, attributes = attributes)      
      
        # calculate number of dimensions
        dimensions = children[0].dimensions if children[0] != None else None
        if dimensions == None:
            dimensions = children[1].dimensions if children[1] != None else None
        else:
            if children[1] != None:
                if children[1].dimensions != None:
                    assert children[1].dimensions == dimensions, "Expected both children to have the same number of dimensions." 

        # The number of dimensions is determined from the child instance.
        self.dimensions = dimensions
      
        #: Tuple containing two :ref:`Shapes<Shape>` or :ref:`Solids<Solid>`.
        self.children = self.children


    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            tree.Node,
        )




class Intersection(tree.Node, Boolean):
    """
    Intersection of two :ref:`Shapes<Shape>` or :ref:`Solids<Solid>`.
    """
    def __init__ (self,
                    children: object = None,
                    name: str = None,
                    attributes: Attributes = None    
        ):

        # assert children are valid
        if isinstance (children, (list, tuple)):
            assert len (children) == 2, "Expected two children"
            assert isinstance (children[0], tree.Item), "Expected a csg tree item as child"
            assert isinstance (children[1], tree.Item), "Expected a csg tree item as child"
        else:
            assert isinstance (children, tree.Item), "Expected a csg tree item as child"
            children = (children,)
    
        super ().__init__ (children = children, name = name, attributes = attributes)
      
        # calculate number of dimensions
        dimensions = children[0].dimensions if children[0] != None else None
        if dimensions == None:
            dimensions = children[1].dimensions if children[1] != None else None
        else:
            if children[1] != None:
                if children[1].dimensions != None:
                    assert children[1].dimensions == dimensions, "Expected both children to have the same number of dimensions." 

        # The number of dimensions is determined from the child instance.
        self.dimensions = dimensions

        #: Tuple containing two :ref:`Shapes<Shape>` or :ref:`Solids<Solid>`.
        self.children = self.children


    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            tree.Node,
        )
