import math




def CreateMatrix (rows: list):
    """
    Create a matrix.
    """
    assert len (rows) > 0, "matrix must not be empty"
    rl = len (rows[0])
    assert rl > 0, "matrix must not be empty"
    for i in range (1, len (rows)):
        assert rl == len (rows[i]), "all rows must have the same size"
    rowSet = []
    for r in rows:
        rowSet.append (tuple(r))
    return tuple(rowSet)




def multiply (m1, m2):
    """
    Multiply two matrices.
    """
    m1r = len (m1)
    m1c = len (m1[0])       
    m2r = len (m2)
    m2c = len (m2[0])
    rr = m1r
    rc = m2c
    assert m1c == m2r, "Matrix multiplication not defined. Invalid dimensions."
    newRows = []
    for i in range (0, rr):
        newRow = []
        for k in range (0, rc):
            val = 0
            for j in range (0, m1c):
                val = val + (m1[i][j] * m2[j][k])
            newRow.append (val)
        newRows.append (tuple (newRow))
    return tuple(newRows)




def transformPoint2D (matrix, point):
    """
    Special case: transform a 2D point with affinite matrix.
    """
    # TODO: performance optimize
    m1 = (tuple([point[0]]), tuple([point[1]]), tuple([1]))
    tp = multiply (matrix, m1)
    return [tp[0][0], tp[1][0]]




def transformPoint3D (matrix, point):
    """
    Special case: transform a 2D point with affinite matrix.
    """
    # TODO: performance optimize
    m1 = (tuple([point[0]]), tuple([point[1]]), tuple([point[2]]), tuple([1]))
    tp = multiply (matrix, m1)
    return [tp[0][0], tp[1][0], tp[2][0]]




def AffineIdentical2D ():
    return CreateMatrix([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])




def AffineIdentical3D ():
    return CreateMatrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])




def AffineTranslate2D (x, y):
    return CreateMatrix([
        [1, 0, x],
        [0, 1, y],
        [0, 0, 1]
    ])




def AffineTranslate3D (x, y, z):
    return CreateMatrix([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1],
    ])




def AffineScale2D (x, y):
    return CreateMatrix([
        [x, 0, 0],
        [0, y, 0],
        [0, 0, 1]
    ])




def AffineScale3D (x, y, z):
    return CreateMatrix([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ])




def AffineRotate2D (rz):
    pz = rz * math.pi / 180.0
    return CreateMatrix([
        [math.cos (pz), -math.sin (pz), 0],
        [math.sin (pz), math.cos (pz), 0],
        [0, 0, 1]
    ])




def AffineRotate3Dx (rx):
    px = rx * math.pi / 180.0
    return CreateMatrix([
        [1, 0, 0, 0],
        [0, math.cos (px), math.sin (px), 0],
        [0, -math.sin (px), math.cos (px), 0],
        [0, 0, 0, 1],
    ])




def AffineRotate3Dy (ry):
    py = ry * math.pi / 180.0
    return CreateMatrix([
        [math.cos (py), 0, -math.sin (py), 0],
        [0, 1, 0, 0],
        [math.sin (py), 0, math.cos (py), 0],
        [0, 0, 0, 1],
    ])




def AffineRotate3Dz (rz):
    pz = rz * math.pi / 180.0
    return CreateMatrix([
        [math.cos (pz), -math.sin (pz), 0, 0],
        [math.sin (pz), math.cos (pz), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])




def AffineRotate3D (px, py, pz):
    m1 = AffineRotate3Dx (px)
    m2 = AffineRotate3Dy (py)
    m3 = AffineRotate3Dz (pz)
    return multiply (multiply (m3, m2), m1)
