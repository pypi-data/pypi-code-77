import os
import pathlib
import subprocess
from ... import tree
from ... import shape
from ... import solid
from ... import transform
from ... import boolean
from ... import algorithms
from ... import attributeTypes
from .. import textwriter
from .. import hash
from .. import cache
from .. import downsample




class _TreeIgnoreFilter (algorithms.RemoveNodes):
    """
    Tree ignore filter for removing nodes ignored by OpenScad.
    """
    def __init__ (self):
        super ().__init__ ()

        # node removal filter
        self.rule (tree.Empty, self.enterFilter, self.leaveFilter)

        # TODO: Add attribute '_openscad.material' to each item.
        # This information will be used by the OpenScad tree exporter to determine a rendering color.

"""
Single instance of tree ignore filter.
"""
TreeIgnoreFilter = _TreeIgnoreFilter ()




class _TreeReplaceNonTrivialTypes (tree.Visitor):
    """
    Replaces non trivial tree nodes before rendering.
    """
    def __init__ (self):
        super ().__init__ ()

        # replacement rules
        self.rule (shape.Bezier, leave = self.leaveCurve)
        self.rule (shape.Polar, leave = self.leaveCurve)
        self.rule (shape.Complex, leave = self.leaveComplex)


    def execute (self, item, attributes):
        """
        Collect render attributes for node.
        """
        context = tree.Visitor.Context (attributes)
        return self.visit (item, context)


    def leaveCurve (self, item, context):
        """
        Convert curve to rasterized Polygon
        """
        rasterizingAttributes = context.resolvedAttributes[-1]
        return shape.Polygon.fromShape (item, rasterizingAttributes = rasterizingAttributes, name = item.name, attributes = item.attributes)


    def leaveComplex (self, item, context):
        """
        Convert complex to rasterized Polygon
        """
        rasterizingAttributes = context.resolvedAttributes[-1]
        return item.rasterize (rasterizingAttributes, False)

"""
Single instance of replace non trivial types filter.
"""
TreeReplaceNonTrivialTypes = _TreeReplaceNonTrivialTypes ()




def TreeCollectRenderAttributes (item):
    """
    Collect render attributes for tree node.
    """ 
    # already tagged with a material?   
    if item == None:
        return None
    matAttr = item.attributes.get ('_openscad.material')
    if matAttr != None:
        return item

    matAttr = item.attributes.get ('material')
    if matAttr != None:
        # has own material definition
        if isinstance (item, tree.Node):
            newChildren = []
            for child in item.children:
                newChildren.append (TreeCollectRenderAttributes (child))
            return item.copy (children = newChildren, attributes = item.attributes.override ({'_openscad.material': matAttr}))
        else:
            return item.copy (attributes = item.attributes.override ({'_openscad.material': matAttr}))
    else:
        # get material definition from children
        nAttributes = item.attributes

        # recurse on children
        if isinstance (item, tree.Node):
            newChildren = []
            for child in item.children:
                newChildren.append (TreeCollectRenderAttributes (child))

        if isinstance (item, (solid.LinearExtrude, solid.RotateExtrude, transform.Transform)):
            childAttr = newChildren[0].attributes.get ('_openscad.material')
            if childAttr != None:
                nAttributes = nAttributes.override ({'_openscad.material': childAttr})
        elif isinstance (item, boolean.Union):
            childAttr = None
            mismatch = False
            for child in newChildren:
                tChildAttr = child.attributes.get ('_openscad.material')
                if childAttr != None:
                    if childAttr != tChildAttr:
                        mismatch = True
                    else:
                        childAttr = tChildAttr
            if (mismatch == False) and (childAttr != None):
                nAttributes = nAttributes.override ({'_openscad.material': childAttr})
        elif isinstance (item, (boolean.Difference, boolean.Intersection)):
            childAttr1 = newChildren[0].attributes.get ('_openscad.material')
            childAttr2 = newChildren[1].attributes.get ('_openscad.material')
            if childAttr1 == None:
                if childAttr2 != None:
                    nAttributes = nAttributes.override ({'_openscad.material': childAttr2})
            else:
                nAttributes = nAttributes.override ({'_openscad.material': childAttr1})

        # rebuild node
        if isinstance (item, tree.Node):
            return item.copy (children = newChildren, attributes = nAttributes)
        else:
            return item.copy (attributes = nAttributes)




