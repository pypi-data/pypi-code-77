import math
from . import tree
from . import boolean
from . import transform
from . import solid
from . import shape
from . import attributeTypes
from .util import cache
from .util import vmath
from .util import hash
from .util import differentialdrawing




def pushTransformsFurtherInside (item):
    """
    Push :ref:`Transforms<Transform>` into :ref:`Extrude<Extrude>` and :ref:`Boolean<Boolean>` tree nodes.
    """
    return _pushTransformsFurtherInside (item, [])




def pushExtrusionsFurtherInside (item):
    """
    Push :ref:`Extrudes<Extrude>` into and :ref:`Boolean<Boolean>` tree nodes.
    """
    return _pushExtrusionsFurtherInside (item, [])




def groupsToUnions (item):
    """
    Transform groups into unions.
    """
    return GroupsToUnions.execute (item, tree.Attributes ())




def removeEmpty (item):
    """
    Remove empty items from tree.
    """
    return RemoveEmptyNodes.execute (item, tree.Attributes ())




def defaultColorGenerator (count):
    """
    Generate color for item.
    """
    rsx = 1.0 / 3.0
    if count < 2:
        # TODO: return default color
        return ((1, 0, 0),)
    colors = []
    for index in range (0, count):
        rsp = index / count
        if rsp <= rsx:
            # in red to green range
            ix = (rsp) * 3
            c1 = vmath.vsMulScalar ((1, 0, 0), 1 - ix)
            c2 = vmath.vsMulScalar ((0, 1, 0), ix)
            c = vmath.vsAdd (c1, c2)
        elif rsp <= (2 * rsx):
            # in green to blue range
            ix = (rsp - rsx) * 3
            c1 = vmath.vsMulScalar ((0, 1, 0), 1 - ix)
            c2 = vmath.vsMulScalar ((0, 0, 1), ix)
            c = vmath.vsAdd (c1, c2)
        else:
            # in blue to red range
            ix = (rsp - (2 * rsx)) * 3
            c1 = vmath.vsMulScalar ((0, 0, 1), 1 - ix)
            c2 = vmath.vsMulScalar ((1, 0, 0), ix)
            c = vmath.vsAdd (c1, c2)
        colors.append (c)
    return colors




def distributeColors (item, override: bool = False, colorGenerator = defaultColorGenerator):
    """
    Distribute colors of renderable items.
    """
    colorCount = _DistributeColorsSingleton.countColors (item, override)
    colorMap = colorGenerator (colorCount)
    return _DistributeColorsSingleton.execute (item, override, colorMap)


# === implementation ===


class _DistributeColors (tree.Visitor):
    """
    Distribute colors to renderable items
    """
    def __init__ (self):
        super ().__init__ ()
        self.rule (shape.Shape, leave = self.leaveRenderable)
        self.rule (solid.Solid, leave = self.leaveRenderable)


    class Context (tree.Visitor.Context):
        """
        Visitor for assigning rendering colors.
        """
        def __init__ (self, attributes):
            super ().__init__ (attributes)
            self.contextCollectStage = True
            self.colorMap = None
            self.contextColorId = 0


    def countColors (self, item, override):
        """
        Count colores required for painting items.
        """
        context = _DistributeColors.Context (None)
        self.visit (item, context)
        return context.contextColorId


    def execute (self, item, override, colorMap):
        """
        Run replace node on a tree.
        """
        context = _DistributeColors.Context (None)
        context.colorMap = colorMap
        context.contextCollectStage = False
        return self.visit (item, context)


    def leaveRenderable (self, item, context):
        if context.contextCollectStage:
            if item.attributes.get ('material') == None:
                context.contextColorId += 1
        else:
            if item.attributes.get ('material') == None:
                cid = context.contextColorId
                cid = cid % len (context.colorMap)
                newColor = context.colorMap[cid]
                context.contextColorId += 1
                newMaterialColor = attributeTypes.Material (newColor)
                nAttributes = item.attributes.override ({'material': newMaterialColor})
                return item.copy (attributes = nAttributes)
            return item
        return item

"""
Single instance of distribute colors arlgorithm.
"""
_DistributeColorsSingleton = _DistributeColors ()




