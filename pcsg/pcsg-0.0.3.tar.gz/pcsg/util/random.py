import hashlib
import copy
import datetime




class RandomSequence:
    """
    Pseudo random generator.
    """
    def __init__(self, seed = None):
        self.state = hashlib.md5 ()
        if seed != None:
            self.state.update (str (seed).encode ('utf-8'))
        else:
            self.state.update (str (datetime.datetime.now ().utctimetuple ()).encode ('utf-8'))
        self.counter = 0


    def _next(self):
        """
        Get next pseudo random entry MD5.
        """
        self.state.update (str (self.counter).encode ('utf-8'))
        self.counter = self.counter + 17
        return str (self.state.hexdigest ())


    def _nextInteger(self, signed = False):
        """
        Get next 64 bit signed or unsigned integer of random sequence.
        """
        nextVal = self._next ()
        intNum = int ("0x" + (nextVal [0 : 16]), base = 16)
        if signed == False:
            return intNum
        if (intNum & 0x80000000) != 0:
            intNum = 0xffffffff - (intNum + 1)
        return intNum


    def intRange (self, max, min = 0):
        """
        Generate a pseudo random integer in range, max is excluded.
        """
        assert max > min
        dist = max - min
        r = self._nextInteger (False)
        return min + (r % dist)


    def range (self, max = 1.0, min = 0.0):
        """
        Generate a pseudo random float in range [min..max], max is excluded.
        """
        fv = self._nextInteger () * 5.421010861e-20
        assert max > min
        dist = max - min
        return (fv * dist)  + min
