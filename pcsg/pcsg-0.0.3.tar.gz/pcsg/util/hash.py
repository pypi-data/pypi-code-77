import inspect
import enum




def _hashString (text):
    """
    Compute hash for a string, returns an unsigned 64 bit number.
    """
    value = 0x35af7b2c97a78b9e
    step = 0x072f2b592a4c57f9
    for ch in text:
        value = ((value * 104297) + (step * ord (ch))) & 0xFFFFFFFFFFFFFFFF
    return value




def _hashDict (element):
    """
    Compute hash for a dictionary, returns an unsigned 64 bit number.
    """
    value = "dict"
    for key in sorted(element):
        value = value + ":" + key + "=" + str (_hashArgument (element[key]))
    return _hashString (value)




def _hashList (element):
    """
    Compute hash for a list, returns an unsigned 64 bit number.
    """
    value = "list"
    for e in element:
        value = value + "," + str (_hashArgument (e))
    return _hashString (value)




def _hashObject (element):
    """
    Generate hash for an object, returns an unsigned 64 bit number.
    """
    m = getattr (element, "__hash__", None)
    if (m != None) and (m.__qualname__ != 'object.__hash__'):
        return element.__hash__ ()
    value = str (getattr (element, "__class__", "None")) + "@"
    for memberName in dir (element):
        member = getattr (element, memberName)
        if not memberName in ("__class__", "__dict__", "__doc__", "__module__", "__weakref__", "__slotnames__"):
            if not callable (member):
                value = "!" + memberName + "=" + str (_hashArgument (member))
    return _hashString (value)




_hashClassCache = {}
def _hashClass (element):
    """
    Generate hash for a class, returns an unsigned 64 bit number.
    Hashes of classes will track also code changes.
    """
    if element in _hashClassCache:
        return _hashClassCache[element]
    h = element.__module__ + "@" + element.__qualname__
    for e in sorted (dir (element)):
        entry = getattr (element, e, None)
        if callable (entry):
            h = h + "," + str (_hashFunction (entry))
        else:
            h = h + "/" + str (_hashArgument (entry)) 
    value = _hashString (h)
    _hashClassCache[element] = value
    return value




_hashFunctionCache = {}
def _hashFunction (element):
    """
    Generate hash for a function, returns an unsigned 64 bit number.
    Hashes of classes will track also code changes.
    """
    if element in _hashFunctionCache:
        return _hashFunctionCache[element]
    h = "method@" + element.__qualname__
    code = getattr (element, '__code__', None)
    if code != None:
        h = h + "," + str (_hashString (str (code.co_code))) + "->" + str (_hashArgument (code.co_consts))
    value = _hashString (h)
    _hashFunctionCache[element] = value
    return value




def _hashArgument(element):
    """
    Compute hash code for a single argument, returns an unsigned 64 bit number.
    """
    if element == None:
        return 8726341235
    elif inspect.isclass (element):
        return _hashClass (element)
    elif callable (element):
        # TODO: need refinements for lamda function?
        return _hashFunction (element)
    elif isinstance (element, enum.Enum):
        return _hashString ("e@" + element.__class__.__qualname__ + "@" + element.name + "=" + str (element.value))
    elif isinstance (element, int):
        return _hashString ("i@" + str (element))
    elif isinstance (element, bool):
        return 298374234 if element else -34283749872
    elif isinstance (element, float):
        return _hashString ("f@" + str (element))
    elif isinstance (element, str):
        return _hashString (element)
    elif isinstance (element, (tuple, list)):
        return _hashList (element)
    elif isinstance (element, dict):
        return _hashDict (element)
    elif isinstance (element, object):
        return _hashObject (element)
    assert False, "No rule to hash element."