def _pushTransformsFurtherInside (item, transformStack):
    """
    Move transforms further inside the tree.
    """
    if item == None:
        return None
    if isinstance (item, tree.Empty):
        return item
    if isinstance (item, transform.Transform):
        transformStack.append (item)
        assert len (item.children) == 1
        result = _pushTransformsFurtherInside (item.children[0], transformStack)
        transformStack.pop ()
        return result
    elif isinstance (item, (boolean.Boolean, solid.LinearExtrude)):
        if len (transformStack) == 0:
            return item
        newChildren = []
        for childId in range (0, len (item.children)):
            newChildren.append (_pushTransformsFurtherInside (item.children[childId], transformStack))
        return item.copy (children = newChildren)
    else:
        if len (transformStack) == 0:
            return item
        else:
            transformed = pushTransformsFurtherInside (item)
            for transformId in range (len (transformStack) - 1, -1, -1):
                transformed = transformStack[transformId].copy (children = (transformed,))
            return transformed




def _pushExtrusionsFurtherInside (item, extrudeStack):
    """
    Move extrusions further inside the tree.
    """
    if item == None:
        return None
    if isinstance (item, tree.Empty):
        return item
    if isinstance (item, (solid.LinearExtrude, solid.RotateExtrude)):
        extrudeStack.append (item)
        assert len (item.children) == 1
        result = _pushExtrusionsFurtherInside (item.children[0], extrudeStack)
        extrudeStack.pop ()
        return result
    elif isinstance (item, boolean.Boolean):
        if len (extrudeStack) == 0:
            return item
        newChildren = []
        for childId in range (0, len (item.children)):
            newChildren.append (_pushExtrusionsFurtherInside (item.children[childId], extrudeStack))
        return item.copy (children = newChildren)
    else:
        if len (extrudeStack) == 0:
            return item
        else:
            extruded = pushExtrusionsFurtherInside (item)
            for extrudedId in range (len (extrudeStack) - 1, -1, -1):
                extruded = extrudeStack[extrudedId].copy (children = (extruded,))
            return extruded




class RemoveNodes (tree.Visitor):
    """
    Remove nodes from csg tree by custom rule.
    """
    def __init__ (self):
        super ().__init__ ()


    def execute (self, item, attributes):
        """
        Run replace node on a tree.
        """
        context = tree.Visitor.Context (attributes)
        result = self.visit (item, context)
        if isinstance (result, tree.Empty):
            return None
        return result


    def enterFilter (self, item, context):
        """
        Enter node filtered out.
        """
        return False


    def leaveFilter (self, item, context):
        """
        Enter node filtered out.
        """
        return tree.Empty ()




class _GroupsToUnions (tree.Visitor):
    """
    Replace group by union nodes.
    """
    def __init__ (self):
        super ().__init__ ()
        self.rule (tree.Group, leave = self.leaveGroup)


    def execute (self, item, attributes):
        """
        Return tree with unions instead of groups.
        """
        context = tree.Visitor.Context (attributes)
        result = self.visit (item, context)
        return result


    def leaveGroup (self, item, context):
        """
        Process group.
        """
        return boolean.Union (children = item.children, name = item.name, attributes = item.attributes)

"""
Single instance of group to union filter.
"""
GroupsToUnions = _GroupsToUnions ()




class _CollectParts (tree.Visitor):
    """
    Collect all parts of a scene.
    """
    def __init__ (self):
        super ().__init__ ()
        self.rule (tree.Part, enter = self.enterPart)


    def execute (self, item, attributes):
        """
        Collect parts from a csg tree. Returns a list of all parts found inside a design.
        """
        context = tree.Visitor.Context (attributes)
        context.__setattr__ ('parts', [])
        self.visit (item, context)
        return context.__getattribute__ ('parts')


    def enterPart (self, item, context):
        """
        Enter part node.
        """
        context.parts.append (item)

        # Do not recurse on part.
        return False

"""
Single instance of part collector.
"""
CollectParts = _CollectParts ()




