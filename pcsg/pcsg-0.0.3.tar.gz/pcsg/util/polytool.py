from functools import cmp_to_key




def _optimizeEqualsVector2 (x, y):
    return (x[0] == y[0]) and (x[1] == y[1])




def _optimizeEqualsVector3 (x, y):
    return (x[0] == y[0]) and (x[1] == y[1]) and (x[2] == y[2])




def _optimizeCompareVector2 (x, y):
    if x[0][0] < y[0][0]:
        return -1
    if x[0][0] > y[0][0]:
        return 1
    if x[0][1] < y[0][1]:
        return -1
    if x[0][1] > y[0][1]:
        return 1
    return 1




def _optimizeCompareVector3 (x, y):
    if x[0][0] < y[0][0]:
        return -1
    if x[0][0] > y[0][0]:
        return 1
    if x[0][1] < y[0][1]:
        return -1
    if x[0][1] > y[0][1]:
        return 1
    if x[0][2] < y[0][2]:
        return -1
    if x[0][2] > y[0][2]:
        return 1
    return 1




def _removeDuplicatesVector2 (elements):
    """
    Optimize polyhedron: remove duplicates vom 3D vector list, return new list and remapping dictionary
    """
    if elements == None:
        return (None, None)
    if len (elements) == 0:
        return ((), {})
    orderedElements = sorted (elements, key = cmp_to_key (_optimizeCompareVector2))
    newElements = [orderedElements[0][0]]
    elementMap = {orderedElements[0][1] : 0}
    lastElement = orderedElements[0][0]
    for elementId in range (1, len (orderedElements)):
        e = orderedElements[elementId][0]
        if not _optimizeEqualsVector2 (lastElement, e):
            newElements.append (e)
            lastElement = e
        elementMap[orderedElements[elementId][1]] = len (newElements) - 1
    return (newElements, elementMap)




def _removeDuplicatesVector3 (elements):
    """
    Optimize polyhedron: remove duplicates vom 3D vector list, return new list and remapping dictionary
    """
    if elements == None:
        return (None, None)
    if len (elements) == 0:
        return ((), {})
    orderedElements = sorted (elements, key = cmp_to_key (_optimizeCompareVector3))
    newElements = [orderedElements[0][0]]
    elementMap = {orderedElements[0][1] : 0}
    lastElement = orderedElements[0][0]
    for elementId in range (1, len (orderedElements)):
        e = orderedElements[elementId][0]
        if not _optimizeEqualsVector3 (lastElement, e):
            newElements.append (e)
            lastElement = e
        elementMap[orderedElements[elementId][1]] = len (newElements) - 1
    return (newElements, elementMap)




def _createIndexedList (elements):
    if elements == None:
        return None
    indexed = []
    for index in range (0, len (elements)):
        indexed.append ((elements[index], index))
    return indexed
