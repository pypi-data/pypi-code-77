import math




def isVector (any, expectedSize:int = None) -> bool:
    """
    Check if a data type is a valid vector containing only numbers. Optionally, the number of elements can be expected.
    """
    if isinstance (any, (list, tuple)):
        if expectedSize != None:
            if len (any) != expectedSize:
                return False
        for item in any:
            if not ((type (item) == int) or (type (item) == float)):
                return False
        return True
    return False




def assertVector (any, expectedSize: int = None, title: str = None, msg: str = None) -> bool:
    """
    Assert expression is a vector containing only numbers. Optionally, the number of elements can be expected.
    """
    if title == None:
        assert isVector (any), "expected a vector."
    else:
        if msg == None:
            assert isVector (any), title + " must be a vector."
        else:
            assert isVector (any), msg




def isNumber (any):
    """
    Check if data type is a number.
    """
    return (type (any) == int) or (type (any) == float)




def assertNumber (any, title: str = None, msg: str = None) -> None:
    """
    Asserts expression is a number.
    """
    if title == None:
        assert isNumber (any), "expected a number."
    else:
        if msg == None:
            assert isNumber (any), title + " must be a number."
        else:
            assert isNumber (any), msg



def vsAdd (vs1, vs2):
    """
    Add two scalars or vectors with same signature.
    """
    if isinstance (vs1, (int, float)):
        assert isinstance (vs2, (int, float)), "types must match"
        return vs1 + vs2
    assertVector (vs1)
    assertVector (vs2, len (vs1))
    result = []
    for i in range (0, len (vs1)):
        result.append (vs1[i] + vs2[i])
    return result




def vsAddScalar (vs1, vs2):
    """
    Add scalar or vector to scalar value.
    """
    assert isinstance (vs2, (int, float)), "second value must be a number"
    if isinstance (vs1, (int, float)):
        return vs1 + vs2
    assertVector (vs1)
    result = []
    for i in range (0, len (vs1)):
        result.append (vs1[i] + vs2)
    return result




def vsSub (vs1, vs2):
    """
    Difference of two scalars or vectors with same signature.
    """
    if isinstance (vs1, (int, float)):
        assert isinstance (vs2, (int, float)), "types must match"
        return vs1 - vs2
    assertVector (vs1)
    assertVector (vs2, len (vs1))
    result = []
    for i in range (0, len (vs1)):
        result.append (vs1[i] - vs2[i])
    return result




def vsSubScalar (vs1, vs2):
    """
    Difference of scalar or vector and scalar value.
    """
    assert isinstance (vs2, (int, float)), "second value must be a number"
    if isinstance (vs1, (int, float)):
        return vs1 - vs2
    assertVector (vs1)
    result = []
    for i in range (0, len (vs1)):
        result.append (vs1[i] - vs2)
    return result




def vsMul (vs1, vs2):
    """
    Product of two scalars or vectors with same signature.
    """
    if isinstance (vs1, (int, float)):
        assert isinstance (vs2, (int, float)), "types must match"
        return vs1 * vs2
    assertVector (vs1)
    assertVector (vs2, len (vs1))
    result = []
    for i in range (0, len (vs1)):
        result.append (vs1[i] * vs2[i])
    return result




def vsMulScalar (vs1, vs2):
    """
    Product of scalar or vector and scalar value.
    """
    assert isinstance (vs2, (int, float)), "second value must be a number"
    if isinstance (vs1, (int, float)):
        return vs1 * vs2
    assertVector (vs1)
    result = []
    for i in range (0, len (vs1)):
        result.append (vs1[i] * vs2)
    return result




def vsDiv (vs1, vs2):
    """
    Quotient of two scalars or vectors with same signature.
    """
    if isinstance (vs1, (int, float)):
        assert isinstance (vs2, (int, float)), "types must match"
        return vs1 / vs2
    assertVector (vs1)
    assertVector (vs2, len (vs1))
    result = []
    for i in range (0, len (vs1)):
        result.append (vs1[i] / vs2[i])
    return result




def vsDivScalar (vs1, vs2):
    """
    Quotient of scalar or vector and scalar value.
    """
    assert isinstance (vs2, (int, float)), "second value must be a number"
    if isinstance (vs1, (int, float)):
        return vs1 / vs2
    assertVector (vs1)
    result = []
    for i in range (0, len (vs1)):
        result.append (vs1[i] / vs2)
    return result




def vsLength (vs):
    """
    Get length of vector.
    """
    if isinstance (vs, (int, float)):
        return vs if vs >= 0 else -vs
    else:
        assertVector (vs)
        accu = 0
        for component in vs:
            accu = accu + component * component
        return math.sqrt (accu)




def vsNormalize (vs):
    """
    Normalize a vector.
    """
    length = vsLength (vs)
    if length == 0:
        return vs
    return vsDivScalar (vs, length)




def vsScalarProduct (vs1, vs2):
    """
    Scalar product of two vectors with same signature.
    """
    if isinstance (vs1, (int, float)):
        assert isinstance (vs2, (int, float)), "types must match"
        return vs1 * vs2
    assertVector (vs1)
    assertVector (vs2, len (vs1))
    accumulator = 0
    for component in range (0, len (vs1)):
        accumulator += vs1[component] * vs2[component]
    return accumulator




def calculateAngle (vs1, vs2):
    """
    Calculate the angle between two vectors.
    Returns the angle as radiant.
    """
    ma = vsScalarProduct (vs1, vs2) / (vsLength (vs1) * vsLength (vs2))
    if ma > 1:
        ma = 1
    return math.acos (ma)




def distanceLinePoint (lineP1, lineP2, point):
    """
    Calculates the distance between a point and a line defined by two points.
    """
    assertVector (lineP1)
    assertVector (lineP2, len (lineP1))
    assertVector (point, len (lineP1))
    nominator = 0
    denominator = 0
    for component in range (0, len (lineP1)):
        nominator -= lineP2[component] * point[component]
        nominator += lineP1[component] * lineP2[component]
        denominator -= lineP2[component] * lineP2[component]
    s = nominator / denominator
    distSquared = 0
    for component in range (0, len (lineP1)):
        distComponent = point[component] - lineP1[component] - s * lineP2[component]
        distSquared += distComponent * distComponent
    return math.sqrt (distSquared)




def bezier (points, t):
    """
    Calculate point of bezier curve.
    """
    t1 = (1 - t) * (1 - t) * (1 - t)
    t2 = 3 * t * (1 - t) * (1 - t)
    t3 = 3 * t * t * (1 - t)
    t4 = t * t * t
    return vsAdd (vsAdd(vsMulScalar (points[0], t1), vsMulScalar (points[1], t2)), vsAdd(vsMulScalar (points[2], t3), vsMulScalar (points[3], t4)))