class _RemoveEmptyNodes (tree.Visitor):
    """
    Remove emtpy nodes from csg tree.
    """
    def __init__ (self):
        super ().__init__ ()

        # deep inspection rules
        self.rule (solid.LinearExtrude, leave = self._leaveSingleChild)
        self.rule (solid.RotateExtrude, leave = self._leaveSingleChild)
        self.rule (shape.Projection, leave = self._leaveSingleChild)
        self.rule (transform.Translate, leave = self._leaveSingleChild)
        self.rule (transform.Scale, leave = self._leaveSingleChild)
        self.rule (transform.Rotate, leave = self._leaveSingleChild)
        self.rule (boolean.Union, leave = self._leaveUnion)
        self.rule (boolean.Difference, leave = self._leaveDifference)
        self.rule (boolean.Intersection, leave = self._leaveIntersection)
        self.rule (tree.Group, leave = self._leaveGroup)


    def execute (self, item, attributes):
        """
        Run replace node on a tree.
        """
        context = tree.Visitor.Context (attributes)
        return self.visit (item, context)


    def _leaveSingleChild (self, item, context):
        """
        Process a tree item with a single child.
        """
        if (item.children[0] == None) or (isinstance (item.children[0], tree.Empty)):
            return item.Empty
        return item


    def _leaveUnion (self, item, context):
        """
        Remove empty items from a union.
        """
        childCount = 0
        children = []
        for child in item.children:
            if child != None:
                if not isinstance (child, tree.Empty):
                    childCount += 1
                    children.append (child)
        if childCount == 0:
            return tree.Empty (name = item.name, attributes = item.attributes)
        if childCount != len (item.children):
            if childCount == 1:
                return children[0]
            return boolean.Union (children = children, name = item.name, attributes = item.attributes)
        else:
            return item


    def _leaveDifference (self, item, context):
        """
        Remove empty items from a difference.
        """
        c1 = item.children[0] if len (item.children) > 0 else None
        c2 = item.children[1] if len (item.children) > 1 else None
        if isinstance (c1, tree.Empty):
            c1 = None
        if isinstance (c2, tree.Empty):
            c2 = None
        if c1 != None:
            if c2 == None:
                return c1
            else:
                return item
        else:
            return tree.Empty (name = item.name, attributes = item.attributes)
        

    def _leaveIntersection (self, item, context):
        """
        Remove empty items from an intersection.
        """
        c1 = item.children[0] if len (item.children) > 0 else None
        c2 = item.children[1] if len (item.children) > 1 else None
        if isinstance (c1, tree.Empty):
            c1 = None
        if isinstance (c2, tree.Empty):
            c2 = None
        if c1 != None:
            if c2 == None:
                return c1
            else:
                return item
        else:
            if c2 == None:
                return tree.Empty (name = item.name, attributes = item.attributes)
            else:
                return c2
        

    def _leaveGroup (self, item, context):
        """
        Remove empty items from a group.
        """
        childCount = 0
        children = []
        for child in item.children:
            if child != None:
                if not isinstance (child, tree.Empty):
                    childCount += 1
                    children.append (child)
        if childCount == 0:
            return tree.Empty (name = item.name, attributes = item.attributes)
        if childCount != len (item.children):
            if childCount == 1:
                return children[0]
            return tree.Group (children = children, name = item.name, attributes = item.attributes)
        else:
            return item
        
"""
Single instance of empty nodes removal filter.
"""
RemoveEmptyNodes = _RemoveEmptyNodes ()




# import open scad tools
from .util.external import openscad




class BezierDDAElement (differentialdrawing.Element):
    """
    Differential drawing element for bezier curve path.
    """
    def __init__ (self, pathPoints):
        super ().__init__ ()
        self.pathPoints = pathPoints

    def pointAt (self, t):
        """
        Calculate a point on the bezier curve.
        """
        return vmath.bezier (self.pathPoints, t)




def _bezierShapeToPolygon (item, rasterizingAttributes):
    """
    Convert a bezier shape to a Polygon.
    """

    # get rasterizing settings
    minAngle, minSize, fixedCount, minSlices = rasterizingAttributes.rasterizingAttributes ()

    # rasterize bezier shape to polygon
    pathes = []
    for curve in item.curves:
        pathes.append (BezierDDAElement (curve))
    dda = differentialdrawing.Path (pathes)
    return dda.toPolygon (initialSegmentCount = 2, maxStepSize = minSize, name = item.name, attributes = item.attributes)