class _TreeVisitor (tree.Visitor):
    """
    A tree visitor writing an OpenScad script.
    """
    def __init__ (self):
        super ().__init__ ()

        # handle two dimensional basic shapes
        self.rule (shape.Circle, self.enterCircle, self.leaveGeometry)
        self.rule (shape.Square, self.enterSquare, self.leaveGeometry)
        self.rule (shape.Polygon, self.enterPolygon, self.leaveGeometry)
        self.rule (shape.Projection, self.enterProjection, self.leaveProjection)

        # handle three dimensional basic shapes
        self.rule (solid.Sphere, self.enterSphere, self.leaveGeometry)
        self.rule (solid.Cube, self.enterCube, self.leaveGeometry)
        self.rule (solid.Cylinder, self.enterCylinder, self.leaveGeometry)
        self.rule (solid.Polyhedron, self.enterPolyhedron, self.leaveGeometry)
        self.rule (solid.LinearExtrude, self.enterLinearExtrude, self.leaveExtrude)
        self.rule (solid.RotateExtrude, self.enterRotateExtrude, self.leaveExtrude)

        # handle transformations
        self.rule (transform.Translate, self.enterTranslate, self.leaveTransform)
        self.rule (transform.Scale, self.enterScale, self.leaveTransform)
        self.rule (transform.Rotate, self.enterRotate, self.leaveTransform)

        # handle boolean operations
        self.rule (boolean.Union, self.enterUnion, self.leaveUnion)
        self.rule (boolean.Difference, self.enterDifference, self.leaveBoolean)
        self.rule (boolean.Intersection, self.enterIntersection, self.leaveBoolean)

        # handle empty node
        self.rule (tree.Empty, self.enterIgnore, self.leaveIgnore)

        # handle part node
        self.rule (tree.Part, self.enterPart, self.leavePart)


    class Context (tree.Visitor.Context):
        """
        Own context class.
        """
        def __init__ (self, attributes, writer):
            super ().__init__ (attributes)
            self.writer = writer


    def execute (self, item: tree.Item, attributes: dict, writer: textwriter.TextWriter):
        """
        Write a tree as a OpenScad script.
        """
        # Remove unrenderable items, replace non trivial item types, translate groups into unions and remove empty nodes.
        filtered = TreeIgnoreFilter.execute (item, attributes)                      # remove ignored rendering items
        filtered = TreeReplaceNonTrivialTypes.execute (filtered, attributes)        # replace none trivial render items
        filtered = algorithms.groupsToUnions (filtered)                             # rewite groups as unions.
        filtered = algorithms.removeEmpty (filtered)                                # purge empty nodes from item.
        filtered = algorithms.pushTransformsFurtherInside (filtered)                # push transforms to be most inner
        filtered = algorithms.pushExtrusionsFurtherInside (filtered)                # push extrusions to be most inner
        filtered = TreeCollectRenderAttributes (filtered)                           # collect render colors

        # flatten to OpenScad script
        context = _TreeVisitor.Context (attributes, writer)
        self.visit (filtered, context)


    def enterPart (self, item, context):
        """
        Enter tree.Part element.
        """
        return True


    def leavePart (self, item, context):
        """
        Leave tree.Part element.
        """
        return item


    def enterIgnore (self, item, context):
        """
        Ignore item on tree traversal.
        """
        return False


    def leaveIgnore (self, item, context):
        """
        Ignore item on tree traversal.
        """
        return item


    def defaultEnter (self, item, context):
        """
        Handler function for entering non handled types.
        """
        assert False, "Item class not handled."


    def defaultLeave (self, item, context):
        """
        Handler function for leaving non handled types.
        """
        assert False, "Item class not handled."


    def writeComment (self, item, context):
        """
        Write comment for node.
        """
        if item.name != None:
            if item.name != "":
                context.writer.write ("// " + item.name + ":\n")


    def writeAttributes (self, item, context):
        """
        Write attributes for node.
        """
        attributes = context.resolvedAttributes[-1].attributes
        material = attributes['_openscad.material'] if '_openscad.material' in attributes else None
        if material != None:
            context.writer.write ("color ([")
            context.writer.write (str (material[0]))
            context.writer.write (", " + str (material[1]))
            context.writer.write (", " + str (material[2]))
            if len (material) > 3:
                context.writer.write (", " + str (material[3]))
            context.writer.write ("]) \n")


    def endAttributes (self, item, context):
        """
        End processing item with attributes.
        """
        pass


    def formatTesselationParameters (self, item, context):
        """
        Calculates the tesselation parameter string.
        """
        # get rasterizing settings
        minAngle, minSize, fixedCount, minSlices = context.resolvedAttributes[-1].rasterizingAttributes ()
        result = ""
        if fixedCount != None:
            result = ", $fn = " + context.writer.formatNumber (fixedCount)
        else:
            if minAngle != None:
                result += ", $fa = " + context.writer.formatNumber (minAngle)
            if minSize != None:
                result += ", $fs = " + context.writer.formatNumber (minSize)
        return result


    def enterCircle (self, item, context):
        """
        Write a shape.Circle instance.
        """
        self.writeComment (item, context)
        self.writeAttributes (item, context)
        tes = self.formatTesselationParameters (item, context)
        context.writer.write ("circle (r = ")
        context.writer.writeNumber (item.radius)
        context.writer.write (tes + ");\n")
        return True


    def enterSquare (self, item, context):
        """
        Write a shape.Square instance.
        """
        self.writeComment (item, context)
        self.writeAttributes (item, context)
        context.writer.write ("square (size = [")
        context.writer.writeNumber (item.size[0])
        context.writer.write (", ")
        context.writer.writeNumber (item.size[1])
        context.writer.write ("], center = true);\n")
        return True
        

    def writePolygonPath (self, item, path, context):
        """
        Format a polygon path.
        """
        context.writer.write ("[")
        for pid in range (0, len (path)):
            if pid == (len (path) - 1):
                context.writer.write (str (path[pid]))
            else:
                context.writer.write (str (path[pid]) + ", ")
        context.writer.write ("]")


    def enterPolygon (self, item, context):
        """
        Enter a ploygon.
        """
        self.writeComment (item, context)
        self.writeAttributes (item, context)
        context.writer.write ("polygon (points = [")
        context.writer.increaseIndent ()
        self.writePoints2D (item.points, context)
        context.writer.write ("],\n")
        context.writer.decreaseIndent ()
        context.writer.write ("paths = [\n")
        context.writer.increaseIndent ()
        self.writePolygonPath (item, item.outer, context)
        for cutout in item.cutouts:
            context.writer.write (", \n")
            self.writePolygonPath (item, cutout, context)
        context.writer.write ("]);\n")
        context.writer.decreaseIndent ()
        return True
        

    def enterProjection (self, item, context):
        """
        Enter projection.
        """
        self.writeComment (item, context)
        self.writeAttributes (item, context)
        context.writer.write ("projection (cut = ")
        context.writer.write ("true" if item.cut == True else "false")
        context.writer.write (")\n")
        context.writer.increaseIndent ()
        return True


    def leaveProjection (self, item, context):
        """
        Leave projection.
        """
        self.endAttributes (item, context)
        context.writer.decreaseIndent ()
        return item
        

    def enterSphere (self, item, context):
        """
        Write a solid.Sphere instance.
        """
        self.writeComment (item, context)
        self.writeAttributes (item, context)
        tes = self.formatTesselationParameters (item, context)
        context.writer.write ("sphere (r = ")
        context.writer.writeNumber (item.radius)
        context.writer.write (", center = true" + tes + ");\n")
        return True
        

    def enterCube (self, item, context):
        """
        Write a solid.Cube instance.
        """
        self.writeComment (item, context)
        self.writeAttributes (item, context)
        context.writer.write ("cube (size = [")
        context.writer.writeNumber (item.size[0])
        context.writer.write (", ")
        context.writer.writeNumber (item.size[1])
        context.writer.write (", ")
        context.writer.writeNumber (item.size[2])
        context.writer.write ("], center = true);\n")
        return True
        

    def enterCylinder (self, item, context):
        """
        Write a solid.Cylinder instance.
        """
        self.writeComment (item, context)
        self.writeAttributes (item, context)
        tes = self.formatTesselationParameters (item, context)
        context.writer.write ("cylinder (h = ")
        context.writer.writeNumber (item.height)
        context.writer.write (", r1 = ")
        context.writer.writeNumber (item.radius1)
        context.writer.write (", r2 = ")
        context.writer.writeNumber (item.radius2)
        context.writer.write (", center = true" + tes + ");\n")
        return True
        

    def writePoints2D (self, points, context):
        """
        Write list of points.
        """
        for pointId in range (0, len (points) - 1):
            point = points[pointId]
            context.writer.write ("[")
            context.writer.writeNumber (point[0])
            context.writer.write (", ")
            context.writer.writeNumber (point[1])
            context.writer.write ("],\n")
        if len (points) > 0:
            point = points[-1]
            context.writer.write ("[")
            context.writer.writeNumber (point[0])
            context.writer.write (", ")
            context.writer.writeNumber (point[1])
            context.writer.write ("]\n")
        

    def writePoints3D (self, points, context):
        """
        Write list of points.
        """
        for pointId in range (0, len (points) - 1):
            point = points[pointId]
            context.writer.write ("[")
            context.writer.writeNumber (point[0])
            context.writer.write (", ")
            context.writer.writeNumber (point[1])
            context.writer.write (", ")
            context.writer.writeNumber (point[2])
            context.writer.write ("],\n")
        if len (points) > 0:
            point = points[-1]
            context.writer.write ("[")
            context.writer.writeNumber (point[0])
            context.writer.write (", ")
            context.writer.writeNumber (point[1])
            context.writer.write (", ")
            context.writer.writeNumber (point[2])
            context.writer.write ("]\n")
        

    def writeFaceIds (self, faces, context):
        """
        Write list of faces.
        """
        for faceId in range (0, len (faces) - 1):
            face = faces[faceId]
            context.writer.write ("[")
            context.writer.write (str (face[0]))
            context.writer.write (", ")
            context.writer.write (str (face[1]))
            context.writer.write (", ")
            context.writer.write (str (face[2]))
            context.writer.write ("],\n")
        if len (faces) > 0:
            face = faces[-1]
            context.writer.write ("[")
            context.writer.write (str (face[0]))
            context.writer.write (", ")
            context.writer.write (str (face[1]))
            context.writer.write (", ")
            context.writer.write (str (face[2]))
            context.writer.write ("]\n")


    def enterPolyhedron (self, item, context):
        """
        Write a polyhedron to OpenScad script.
        """
        self.writeComment (item, context)
        self.writeAttributes (item, context)
        context.writer.write ("polyhedron (points = [\n")
        context.writer.increaseIndent ()
        self.writePoints3D (item.points, context)
        context.writer.write ("],\n")
        context.writer.decreaseIndent ()
        context.writer.write ("faces = [\n")
        context.writer.increaseIndent ()
        self.writeFaceIds (item.faces, context)
        context.writer.write ("]);\n")
        context.writer.decreaseIndent ()
        return True
        

    def enterLinearExtrude (self, item, context):
        """
        Enter linear extrusion.
        """
        self.writeComment (item, context)
        self.writeAttributes (item, context)
        tes = self.formatTesselationParameters (item, context)
        context.writer.write ("linear_extrude (height = ")        
        context.writer.writeNumber (item.height)
        if item.twist != 0:
            context.writer.write (", twist = ")
            context.writer.writeNumber (item.twist)
        if item.scale != 1:
            context.writer.write (", scale = ")
            context.writer.writeNumber (item.scale)
        context.writer.write (", convexity = 10")
        minAngle, minSize, fixedCount, minSlices = context.resolvedAttributes[-1].rasterizingAttributes ()
        if minSlices != None:
            context.writer.write (", slices = ")
            context.writer.writeNumber (minSlices)            
        context.writer.write (", center = true" + tes + ")\n")
        context.writer.increaseIndent ()
        return True
        

    def enterRotateExtrude (self, item, context):
        """
        Enter linear extrusion.
        """
        self.writeComment (item, context)
        self.writeAttributes (item, context)
        tes = self.formatTesselationParameters (item, context)
        context.writer.write ("rotate_extrude (angle = ")        
        context.writer.writeNumber (item.angle)
        context.writer.write (", convexity = 10")
        context.writer.write (tes + ")\n")
        context.writer.increaseIndent ()
        return True


    def leaveExtrude (self, item, context):
        """
        Leave an extrusion.
        """
        self.endAttributes (item, context)
        context.writer.decreaseIndent ()
        return item


    def leaveGeometry (self, item, context):
        """
        Leave a geometry item.
        """
        self.endAttributes (item, context)
        return item


    def enterTranslate (self, item, context):
        """
        Enter translation.
        """
        self.writeComment (item, context)
        self.writeAttributes (item, context)
        context.writer.write ("translate ([")        
        context.writer.writeNumber (item.x)
        context.writer.write (", ")
        context.writer.writeNumber (item.y)
        context.writer.write (", ")
        context.writer.writeNumber (item.z)
        context.writer.write ("])\n")
        context.writer.increaseIndent ()
        return True
        

    def enterScale (self, item, context):
        """
        Enter scale.
        """
        self.writeComment (item, context)
        self.writeAttributes (item, context)
        context.writer.write ("scale ([")        
        context.writer.writeNumber (item.sx)
        context.writer.write (", ")
        context.writer.writeNumber (item.sy)
        context.writer.write (", ")
        context.writer.writeNumber (item.sz)
        context.writer.write ("])\n")
        context.writer.increaseIndent ()
        return True
        

    def enterRotate (self, item, context):
        """
        Enter rotate.
        """
        self.writeComment (item, context)
        self.writeAttributes (item, context)
        context.writer.write ("rotate ([")        
        context.writer.writeNumber (item.rx)
        context.writer.write (", ")
        context.writer.writeNumber (item.ry)
        context.writer.write (", ")
        context.writer.writeNumber (item.rz)
        context.writer.write ("])\n")
        context.writer.increaseIndent ()
        return True


    def leaveTransform (self, item, context):
        """
        Leave transform.
        """
        self.endAttributes (item, context)
        context.writer.decreaseIndent ()
        return item


    def enterUnion (self, item, context):
        """
        Write a boolean.Union instance.
        """
        if len (context.stack) > 1:
            self.writeComment (item, context)
            self.writeAttributes (item, context)
            context.writer.write ("union () {\n")        
            context.writer.increaseIndent ()
        return True
        

    def enterDifference (self, item, context):
        """
        Write a boolean.Difference instance.
        """
        self.writeComment (item, context)
        self.writeAttributes (item, context)
        context.writer.write ("difference () {\n")        
        context.writer.increaseIndent ()
        return True
        

    def enterIntersection (self, item, context):
        """
        Write a boolean.Intersection instance.
        """
        self.writeComment (item, context)
        self.writeAttributes (item, context)
        context.writer.write ("intersection () {\n")        
        context.writer.increaseIndent ()
        return True
        

    def leaveBoolean (self, item, context):
        """
        Leave boolean operation.
        """
        self.endAttributes (item, context)
        context.writer.decreaseIndent ()
        context.writer.write ("};\n")
        return item
        

    def leaveUnion (self, item, context):
        """
        Leave union operation.
        """
        if len (context.stack) > 1:
            self.endAttributes (item, context)
            context.writer.decreaseIndent ()
            context.writer.write ("};\n")
        return item
            
