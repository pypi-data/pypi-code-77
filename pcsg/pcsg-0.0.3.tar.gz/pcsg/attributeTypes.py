def Material (colorVector):
    """
    Material color.
    """
    if colorVector == None:
        return None
    else:
        assert isinstance (colorVector, (list, tuple))
        assert len (colorVector), 3
        for cid in range (0, 3):
            assert colorVector[cid] >= 0
            assert colorVector[cid] <= 1
        return colorVector