def __reassemblePath (edgesLeft, normalizedEdges, currentPath):
    """
    Reassembles a path from elements.
    """
    # start on an arbitrary path
    pivot = edgesLeft.pop ()
    alreadyProcessed = set ()
    alreadyProcessed.add (pivot)
    currentPath.append (pivot[0])
    currentPath.append (pivot[1])

    # link paths until no path is left.
    elementFound = True
    while elementFound:
        # find next candidate
        lastPoint = currentPath[-1]
        if lastPoint in normalizedEdges:
            nextPoints = normalizedEdges[lastPoint]
            if len (nextPoints) == 1:
                # simple case, got only one candidate
                nextCandidate = (lastPoint, nextPoints[0])
                if lastPoint < nextPoints[0]:
                    nextCandidateKey = (lastPoint, nextPoints[0])
                else:
                    nextCandidateKey = (nextPoints[0], lastPoint)
                if nextCandidateKey in alreadyProcessed:
                    nextCandidate = None
            else:
                nextCandidate = None
                nextCandidateKey = None
                for nextPoint in nextPoints:
                    nextCandidateProto = (lastPoint, nextPoint)
                    if lastPoint < nextPoint:
                        nextCandidateProtoKey = (lastPoint, nextPoint)
                    else:
                        nextCandidateProtoKey = (nextPoint, lastPoint)
                    if not nextCandidateProtoKey in alreadyProcessed:
                        nextCandidate = nextCandidateProto
                        nextCandidateKey = nextCandidateProtoKey
                        break
        else:
            assert False, "invalid point index found"
            nextCandidate = None
            nextCandidateKey = None

        elementFound = nextCandidate != None

        # process candidate
        if nextCandidate != None:
            # TODO: remove from edges left
            if nextCandidateKey in edgesLeft:
                edgesLeft.remove (nextCandidateKey)
            alreadyProcessed.add (nextCandidateKey)
            currentPath.append (nextCandidate[1])

    # Assert path is closed, remove closing point
    assert len (currentPath) > 0, "expected path to be not empty."
    assert currentPath[0] == currentPath[-1]
    currentPath.pop ()
    return




def _projectedMeshToPolygon (mesh):
    """
    Transform a projected mesh into a Polygon.
    """
    # foreach face in "bottom layer" (i.e. all z-coordinates < 0):
    # build a map [points of edge -> (faceIndex, pointIndex1, pointIndex2)]
    edgeMap = {}
    for faceId in range (0, len (mesh.faces)):
        face = mesh.faces[faceId]
        faceAccepted = True
        for edgeId in range (0, 3):
            if mesh.points[face[edgeId]][2] >= 0:
                faceAccepted = False
        if faceAccepted:
            for edgeId in range (0, 3):
                pid1 = face[edgeId % 3]
                pid2 = face[(edgeId + 1) % 3]
                pid = str (pid1) + "," + str (pid2) if pid1 < pid2 else str (pid2) + "," + str (pid1)
                if pid in edgeMap:
                    edgeMap[pid].append ((pid1, pid2))
                else:
                    edgeMap[pid] = [(pid1, pid2)]

    # build edge links
    normalizedEdges = {}
    edgesLeft = set ()
    for edge in edgeMap:
        value = edgeMap[edge]
        if len (value) == 1:
            p0 = value[0][0]
            p1 = value[0][1]
            if p1 < p0:
                t = p0
                p0 = p1
                p1 = t
            edgesLeft.add ((p0, p1))
            if p0 in normalizedEdges:
                normalizedEdges[p0].append (p1)
            else:
                normalizedEdges[p0] = [p1]
            if p1 in normalizedEdges:
                normalizedEdges[p1].append (p0)
            else:
                normalizedEdges[p1] = [p0]

    # rebuild pathes from edge links
    pathes = []
    while len (edgesLeft) > 0:
        currentPath = []
        __reassemblePath (edgesLeft, normalizedEdges, currentPath)
        pathes.append (currentPath)

    # separated pathes, recreate points and indices.
    remappedPointIndices = {}
    newPoints = []
    newPathes = []
    for path in pathes:
        newPath = []
        for point in path:
            if point in remappedPointIndices:
                rpid =  remappedPointIndices[point]
            else:
                rpid = len (newPoints)
                newPoints.append ((mesh.points[point][0], mesh.points[point][1]))
                remappedPointIndices[point] = rpid
            newPath.append (rpid)
        newPathes.append (newPath)

    # select outer path
    outerPathIndex = None
    testEdgeIndex = 0
    testsDone = True
    while testsDone:
        testsDone = False
        for outerFaceTestIndex in range (0, len (newPathes)):
            for innerFaceTestIndex in range (0, len (newPathes)):
                if innerFaceTestIndex != outerFaceTestIndex:
                    if testEdgeIndex < len (newPathes[innerFaceTestIndex]):
                        innerPoint = newPoints[newPathes[innerFaceTestIndex][testEdgeIndex]]
                        if _checkIfPointIsInsidePath (newPoints, newPathes[outerFaceTestIndex], innerPoint):
                            outerPathIndex = outerFaceTestIndex
                            break
                        testsDone = True
            if outerPathIndex != None:
                break
        if testsDone == False:
            break
        testEdgeIndex += 1
    if outerPathIndex == None:
        outerPathIndex = 0

    # build cutouts
    cutouts = []
    for pathIndex in range (0, len (newPathes)):
        if pathIndex != outerPathIndex:
            cutouts.append (newPathes [pathIndex])

    # build polygon from pathes
    return shape.Polygon (newPoints, newPathes[outerPathIndex], cutouts, name = mesh.name, attributes = mesh.attributes)