"""
Single instance of tree visitor.
"""
TreeVisitor = _TreeVisitor ()




# Open scad toolkit class
class _OpenScad:
    pass

_openScadInstance = None


def _writeScript (item: tree.Item, fileName: str, attributes: tree.Attributes = None):
    """
    Write a csg tree to a OpenScad script file. The file will be overwritten.
    """
    writer = textwriter.FileWriter (fileName)
    fmtWriter = textwriter.TextWriter (writer)
    if attributes == None:
        attributes = tree.Attributes.defaults ()
    TreeVisitor.execute (item, attributes, fmtWriter)
    fmtWriter.flush ()
    fmtWriter.close ()
    writer.flush ()
    writer.close ()


def getOpenScadRunnable ():
    """
    Get OpenScad runnable.
    """
    return "openscad"


def getScadScript (item: tree.Item, attributes: tree.Attributes = None):
    """
    Get the absolute path to an OpenScad script describing the geometry of *item* with *attributs*.
    """
    if attributes == None:
        attributes = tree.Attributes.defaults ()
    hc = hash ('openscad', item, attributes)
    persistent = cache.persistentPath (hc, 'scad', True)
    if pathlib.Path (persistent).exists ():
        return persistent
    tempFile = cache.temporary ('scad')
    _writeScript (item, tempFile, attributes)
    try:
        pathlib.os.rename (tempFile, persistent)
    except:
        pass
    return persistent


