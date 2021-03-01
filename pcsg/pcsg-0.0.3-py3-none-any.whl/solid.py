import os
import math
import pathlib
from . import tree
from .attributes import Attributes
from .util import polytool
from .util import cache
from .util import hash
from .util import vmath




class Solid:
    """
    Informational base class of :ref:`Solid<Solid>` objects. This empty class is implemented for type matching purposes.
    """
    def __init__ (self):
        #: Number of dimensions is always 3 for :ref:`Solids<Solid>`.
        self.dimensions = 3




class Sphere(tree.Item, Solid):
    """
    A Sphere is a basic :ref:`Solid<Solid>` class.
    
    The Sphere can be definied with the parameter *radius* or *diameter*. Only the radius will be stored.
    The Spheres center is at coordinate (0, 0, 0).
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

        # Number of dimensions is always 3 for :ref:`Solids<Solid>`.
        self.dimensions = 3

        #: Radius of the sphere.
        self.radius = radius

    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            tree.Item,
            'radius'
        )




class Cube(tree.Item, Solid):
    """
    A Cube is a basic :ref:`Solid<Solid>` class.
    
    The Cube is defined by a three dimensional size tuple.
    The Cubes center is at coordinate (0, 0, 0).
    """
    def __init__ (self,
                    size: tuple = (1, 1, 1),
                    name: str = None,
                    attributes: Attributes = None    
        ):
        super ().__init__ (name = name, attributes = attributes)

        # check for valid size parameter
        assert size != None, "Expected parameter size to be defined"
        if isinstance (size, (int, float)):
            size = (size, size, size)
        elif isinstance (size, list):
            size = tuple (size)
        elif not isinstance (size, tuple):
            assert False, "Expected size to be a number or a 3 dimensional vector"
        assert len (size) == 3, "Expected size to be a number or a 3 dimensional vector"
        assert isinstance (size[0], (int, float)), "Expected size to be a tuple containing 3 numbers"
        assert isinstance (size[1], (int, float)), "Expected size to be a tuple containing 3 numbers"
        assert isinstance (size[2], (int, float)), "Expected size to be a tuple containing 3 numbers"

        # Number of dimensions is always 3 for :ref:`Solids<Solid>`.
        self.dimensions = 3

        #: Size of Cube as tuple containing (width: float, height: float, depth: float).
        self.size = size

    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            tree.Item,
            'size'
        )    




class Cylinder(tree.Item, Solid):
    """
    A Cylinder is a basic :ref:`Solid<Solid>` class.
    
    The Cylinder is defined by a height and two diameters or radius values.
    The Cylinders center is at coordinate (0, 0, 0).
    """
    def __init__ (self,
                    height: float = 1,
                    radius1: float = None,
                    radius2: float = None,
                    diameter1: float = None,
                    diameter2: float = None,
                    name: str = None,
                    attributes: Attributes = None    
        ):
        super ().__init__ (name = name, attributes = attributes)

        # check parameters for height
        assert isinstance (height, (int, float)), "Expected a number as parameter height"

        # check parameters for radius1
        if radius1 != None:
            assert isinstance (radius1, (int, float)), "Expected a number as parameter radius1"
            assert diameter1 == None, "Parameter radius1 can not be used together with diameter1"
        elif diameter1 != None:
            assert isinstance (diameter1, (int, float)), "Expected a number as parameter diameter1"
            radius1 = diameter1 / 2
        else:
            radius1 = 1

        # check parameters for radius2
        if radius2 != None:
            assert isinstance (radius2, (int, float)), "Expected a number as parameter radius2"
            assert diameter2 == None, "Parameter radius2 can not be used together with diameter2"
        elif diameter2 != None:
            assert isinstance (diameter2, (int, float)), "Expected a number as parameter diameter2"
            radius2 = diameter2 / 2
        else:
            radius2 = radius1

        # Number of dimensions is always 3 for :ref:`Solids<Solid>`.
        self.dimensions = 3

        #: Height of the Cylinder.
        self.height = height

        #: Radius of Cylinder at z = **-height** / 2.
        self.radius1 = radius1

        #: Radius of Cylinder at z = **height** / 2.
        self.radius2 = radius2

    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            tree.Item,
            'height',
            'radius1',
            'radius2'
        )    




class Polyhedron(tree.Item, Solid):
    """
    A Polyhedron is a :ref:`Solid<Solid>` formed by a closed surface of triangles.
    """
    def __init__ (self,
                    points: tuple = None,
                    faces: tuple = None,
                    normals: tuple = None,
                    uvvectors: tuple = None,
                    name: str = None,
                    attributes: Attributes = None    
        ):

        super ().__init__ (name = name, attributes = attributes)

        # Number of dimensions is always 3 for :ref:`Solids<Solid>`.
        self.dimensions = 3

        #: Tuple containing the three dimensional position vectors used for declaraing the corners of a face.
        self.points = points

        #: Tuple containing the three dimensional normal vectors used for defining the normals of a face.
        #: Normals are optional.
        self.normals = normals

        #: Tuple containing the two dimensional uv vectors used for defining the texture mapping of a face.
        #: Uv vectors are optional.
        self.uvvectors = uvvectors

        #: A Polyhedron is definied by a closed set of faces. Each face describes a triangle with optional
        #: normals and texture mappings for each point. Faces are references to points, normals and uv vectors
        #: in the format (p1, p2, p3[, n1, n2, n3 [, vu1, vu2, vu3]]). A face must have 3, 6 or 9 elements.
        #: Normal and vu vector indices are optional and can be set to None if a point doesn't have a normal
        #: or uv mapping.
        self.faces = faces


    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            tree.Item,
            'points',
            'faces',
            'normals',
            'uvvectors'
        )


    @staticmethod
    def _removeDuplicatesWithIndices (points, faces, normals, uvs):
        """
        Optimize polyhedron: remove duplicated points, normals and uv vectors, adjusts face indices accodingly.
        """
        # make point, normals, uvs unique
        newPoints, pointMap = polytool._removeDuplicatesVector3 (points)
        newNormals, normalMap = polytool._removeDuplicatesVector3 (normals)
        newUvs, uvsMap = polytool._removeDuplicatesVector2 (uvs)

        # replace indices in faces
        newFaces = []
        for face in faces:
            newFace = []
            if len (face) >= 3:
                # process points
                newFace.append (pointMap [face[0]])
                newFace.append (pointMap [face[1]])
                newFace.append (pointMap [face[2]])
            if len (face) >= 6:
                # process normals
                newFace.append (normalMap [face[3]] if face[3] != None else None)
                newFace.append (normalMap [face[4]] if face[4] != None else None)
                newFace.append (normalMap [face[5]] if face[5] != None else None)
            if len (face) >= 9:
                # process uvs
                newFace.append (uvsMap [face[6]] if face[6] != None else None)
                newFace.append (uvsMap [face[7]] if face[7] != None else None)
                newFace.append (uvsMap [face[8]] if face[8] != None else None)
            elif len (face) > 9:
                assert False, "unsupported face format"
            newFaces.append (newFace)

        # return result
        return (newPoints, newFaces, newNormals, newUvs)


    @staticmethod
    def fromSolid (solid: tree.Item, rasterizingAttributes: Attributes = None, name: str = None, attributes: Attributes = None):
        """
        Create a Polyhedron by rasterizing a three dimensional csg tree :ref:`Item<Item>`.
        The accuracy for rasterizing is calculated from *rasterizingAttributes*.
        When the solid has disjunct volumes, a :ref:`Group<Group>` of Polyhedrons will be returned.
        When the solid has no renderable items, :ref:`Empty<Empty>` will be returned.
        """
        rasterized = _toPolyhedronsWrapper (solid, rasterizingAttributes)
        return rasterized.copy (name = name, attributes = attributes)


    @staticmethod
    def _parseFloatArgs (line, count = None):
        """
        Parse array of numbers.
        """
        l = line.split (" ")
        r = []
        for e in l:
            if e != "":
                r.append (float (e))
        return r


    @staticmethod
    def _parseIntegerArgs (line, count = None):
        """
        Parse array of integers.
        """
        l = line.split (" ")
        r = []
        for e in l:
            if e != "":
                r.append (int (e))
        return r


    @staticmethod
    def _checkIsCCW (normalVector, facetPoints, default):
        center = vmath.vsDivScalar (vmath.vsAdd (vmath.vsAdd (facetPoints[0], facetPoints[1]), facetPoints[2]), 3)
        s = vmath.vsAdd (center, normalVector)
        va = vmath.vsSub (facetPoints[1], facetPoints[0])
        vb = vmath.vsSub (facetPoints[2], facetPoints[0])
        vc = vmath.vsSub (s, facetPoints[0])
        axb = (
            va[1] * vb[2] - va[2] * vb[1],
            va[2] * vb[0] - va[0] * vb[2],
            va[0] * vb[1] - va[1] * vb[0]
        )
        vd = axb[0] * vc[0] + axb[1] * vc[1] + axb[2] * vc[2]
        if vd > 0:
            return True
        elif vd < 0:
            return False
        else:
            return default


    def _fromSubsetOfFaces (self, facesIncluded, name, attributes):
        """
        Returns a new Polyhedron consisting of a subset of the current faces
        """
        newPoints = []
        pointRemap = {}
        newNormals = []
        normalRemap = {}
        newVus = []
        vuRemap = {}
        newFaces = []

        # process each face
        for faceId in facesIncluded:
            face = self.faces[faceId]
            newFace = []
            # process points...
            for index in range (0, 3):
                pid = face[index]
                if pid in pointRemap:
                    npid = pointRemap[pid]
                else:
                    npid = len (newPoints)
                    newPoints.append (self.points[pid])
                    pointRemap[pid] = npid
                newFace.append (npid)
            if len (face) > 3:
                # process normal vectors
                for index in range (3, 6):
                    pid = face[index] if index < len (face) else None
                    if pid in normalRemap:
                        npid = normalRemap[pid]
                    else:
                        npid = len (newNormals)
                        newNormals.append (self.normals[pid])
                        normalRemap[pid] = npid
                    newFace.append (npid)
            if len (face) > 6:
                # process vu vectors
                for index in range (6, 9):
                    pid = face[index] if index < len (face) else None
                    if pid in vuRemap:
                        npid = vuRemap[pid]
                    else:
                        npid = len (newVus)
                        newVus.append (self.uvvectors[pid])
                        vuRemap[pid] = npid
                    newFace.append (npid)
            # append new face
            newFaces.append (newFace)

        # return subset
        return Polyhedron (newPoints, newFaces, newNormals, newVus, name, attributes)


    @staticmethod
    def _splitCollectFaces (pointsToFaces, facesToMashMap, faceIndex, currentSolidIdentifier, volumeFaces, faceList):
        # start on face index
        delayedProcess = [faceIndex]
        alreadyProcessed = set ()
        alreadyProcessed.add (faceIndex)
        
        # delay processed nodes
        while len (delayedProcess) > 0:
            # pop from delayed process stack
            popDelay = delayedProcess.pop ()

            # add node to face list and flag as used
            faceList.append (popDelay)
            facesToMashMap[popDelay] = currentSolidIdentifier

            # process neighbours
            face = volumeFaces[popDelay]
            for edge in range (0, 3):
                pid1 = face[edge % 3]
                pid2 = face[(edge + 1) % 3]
                pid = str (pid1) + "," + str (pid2) if pid1 < pid2 else str (pid2) + "," + str (pid1)
                for anchestor in pointsToFaces[pid]:
                    if not anchestor in alreadyProcessed:
                        alreadyProcessed.add (anchestor)
                        delayedProcess.append (anchestor)


    @staticmethod
    def _splitVolume (volume):
        # create point to face map and solid mapping dictionary
        pointsToFaces = {}
        facesToMashMap = []
        for faceId in range (0, len (volume.faces)):
            face = volume.faces[faceId]
            for edge in range (0, 3):
                pid1 = face[edge % 3]
                pid2 = face[(edge + 1) % 3]
                pid = str (pid1) + "," + str (pid2) if pid1 < pid2 else str (pid2) + "," + str (pid1)
                if pid in pointsToFaces:
                    pointsToFaces[pid].append (faceId)
                else:
                    pointsToFaces[pid] = [faceId]
            facesToMashMap.append (None)

        # split algorithm
        splitVolumes = []
        currentSolidIdentifier = -1
        nextFaceToCheck = 0
        while nextFaceToCheck < len (facesToMashMap):
            # when already marked, skip node
            if facesToMashMap[nextFaceToCheck] != None:
                nextFaceToCheck += 1

            # face is not marked yet, pick a new solid identifier and mark it.
            else:
                currentSolidIdentifier += 1
                faceList = []
                Polyhedron._splitCollectFaces (pointsToFaces, facesToMashMap, nextFaceToCheck, currentSolidIdentifier, volume.faces, faceList)
                splitVolumes.append (faceList)
                facesToMashMap[nextFaceToCheck] = currentSolidIdentifier
                nextFaceToCheck += 1

        # generate result by splitting volumes
        if len (splitVolumes) > 1:
            items = []
            solidId = 0
            for faces in splitVolumes:
                newName = volume.name
                if newName in (None, ""):
                    newName = str (solidId)
                else:
                    newName = newName + "-" + str (solidId)
                solidId += 1
                items.append (volume._fromSubsetOfFaces (faces, volume.name, volume.attributes))
            return items

        # return solid as it is
        return [volume]


    @staticmethod
    def _splitVolumes (inputs, name: str, attributes: Attributes):
        """
        Split parsed volumes.
        """
        # collect and split volumes
        volumes = []
        if inputs == None:
            return None
        if isinstance (inputs, tree.Group):
            for child in inputs.children:
                volumes = volumes + Polyhedron._splitVolume (child)
        else:
            volumes = volumes + Polyhedron._splitVolume (inputs)

        # write back result
        if len (volumes) == 0:
            return None
        if len (volumes) == 1:
            return volumes[0]
        return tree.Group (children = volumes, name = name, attributes = attributes)


    @staticmethod
    def _loadStlFile (fileName, name: str = None, attributes: Attributes = None):
        """
        Load stl file.
        """
        correctOrientation = True

        # storage for parsed points and faces
        parsedPoints = []
        faces = []
        parsedSolids = []

        # read file
        with open (fileName) as f:
            state = 0
            normalVector = None
            facetPoints = []
            for line in f:
                # remove comments and strip line
                line = line.split (';', 1)[0].strip ().lower ()
                if line != "":
                    if state == 3:
                        # parse vertex coordinates
                        if line == "endloop":
                            assert len (facetPoints) == 3, "Expected 3 points per facet"
                            if correctOrientation:
                                isCCW = Polyhedron._checkIsCCW (normalVector, facetPoints, True)
                            else:
                                isCCW = True
                            firstPointIndex = len (parsedPoints)
                            if isCCW:
                                parsedPoints.append ((facetPoints[0], firstPointIndex))
                                parsedPoints.append ((facetPoints[1], firstPointIndex + 1))
                                parsedPoints.append ((facetPoints[2], firstPointIndex + 2))
                            else:
                                parsedPoints.append ((facetPoints[1], firstPointIndex))
                                parsedPoints.append ((facetPoints[0], firstPointIndex + 1))
                                parsedPoints.append ((facetPoints[2], firstPointIndex + 2))
                            faces.append ((firstPointIndex, firstPointIndex + 1, firstPointIndex + 2))
                            state = 4
                        elif line.startswith ("vertex "):
                            rest = line[7:].strip ()
                            coordinates = Polyhedron._parseFloatArgs (rest)
                            assert len (coordinates) == 3, "Expected 3 coodinates per normal"
                            facetPoints.append (coordinates)
                        else:
                            assert False, "expected endloop or vertex keyword"
    
                    elif state == 4:
                        # expect endfacet statement
                        if line == "endfacet":
                            state = 1
                        else:
                            assert False, "expected endfacet keyword"

                    elif state == 2:
                        # expect outer loop statement
                        if line.startswith ("outer "):
                            rest = line[6:].strip ()
                            if rest == "loop":
                                state = 3
                            else:
                                assert False, "expected loop keyword"
                        else:
                            assert False, "expected outer keyword"

                    elif state == 1:
                        # expect a facet or end of solid
                        normalVector = None
                        facetPoints = []
                        if line.startswith ("endsolid ") or line == "endsolid":
                            # finish currently parsed solid
                            optPoints, optFaces, optNormals, optVUs = Polyhedron._removeDuplicatesWithIndices (parsedPoints, faces, None, None)
                            poly = Polyhedron (optPoints, optFaces, optNormals, optVUs, name, attributes)
                            parsedSolids.append (poly)
                            parsedPoints = []
                            faces = []
                            state = 5
                        elif line == "facet":
                            state = 2
                        elif line.startswith ("facet "):
                            rest = line[6:].strip ()
                            if rest != "":
                                if rest.startswith ("normal "):
                                    rest = rest[7:].strip ()
                                    normalVector = Polyhedron._parseFloatArgs (rest)
                                    assert len (normalVector) == 3, "Expected 3 coodinates per normal"
                                else:
                                    assert False, "expected normal keyword"
                            state = 2
                        else:
                            assert False, "expected facet declaration or endsolid keyword"

                    elif state == 0:
                        # expect a solid keyword
                        if line.startswith ("solid ") or line == "solid":
                            state = 1
                        else:
                            assert False, "expected solid keyword"

                    elif state == 5:
                        if line.startswith ("solid ") or line == "solid":
                            # allow to start on next solid.
                            state = 1
                        else:
                            # expected end of file
                            assert False, "expected end of file"
            assert state == 5, "unexpected end of file"

        # empty list of parsed solids?
        if len (parsedSolids) == 0:
            result = tree.Empty (name, attributes)
        elif len (parsedSolids) == 1:
            result = parsedSolids[0]
        else:
            result = tree.Group (children = parsedSolids, name = name, attributes = attributes)

        # split volumes
        return Polyhedron._splitVolumes (result, name, attributes)


    @staticmethod
    def _loadOffFile (fileName, name: str = None, attributes: Attributes = None):
        """
        Load off file.
        """
        # read file
        with open (fileName) as f:
            state = 0
            points = []
            faces = []
            pointsLeft = None
            facesLeft = None
            for line in f:
                # remove comments and strip line
                line = line.split ('#', 1)[0].strip ()
                if line != "":
                    if state == 2:
                        # parse points
                        values = Polyhedron._parseFloatArgs (line.strip ())
                        assert len (values) == 3, "expected 3 coordinates on point definition"
                        points.append (((values[0], values[1], values[2]), len (points)))
                        pointsLeft -= 1
                        if pointsLeft == 0:
                            state = 3

                    elif state == 3:
                        # parse faces
                        values = Polyhedron._parseIntegerArgs (line.strip ())
                        assert len (values) >= 4, "expected at least 4 values on face definition"
                        vcount = values[0]
                        assert vcount >= 3, "expected at least 3 points on a face definition"
                        fp1 = values[1]
                        fp2 = values[2]
                        fp = values[3]
                        assert fp1 < len (points), "invalid point index"
                        assert fp2 < len (points), "invalid point index"
                        assert fp < len (points), "invalid point index"
                        faces.append ((fp1, fp2, fp))
                        for fpid in range (4, len (values)):
                            fc = values[fpid]
                            assert fc < len (points), "invalid point index"
                            faces.append ((fp1, fp, fc))
                            fp = fc

                        if False:
                            assert values[0] in (3, 4), "expected 3 or 4 points on face definition"
                            assert values[1] < len (points), "invalid point index"
                            assert values[2] < len (points), "invalid point index"
                            assert values[3] < len (points), "invalid point index"
                            faces.append ((values[1], values[2], values[3]))

                        facesLeft -= 1
                        if facesLeft == 0:
                            state = 4

                    elif state == 0:
                        # try to parse file type identifier
                        if line == "OFF":
                            state = 1
                        else:
                            # size definition on first line?
                            values = Polyhedron._parseIntegerArgs (line[3:].strip ())
                            assert len (values) in (2, 3), "invalid size definition"
                            pointsLeft = values[0]
                            facesLeft = values[1]
                        assert pointsLeft > 0, "number of points must be greater zero"
                        assert facesLeft > 0, "number of faces must be greater zero"
                        state = 2

                    elif state == 1:
                        # try to parse number of points and vertexes
                        values = line[3:].strip ().split (" ")
                        assert (len (values) >= 2), "invalid size definition"
                        pointsLeft = int (values[0])
                        facesLeft = int (values[1])
                        assert pointsLeft > 0, "number of points must be greater zero"
                        assert facesLeft > 0, "number of faces must be greater zero"
                        state = 2

                    elif state == 4:
                        assert False, "extra content not expected"

        # abort if no data was parsed
        if len (faces) == 0:
            return tree.Empty (name, attributes)

        # remove duplicates from points
        optPoints, optFaces, optNormals, optUVs = Polyhedron._removeDuplicatesWithIndices (points, faces, None, None)
        poly = Polyhedron (optPoints, optFaces, None, None, name, attributes)

        # split volumes
        return Polyhedron._splitVolumes (poly, name, attributes)



    @staticmethod
    def fromFileOFF (fileName, name: str = None, attributes: Attributes = None):
        """
        Create a Polyhedron by reading an OFF file.
        When the imported solid has disjunct volumes, a :ref:`Group<Group>` of Polyhedrons will be returned.
        When the imported solid has no renderable items, :ref:`Empty<Empty>` will be returned.
        """
        # hash code of file
        fileCreationTime = os.path.getctime (fileName)
        fileSize = os.path.getsize (fileName)
        fileHash = hash (fileName, "Polyhedron from file", fileCreationTime, fileSize)

        # try to load from cache and return with attributes
        loaded = cache.load (fileHash, ".phed")
        if loaded != None:
            return loaded.copy (name = name, attributes = attributes)

        # load off file
        generated = Polyhedron._loadOffFile (fileName, name, attributes)
        cache.store (generated, fileHash, ".phed")
        return generated


    @staticmethod
    def fromFileSTL (fileName, name: str = None, attributes: Attributes = None):
        """
        Create a Polyhedron by reading a STL file.
        When the imported solid has disjunct volumes, a :ref:`Group<Group>` of Polyhedrons will be returned.
        When the imported solid has no renderable items, :ref:`Empty<Empty>` will be returned.
        """
        # hash code of file
        fileCreationTime = os.path.getctime (fileName)
        fileSize = os.path.getsize (fileName)
        fileHash = hash (fileName, "Polyhedron from file", fileCreationTime, fileSize)

        # try to load from cache and return with attributes
        loaded = cache.load (fileHash, ".phed")
        if loaded != None:
            return loaded.copy (name = name, attributes = attributes)

        # load stl file
        generated = Polyhedron._loadStlFile (fileName, name, attributes)
        cache.store (generated, fileHash, ".phed")
        return generated
    

    def _calculateFaceNormalVector (self, face):
        """
        Calculates a normal vector for a face.
        """
        p1 = self.points[face[0]]
        p2 = self.points[face[1]]
        p3 = self.points[face[2]]
        v = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
        w = (p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2])
        normal = (
            (v[1]*w[2] - v[2]*w[1]),
            (v[2]*w[0] - v[0]*w[2]),
            (v[0]*w[1] - v[1]*w[0])
        )
        return vmath.vsNormalize (normal)


    def writeFileOFF (self, file):
        """
        Write Polyhedron to .off file.
        """
        if isinstance (file, str):
            with open (file, "w") as f:
                self.writeFileOFF (f)
        else:
            file.write ("OFF " + str (len (self.points)) + " " + str (len (self.faces)) + " 0\n")
            for point in self.points:
                file.write (str (point[0]) + " " + str (point[1]) + " " + str (point[2]) + "\n")        
            for face in self.faces:
                file.write ("3 " + str (face[0]) + " " + str (face[1]) + " " + str (face[2]) + "\n")        
    

    def writeFileSTL (self, file):
        """
        Write Polyhedron to .stl file.
        """
        """
        Write Polyhedron to .stl file.
        """
        if isinstance (file, str):
            with open (file, "w") as f:
                self.writeFileSTL (f)
        else:
            # write to stl file
            file.write ("solid Part\n")
            for faceId in range (0, len (self.faces)):
                face = self.faces[faceId]
                n1, n2, n3 = self._calculateFaceNormalVector (face)
                file.write ("  facet normal " + str (n1) + " " + str (n2) + " " + str (n3) + "\n")
                file.write ("    outer loop\n")
                for pointId in range (0, 3):
                    px = self.points[face[pointId]][0]
                    py = self.points[face[pointId]][1]
                    pz = self.points[face[pointId]][2]
                    file.write ("      vertex " + str (px) + " " + str (py) + " " + str (pz) + "\n")
                file.write ("    endloop\n")
                file.write ("  endfacet\n")
            file.write ("endsolid Part\n")


    def _createAdjacentFacePoints (self):
        """
        Create pre computed array of adjacent points.
        """
        adjacent = []
        for faceId in range (0, len (self.points)):
            adjacent.append ([])
        for faceId in range (0, len (self.faces)):
            face = self.faces[faceId]
            for edge in range (0, 3):
                pid = face[edge]
                adjacent[pid].append (faceId)
        return adjacent


    def _createFaceNormals (self):
        """
        Pre calculate face normals.
        """
        normals = []
        for faceIndex in range (0, len (self.faces)):
            normals.append (self._calculateFaceNormalVector (self.faces[faceIndex]))
        return normals


    def _calculateSmoothNormal (self, faceIndex, cornerId, angleThreshold, faceNormals):
        """
        Calculates a smoothed normal for a faces corner point.
        """
        nOwn = faceNormals[faceIndex]
        n = nOwn
        otherFaces = self.getAdjacentFacesOnCorner (faceIndex, cornerId)
        for other in otherFaces:
            nOther = faceNormals[other]
            if vmath.calculateAngle (nOwn, nOther) <= angleThreshold:
                n = vmath.vsAdd (n, nOther)
        return vmath.vsNormalize (n)


    @staticmethod
    def _setFaceNormals (face, n1, n2, n3):
        """
        Create new face by overriding face normals.
        """
        nFace = face[0:3] + [n1, n2, n3]
        if len (face) > 6:
            return nFace + face[6:len (face)]
        return nFace


    def smoothNormals (self, thresholdAngle: float = 30):
        """
        Create a new Polyhedron from this one with auto calculated normal vectors for smooth displaying.
        """

        # try to load from cache
        newHash = hash (self, "smooth", thresholdAngle)
        loaded = cache.load (newHash, ".sphed")
        if loaded != None:
            return loaded.copy (name = self.name, attributes = self.attributes)

        # get face normals
        if not "faceNormals" in self._cache:
            self._cache["faceNormals"] = self._createFaceNormals ()
        faceNormals = self._cache["faceNormals"]

        angleThresholdRadiant = thresholdAngle * math.pi / 180.0
        newNormals = polytool._createIndexedList (self.normals)
        if newNormals == None:
            newNormals = []
        newFaces = []

        # create smoothened normals
        for faceIndex in range (0, len(self.faces)):
            face = self.faces[faceIndex]
            ni1 = None if len (face) < 6 else face[3]
            ni2 = None if len (face) < 6 else face[4]
            ni3 = None if len (face) < 6 else face[5]
            n = self._calculateSmoothNormal (faceIndex, 0, angleThresholdRadiant, faceNormals)
            ni1 = len (newNormals)
            newNormals.append ((n, ni1))
            n = self._calculateSmoothNormal (faceIndex, 1, angleThresholdRadiant, faceNormals)
            ni2 = len (newNormals)
            newNormals.append ((n, ni2))
            n = self._calculateSmoothNormal (faceIndex, 2, angleThresholdRadiant, faceNormals)
            ni3 = len (newNormals)
            newNormals.append ((n, ni3))
            newFaces.append (Polyhedron._setFaceNormals (face, ni1, ni2, ni3))

        # optimize normal vectors
        optNormals, mapNormals = polytool._removeDuplicatesVector3 (newNormals)
        optFaces = []
        for faceIndex in range (0, len(newFaces)):
            face = newFaces[faceIndex]
            n1 = None if len (face) < 6 else face[3]
            n2 = None if len (face) < 6 else face[4]
            n3 = None if len (face) < 6 else face[5]
            nr1 = None if n1 == None else mapNormals[n1]
            nr2 = None if n2 == None else mapNormals[n2]
            nr3 = None if n3 == None else mapNormals[n3]
            optFaces.append (Polyhedron._setFaceNormals (face, nr1, nr2, nr3))

        # create polyhedron from parsed data and store to cache
        generated = Polyhedron (self.points, optFaces, optNormals, self.uvvectors, self.name, self.attributes)
        cache.store (generated, newHash, ".sphed")
        return generated


    def isClosed (self):
        """
        Returns True when the Polygon has a closed surface, False otherwise.
        """
        # value already computed?
        if 'isClosedFlag' in self._cache:
            return self._cache['isClosedFlag']

        # count usage of each edge
        edgeUsageCount = {}
        for face in self.faces:
            for edge in range (0, 3):
                pid1 = face[edge % 3]
                pid2 = face[(edge + 1) % 3]
                pid = str (pid1) + "," + str (pid2) if pid1 < pid2 else str (pid2) + "," + str (pid1)
                if pid in edgeUsageCount:
                    edgeUsageCount[pid] = edgeUsageCount[pid] + 1
                else:
                    edgeUsageCount[pid] = 1

        # compute result
        result = True
        for edge in edgeUsageCount:
            if edgeUsageCount[edge] != 2:
                result = False
                break

        # cache result and return
        self._cache['isClosedFlag'] = result
        return result


    @staticmethod
    def fromUnoptimizedMesh (points, faces, normals = None, uvvectors = None, name: str = None, attributes: Attributes = None):
        """
        Returns a Polygon created from an unoptimized mesh.
        Duplicated points, normals and uvvectors will be removed and the face indices will be adjusted.
        """
        # create optimized version of Polyhedron
        newPoints, newFaces, newNormals, newUvs = Polyhedron._removeDuplicatesWithIndices (
            polytool._createIndexedList (points),
            faces,
            polytool._createIndexedList (normals),
            polytool._createIndexedList (uvvectors),
        )
        return Polyhedron (points = newPoints, faces = newFaces, normals = newNormals, uvvectors = newUvs, name = name, attributes = attributes)


    def getFacesContainingPoint (self, pointId: int):
        """
        Returns a tuple containing the indices of the all faces attached to a point.

        This function shall only be called on closed Polyhedrons, otherwise the behaviour will not be defined.
        """
        # get adjacent face cache
        if not "adjacentFacePoints" in self._cache:
            adjacentFacePoints = self._createAdjacentFacePoints ()
            self._cache["adjacentFacePoints"] = adjacentFacePoints
        else:
            adjacentFacePoints = self._cache["adjacentFacePoints"]

        # return indices of faces connected to pointId
        return adjacentFacePoints[pointId]
        

    def getAdjacentFacesOnCorner (self, faceId: int, cornerId: int):
        """
        Returns a list containg the indices of all adjacent faces connected to a corner of a face.
        This function will only return true adjacent faces, so faceId will not be included in the result.

        This function shall only be called on closed Polyhedrons, otherwise the behaviour will not be defined.
        """
        # get adjacent face cache
        if not "adjacentFacePoints" in self._cache:
            adjacentFacePoints = self._createAdjacentFacePoints ()
            self._cache["adjacentFacePoints"] = adjacentFacePoints
        else:
            adjacentFacePoints = self._cache["adjacentFacePoints"]

        # find adjacent faces on corner
        result = []
        pointId = self.faces[faceId][cornerId % 3]
        for face in adjacentFacePoints[pointId]:
            if face != faceId:
                result.append (face)
        return result


    def getAdjacentFaceOnEdge (self, faceId: int, edgeId: int):
        """
        Returns the index ot the adjacent face on a faces edge.
        Each edge is defined by an edgeId: 0 is the edge between point 0 and point 1, 1 is the edge between point 1 and point 2,
        2 is the edge beween point 2 and point 0. Per definition, a closed non-self-intersecting Polyhederon has exactly one adjacent
        face an edge of a face.

        This function shall only be called on closed Polyhedrons, otherwise the behaviour will not be defined.
        """
        # get adjacent face cache
        if not "adjacentFacePoints" in self._cache:
            adjacentFacePoints = self._createAdjacentFacePoints ()
            self._cache["adjacentFacePoints"] = adjacentFacePoints
        else:
            adjacentFacePoints = self._cache["adjacentFacePoints"]

        # find adjacent face
        pointId1 = self.faces[faceId][edgeId % 3]
        pointId2 = self.faces[faceId][(edgeId + 1) % 3]
        for adjacentFaceIndex in adjacentFacePoints[pointId1]:
            if adjacentFaceIndex != faceId:
                adjacentFace = self.faces[adjacentFaceIndex]
                if (adjacentFace[0] == pointId2) or (adjacentFace[1] == pointId2) or (adjacentFace[2] == pointId2):
                    return adjacentFaceIndex
        return None




class LinearExtrude(tree.Node, Solid):
    """
    Converts a :ref:`Shape<Shape>` into a :ref:`Solid<Solid>` by extruding it along the z axis.

    The x/y coordinates are taken from the child geometry, the resulting :ref:`Solid<Solid>` is centered on the z-axis,
    i.e. z-coordinates are in range [-height / 2 .. height / 2].
    """
    def __init__ (self,
                    children: object = None,
                    height: float = 1,
                    twist: float = 0,
                    scale: float = 1.0,
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
        if not isinstance (children[0], tree.Empty):
            dimensions = 3
            assert children[0].dimensions == 2, "Expected a two dimensional child"
        else:
            dimensions = None
    
        super ().__init__ (children = children, name = name, attributes = attributes)
      
        #: Tuple containing a single child. The child must be a two dimensional csg tree :ref:`Item<Item>`.
        self.children = self.children

        # assert height is valid
        assert isinstance (height, (int, float)), "Parameter height must be a float number"
        assert height > 0, "Parameter height must be greater than zero."
        assert isinstance (twist, (int, float)), "Parameter twist must be a float number"
        assert isinstance (scale, (int, float)), "Parameter scale must be a float number"

        # Number of dimensions is always 3 for :ref:`Solids<Solid>`.
        self.dimensions = dimensions

        #: Height of the extruded element.
        self.height = height

        #: Twist in degrees applied along the extrusion.
        self.twist = twist

        #: Scale factor applied along the extrusion. Allows extrusions to be cone shaped.
        self.scale = scale

        # TODO: move this parameter to attributes
        # Number of slices when converting to rasterized shape
        self.slices = None


    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            tree.Node,
            'twist',
            'height',
            'scale'
        )




class RotateExtrude(tree.Node, Solid):
    """
    Extrudes a :ref:`Shape<Shape>` to a :ref:`Solid<Solid>` by rotating it around the z-axis.
    """
    def __init__ (self,
                    children: object = None,
                    angle: float = 360,
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
        if not isinstance (children[0], tree.Empty):
            dimensions = 3
            assert children[0].dimensions == 2, "Expected a two dimensional child"
        else:
            dimensions = None

        super ().__init__ (children = children, name = name, attributes = attributes)

        # Number of dimensions is always 3 for :ref:`Solids<Solid>`.
        self.dimensions = dimensions

        #: Tuple containing a single child. The child must be a two dimensional csg tree :ref:`Item<Item>`.
        self.children = self.children

        #: Angle for extrusion in degrees.
        self.angle = angle


    #: List of attributes for copy construction.
    @staticmethod
    def _copyConstructorAttributes ():
        return (
            tree.Node,
            'angle'
        )




# import algorithms
from . import algorithms




def _toPolyhedronsWrapper (item: tree.Item, rasterizingAttributes: tree.Attributes):
    """
    Do final conversion to Ployhedrons.
    """
    # can load from cache?
    cacheHash = hash (item, "as Polyhedron", rasterizingAttributes)
    loaded = cache.load (cacheHash, ".cphed")
    if loaded != None:
        return loaded

    # convert and store to cache
    poly = algorithms.toPolyhedrons (item, rasterizingAttributes)
    cache.store (poly, cacheHash, ".cphed")
    return poly
