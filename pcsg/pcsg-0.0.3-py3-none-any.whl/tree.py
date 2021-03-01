from . import immutable
from .attributes import Attributes




class Item (immutable.DataObject):
   
    """
    Base class for a csg tree items without children.
    """
    def __init__ (self, 
                    name: str = None,
                    attributes: Attributes = None
        ):

        super ().__init__ ()

        # check parameter types
        assert (name == None) or isinstance (name, str), "Expected parameter name to be a string."

        #: String containing the name of the tree element. Note: the name will not be included in the objects hash and will be ignored on comparision.
        self.name = name

        #: Attributes of the tree element. When a dictionary is supplied, 
        #: the attributes will converted to an :ref:`Attribute<Attributes>` object.
        self.attributes = attributes if isinstance (attributes, Attributes) else Attributes(attributes)

        #: Number of dimensions as integer: 2 for :ref:`Shapes<Shape>`, 3 for :ref:`Solids<Solid>`, None for non renderable items.
        self.dimensions = None


    #: List of attributes provided to copy constructor.
    #: Each inherited class shall define a list of member names which are passed to the constructor on copy construction.
    #: For inheritance support, also base classes are accepted inside the list.
    @staticmethod
    def _copyConstructorAttributes ():
        """
        Returns a list of attributes provided to the copy constructor.
        Each inherited class shall define a list of member names which are passed to the constructor on copy construction.
        #: For inheritance support, also base classes are accepted inside the list.
        """
        return (
            'name',
            'attributes',
        )


    #: List of attributes for hash and comparision functions, when  not defined _copyConstructorAttributes will be used.
    @staticmethod
    def _compareAttributes ():
        return (
            'attributes',
        )




class Empty (Item):
    """
    Empty csg node. Used as placeholder when modifying the tree.
    """
    def __init__ (self, 
                    name: str = None,
                    attributes: Attributes = None
        ):
        super ().__init__ (name = name, attributes = attributes)

        #: Dimensions of emtpy csg :ref:`Item<Item>` is always None.
        self.dimensions = None

    @staticmethod
    def _compareAttributes ():
        return ()




class Node (Item):
    """
    Base class for csg tree elements with children.
    """
    def __init__ (self, 
                    children: list = None,
                    name: str = None, 
                    attributes: Attributes = None
        ):

        super ().__init__ (
            name = name,
            attributes = attributes
        )

        # check parameter types
        assert isinstance (children, (list, tuple)), "Expected parameter children to be a list or tuple"
        for child in children:
            assert isinstance (child, Item), "Expected child element to be a tree node"

        #: Tuple of child :ref:`Items<Item>` attached to this tree element.
        #: When a list is is supplied, it will be converted to a tuple.
        self.children = tuple (children)


    #: List of attributes for copy construction
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            Item,
            'children'
        )




class Group (Node):
    """
    Container for csg tree items.
    """
    def __init__ (self,
                    children: list = None,
                    name: str = None, 
                    attributes: Attributes = None
        ):

        super ().__init__ (
            children = children,
            name = name,
            attributes = attributes
        )

        # calculate dimension count
        calculatedDimensions = None
        if children != None:
            if len (children) > 0:
                calculatedDimensions = children[0].dimensions
        for childIndex in range (1, len (children)):
            if calculatedDimensions != children[childIndex].dimensions:
                calculatedDimensions = None
                break

        #: Number of dimensions as integer: automatically derived from children when all children have the same number of dimensions, None otherwise.
        self.dimensions = calculatedDimensions




class Part (Node):
    """
    A manufacturable Part encloses a Solid. This class is used to mark Solids as 3D printable components.
    Parts with the same *partName* must have the *child*, otherwise the export will fail.
    """
    def __init__ (self,
                    children: list = None,
                    partName: str = None,
                    name: str = None,
                    attributes: Attributes = None
        ):

        if isinstance (children, Item):
            children = (children,)

        super ().__init__ (
            children = children,
            name = name if name != None else partName,
            attributes = attributes
        )

        # assert valid child
        assert self.children != None, "Expected a single solid as child"
        assert len (self.children) == 1, "Expected a single solid as child"
        assert self.children[0].dimensions == 3, "Expected a single solid as child"

        #: Name of the part, used to generate manufacturing files.
        self.partName = partName
        assert isinstance (partName, str), "Expected part name to be a string."

        #: Parts always have 3 dimensions.
        self.dimensions = 3


    #: List of attributes for copy construction
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            Node,
            'partName'
        )




