import copy
from . import immutable




class Attributes (immutable.DataObject):
    """
    Attributes are immutable dictionaries describing rendering attributes of a csg :ref:`Item<Item>`.
    """
    def __init__ (self, attributes = None):
        # check type of parameters
        if attributes == None:
            entries = {}
        else:
            if isinstance (attributes, dict):
                entries = copy.copy (attributes)
            elif isinstance (attributes, Attributes):
                entries = attributes.entries
            else:
                assert False, "Parameter attributes need to be an attributs, dictorionary or None instance."

        super ().__init__ ()

        # Dictionary containing all attribute assignments.
        self.attributes = entries


    @staticmethod
    def defaults ():
        """
        Returns a default attribute set.
        """
        return Attributes ({
            # camera view vector:
            #   either 
            #       - a tuple (eyeX, eyeY, eyeZ, centerX, centerY, centerZ)
            #       - a tuple (translateX, translateY, translateZ, rotateX, rotateY, rotateZ, distance)
            'camera.view':                      None,

            # camera projection mode
            #   either
            #       - "perspective"
            #       - "orthogonal"
            #       - None: default == perspective
            'camera.projection':                None,

            # render attributes
            'render.width':                     None,       # int > 0, default: 800
            'render.height':                    None,       # int > 0, default: 600
            'render.quality':                   None,       # int range 1 .. 12, 12 is best quality, default: 1
            'render.antialias':                 None,       # int range 1 .. 12, 12 is best quality, default: 1
            'render.view.axis':                 None,       # boolean, default: False
            'render.view.scales':               None,       # boolean, default: False
            'render.view.crosshairs':           None,       # boolean, default: False
            'render.colorScheme':               None,       # string, default: "PcsgTheme"

            # default attributes for rasterizing:
            'rasterize.minAngle':               1,
            'rasterize.minSize':                0.01,
            'rasterize.fixedCount':             None,
            'rasterize.fixedSlices':            None,

            # default attributes for rendering:
            'material':                         None
        })


    def merge (self, childAttributes):
        """
        Merges this attribute set with the child attributes and retruns a new instance.
        """
        if childAttributes == None:
            return self
        newAttrs = copy.copy (self.attributes)
        for key in childAttributes.attributes:
            newAttrs[key] = childAttributes.attributes[key]
        return Attributes (newAttrs)


    def override (self, assignments: dict):
        """
        Creates a copy of this attributes object with altered values.
        """
        newAttrs = copy.copy (self.attributes)
        for key in assignments:
            newAttrs[key] = assignments[key]
        return Attributes (newAttrs)


    def get (self, key):
        """
        Get attribute by key. Returns None if the attribute is not set.
        """
        if not key in self.attributes:
            return None
        return self.attributes[key]


    def getAttribute (self, key, defaultValue = None, typeAssert = None):
        """
        Reads a value from the attributes map, may returns a default value.
        """
        if key in self.attributes:
            value = self.attributes[key]
            if value == None:
                return defaultValue
            if typeAssert != None:
                assert isinstance (value, typeAssert)
                return value
        else:
            return defaultValue


    def cameraAttributes (self):
        """
        Get camera settings from Attributes object.
        See :ref:`camera attributes<CameraAttributes>` for more details.
        """
        view = self.getAttribute ('camera.view', (0, 0, 100, 0, 0, 0), (tuple, list))
        assert len (view) in (6, 7)
        projection = self.getAttribute ('camera.projection', 'perspective', str)
        assert projection in ('orthogonal', 'perspective')
        return {
            'view':             view,
            'projection':       projection
        }


    def renderAttributes (self):
        """
        Returns the resolved render attributes from an Attributes object.
        See :ref:`render attributes<RenderAttributes>` for more details.
        """
        return {
            'width':            self.getAttribute ('render.width', 800, (int, float)),
            'height':           self.getAttribute ('render.height', 600, (int, float)),
            'quality':          self.getAttribute ('render.quality', 1, int),
            'antialias':        self.getAttribute ('render.antialias', 1, int),
            'view.axis':        self.getAttribute ('render.view.axis', False, bool),
            'view.scales':      self.getAttribute ('render.view.scales', False, bool),
            'view.crosshairs':  self.getAttribute ('render.view.crosshairs', False, bool),
            'colorScheme':      self.getAttribute ('render.colorScheme', "PcsgTheme", str)
        }

    
    def rasterizingAttributes (self):
        """
        Returns the resolved rasterizing attributes as tuple: (minAngle, minSize, fixedCount, minSlices).
        Note: not all values may be returned, None is also acceptable for undefined values.
        See :ref:`rasterizing attributes<RasterizingAttributes>` for more details.
        """
        minAngle = self.attributes['rasterize.minAngle'] if 'rasterize.minAngle' in self.attributes else None
        minSize = self.attributes['rasterize.minSize'] if 'rasterize.minSize' in self.attributes else None
        fixedCount = self.attributes['rasterize.fixedCount'] if 'rasterize.fixedCount' in self.attributes else None
        minSlices = self.attributes['rasterize.fixedSlices'] if 'rasterize.fixedSlices' in self.attributes else None
        if minAngle == None:
            minAngle = 10
        if minSize == None:
            minSize = 0.01
        return (minAngle, minSize, fixedCount, minSlices)


    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            'attributes',
        )