def getMaterialized (fmt: str, item: tree.Item, attributes: tree.Attributes = None):
    """
    Get materialized OpenScad file by format.
    """
    # try to get from cache
    assert fmt in ('off', 'stl'), "Unknown materializeing format for OpenScad"
    hc = hash ('materialized', item, attributes)
    persistent = cache.persistentPath (hc, fmt, True)
    if pathlib.Path (persistent).exists ():
        return persistent
    tempFile = cache.temporary (fmt)

    # TODO: silent flag
    silent = True

    # render to temporary file
    script = getScadScript (item, attributes)
    cmd = [getOpenScadRunnable (), script, '-o', str (tempFile)]
    result = subprocess.run (cmd, capture_output = silent)
    if result.returncode == 0:
        # move to cache
        try:
            pathlib.os.rename (tempFile, persistent)
        except:
            return None
        return persistent
    else:
        # handle error
        if silent:
            print (result.stderr)
            print (result.stdout)
        return None


def getRendering (fmt: str, item: tree.Item, attributes: tree.Attributes = None):
    """
    Get rendered OpenScad file by format.
    """
    assert fmt in ('png', 'svg'), "Unknown redering format for OpenScad"
    hc = hash ('rendered', item, attributes)
    persistent = cache.persistentPath (hc, fmt, True)
    if pathlib.Path (persistent).exists ():
        return persistent
    tempFile = cache.temporary (fmt)

    renderAttrs = attributes.renderAttributes ()
    if not fmt in ('png'):
        renderAttrs['antialias'] = 1

    # assert rendering options are valid
    assert isinstance (renderAttrs['width'], (int, float))
    assert renderAttrs['width'] > 0
    assert isinstance (renderAttrs['height'], (int, float))
    assert renderAttrs['height'] > 0
    assert isinstance (renderAttrs['antialias'], (int, float))
    assert renderAttrs['antialias'] > 0
    assert isinstance (renderAttrs['view.axis'], bool)
    assert isinstance (renderAttrs['view.scales'], bool)
    assert isinstance (renderAttrs['colorScheme'], str)

    antialias = renderAttrs['antialias']

    # compute rendering options
    width = renderAttrs['width'] * antialias
    height = renderAttrs['height'] * antialias
    renderOptions = ['--imgsize=' + str (width) + "," + str (height)]
    if renderAttrs['view.axis'] or renderAttrs['view.scales'] or renderAttrs['view.crosshairs']:
        vstr = ""
        if renderAttrs['view.axis']:
            vstr += 'axes'
        if renderAttrs['view.scales']:
            if vstr != "":
                vstr += ","
            vstr += 'scales'
        if renderAttrs['view.crosshairs']:
            if vstr != "":
                vstr += ","
            vstr += 'crosshairs'
        renderOptions += ['--view=' + vstr]
    if not renderAttrs['colorScheme'] in ('', None):
        renderOptions += ['--colorscheme=' + renderAttrs['colorScheme']]

    # process camera & perspective settings
    cameraAttribs = attributes.cameraAttributes ()
    renderOptions += ['--camera=' + ','.join (map (str, cameraAttribs['view']))]
    if cameraAttribs['projection'] == 'orthogonal':
        renderOptions += ['--projection=o']

    # TODO: silent flag
    silent = True

    # render to temporary file
    script = getScadScript (item, attributes)
    cmd = [getOpenScadRunnable (), script, '-o', str (tempFile)]
    cmd = cmd + renderOptions
    result = subprocess.run (cmd, capture_output = silent)
    
    # down sample anti aliased image
    if antialias > 1:
        downsample.downsampleImage (tempFile, tempFile, antialias)

    if result.returncode == 0:
        # move to cache
        try:
            pathlib.os.rename (tempFile, persistent)
        except:
            return None
        return persistent
    else:
        # handle error
        if silent:
            print (result.stderr)
            print (result.stdout)
        return None