class Visitor:
    """
    A visitor is used to analyze or modify a csg tree.
    """
    def __init__ (self):
        self._rules = []
        self._compiledRules = None


    class Context:
        """
        Visitor context. Keeps track of parents and resolved :ref:`Attributes<Attributes>`.
        """
        def __init__ (self, attributes: Attributes):
            self._initialAttributes = attributes
            
            #: Stack of parent items for current item. The stack also contains the current item.
            self.stack = []

            #: List of resolved attributes. The list elements corresponds to the resolved attributes for each stack entry.
            self.resolvedAttributes = []


    def visit (self, item, context):
        """
        Visit a tree item.
        Returns the same item as called on or a modified copy of the tree.
        """
        # check for valid item
        if item == None:
            return None
        assert isinstance (item, Item), "Expected a csg tree item"

        # push parent and resolved attributes on context stack
        context.stack.append (item)
        parentAttributes = context.resolvedAttributes[-1] if len (context.resolvedAttributes) > 0 else context._initialAttributes
        if parentAttributes == None:
            context.resolvedAttributes.append (item.attributes)
        else:
            context.resolvedAttributes.append (parentAttributes.merge (item.attributes))

        # dispatch node entry
        recurseOnChildren = self._dispatchEnter (item, context)

        # recurse on children
        if recurseOnChildren == True:
            children = getattr (item, 'children', None)
            visitedChildren = []
            if children != None:
                assert isinstance (children, (list, tuple)), "Children are expected to be a tuple or list."
                for child in children:
                    childAfterVisit = self.visit (child, context)
                    if childAfterVisit != None:
                        visitedChildren.append (childAfterVisit)

            # compare children before and after visitation, may need to create a new object copy.
            cOldLen = len (children) if children != None else 0
            cNewLen = len (visitedChildren)
            childrenChanged = cOldLen != cNewLen
            if childrenChanged == False:
                if cOldLen > 0:
                    for childId in range (0, len (children)):
                        if children[childId] != visitedChildren[childId]:
                            childrenChanged = True
                            break
            if childrenChanged == True:
                item = item.copy (children = visitedChildren)
        
        # dipatch node leave
        result = self._dispatchLeave (item, context)

        # remove parent and resolved attributes from context stack
        context.stack.pop ()
        context.resolvedAttributes.pop ()
        return result


    def rule (self, nodeType: type, enter = None, leave = None):
        """
        Registers a rule for matching classes.
        Enter and leave are the function called while visiting elements of the nodeType,
        when a function is not defined, the default functions will be invoked.
        """
        self._rules.append ((nodeType, enter, leave))
        self._compiledRules = None


    def defaultEnter (self, item, context):
        """
        Default enter function, called when no rule matches.
        Enter functions will return true if the children of the current item should be visited.
        """
        return True


    def defaultLeave (self, item, context):
        """
        Default leave function, called when no rule matches.
        A visitor could replace the item by returning an other instance. A visitor could also remove the node by returning None.
        The by default keeps the item by returning it.
        """
        return item
    

    def _dispatchEnter (self, item, context):
        """
        Dispatch entry of item via compiled rule set.
        """
        compiled = self._getCompiledRules ()
        for rule in compiled:
            if (rule[0] == None) or self._isInstance (type(item), rule[0]):
                result = True
                if rule[1] != None:
                    return rule[1] (item, context)
        return self.defaultEnter (item, context)
    

    def _dispatchLeave (self, item, context):
        """
        Dispatch leave of item via compiled rule set.
        """
        compiled = self._getCompiledRules ()
        for rule in compiled:
            if (rule[0] == None) or self._isInstance (type(item), rule[0]):
                result = True
                if rule[2] != None:
                    return rule[2] (item, context)
        return self.defaultLeave (item, context)


    def _getCompiledRules (self):        
        """
        Get compiled rules for visitor.
        """
        if (self._compiledRules):
            return self._compiledRules
        flattenedRules = []
        for rule in self._rules:
            if self._isInstance (rule[0], list):
                for t in rule[0]:
                    flattenedRules.append ([t, rule[1], rule[2]])
            else:
                flattenedRules.append (rule)
        self._compiledRules = []
        while len (flattenedRules) > 0:
            self._compiledRules.append (self._compileElement (flattenedRules, 0))
        return self._compiledRules


    def _compileElement (self, rulesLeft, index):
        """
        Pick one rule element in order from rulesLeft list.
        """
        if index >= len (rulesLeft):
            return None
        pivot = rulesLeft[index]
        betterIndex = None
        for i in range (index + 1, len (rulesLeft)):
            if self._compileElementCompare (pivot, rulesLeft[i]):
                betterIndex = i
                break
        if betterIndex == None:
            return rulesLeft.pop (index)
        else:
            return self._compileElement (rulesLeft, betterIndex)


    def _compileElementCompare (self, left, right):
        """
        Check if right element class is derived from left one.
        """
        if left[0] == None:
            return True
        return self._isInstance (right[0], left[0])


    def _isInstance (self, clz, needle):
        """
        Check if a class inherits an other one recursively.
        """
        if clz == needle:
            return True
        for base in clz.__bases__:
            if self._isInstance (base, needle):
                return True
        return False