def _checkIfTestpointIntersectsPath (line1, line2, testPoint):
    # sort that l2rel has maximum x
    l1rel = vmath.vsSub (line1, testPoint)
    l2rel = vmath.vsSub (line2, testPoint)
    if l2rel[0] < l1rel[0]:
        t = l1rel
        l1rel = l2rel
        l2rel = t

    # elements wont match?
    if l2rel[0] < 0:
        return False
    if l1rel[0] > 0:
        return False

    # check if is intersecting
    xDist = l2rel[0] - l1rel[0]
    xRelOff = -l1rel[0] / xDist
    yDist = l2rel[1] - l1rel[1]
    yAtX0 = yDist * xRelOff + l1rel[1]
    return yAtX0 > 0




def _checkIfPointIsInsidePath (points, edges, testPoint):
    """
    Check if a point is inside a path
    """
    intersectionCount = 0
    for edgeId1 in range (0, len (edges)):
        edgeId2 = (edgeId1 + 1) % len (edges)
        if _checkIfTestpointIntersectsPath (points[edgeId1], points[edgeId2], testPoint):
            intersectionCount += 1
    return (intersectionCount % 2) == 1




def toPolygons (item: tree.Item, rasterizingAttributes: tree.Attributes):
    """
    Converts a Shape into a set of polygons.
    """
    # complex shape?
    if isinstance (item, shape.Complex):
        return item.rasterize (rasterizingAttributes)

    # convert bezier shape?
    if isinstance (item, shape.Bezier):
        return _bezierShapeToPolygon (item, rasterizingAttributes)

    # convert bezier shape?
    if isinstance (item, shape.Polar):
        return _polarShapeToPolygon (item, rasterizingAttributes)

    # create shapes from projected solid
    itmesh = solid.Polyhedron.fromSolid (solid.LinearExtrude (children = (item,)), rasterizingAttributes)
    polygons = []
    if isinstance (itmesh, tree.Group):
        for child in itmesh.children:
            if not isinstance (child, tree.Empty):
                polygons.append (_projectedMeshToPolygon (child))
    else:
        if not isinstance (itmesh, tree.Empty):
            polygons.append (_projectedMeshToPolygon (itmesh))

    # create return value
    if len (polygons) == 0:
        return tree.Empty (item.name, item.attributes)
    elif len (polygons) == 1:
        return polygons[0]
    else:
        return tree.Group (children = polygons, name = item.name, attributes = item.attributes)




def toPolyhedrons (item: tree.Item, rasterizingAttributes: tree.Attributes):
    """
    Converts a solid into a set of polyhedrons.
    """
    renderedFile = openscad.getMaterialized ('off', item, rasterizingAttributes)
    return solid.Polyhedron.fromFileOFF (renderedFile)
