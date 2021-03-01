import os
import shutil
import pathlib
import atexit
import weakref
from . import random
from . import hash
from .. import immutable




class _Cache:
    """
    Cache class.
    """
    def __init__ (self, cachePrefix: str, tempPrefix: str, noPersistence: bool):
        # base path of cache directory
        if (cachePrefix == None) or (cachePrefix == ""):
            cachePrefix = ".pcsg.cache"

        #: random sequence, seeded with time stamp
        self.rand = random.RandomSequence ()

        #: cachePrefix supplied to constructor
        self.cachePrefix = cachePrefix

        #: absolute cache directory 
        self.cacheDir = pathlib.Path.absolute (pathlib.Path (cachePrefix + pathlib.os.sep + "cache"))
        if not self.cacheDir.exists ():
            try:
                self.cacheDir.mkdir (parents = True, exist_ok = True)
            except:
                pass

        #: tempPrefix supplied to constructor
        self.tempPrefix = tempPrefix

        #: location for temporary files
        if (tempPrefix == None) or (tempPrefix == ""):
            tempPrefix = cachePrefix + pathlib.os.sep + "temp" + pathlib.os.sep + self._createTempName ()

        #: flag to disable persistence
        self.noPersistence = noPersistence

        #: absolute temp directory, create if not existing
        self.tempDir = pathlib.Path.absolute (pathlib.Path (tempPrefix))
        tempCreated = False
        if not self.tempDir.exists ():
            tempCreated = True
            try:
                self.tempDir.mkdir (parents = True, exist_ok = True)
            except:
                tempCreated = False
        self._tempCreated = tempCreated

        # remove temp folder on application terminate
        atexit.register (self._onTerminate)

        #: weak cached items
        self._weakCache = weakref.WeakValueDictionary ()


    #: Alphabet to choose characters from when creating random temporary file names.
    _tempChars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


    def _createTempName (self, length = 12):
        """
        Generates a temporary name.
        """
        result = ""
        cid = 0
        while cid < length:
            rid = self.rand.intRange (len (_Cache._tempChars) - 1)
            rc = _Cache._tempChars[rid]
            result += rc
            cid += 1
        return result


    def _onTerminate (self):
        """
        Clean up temorary files on termination.
        """
        if self._tempCreated:
            try:
                shutil.rmtree (self.tempDir)
            except:
                pass


    def load (self, fingerprint, suffix):
        """
        Load instance from cache by fingerprint.
        """
        hashKey = '{:016x}'.format (hash ("path", fingerprint)) + "-" + str (suffix)
        cacheEntry = self._weakCache.get (hashKey)
        if cacheEntry != None:
            return cacheEntry
        if self.noPersistence:
            return None
        path = pathlib.Path (self.persistentPath (fingerprint, suffix))
        if path.exists:
            try:
                with path.open ("rb") as file:
                    obj = immutable.DataObject.restore (file, True)
                    self._weakCache[hashKey] = obj
                    return obj
            except:
                return None
        return None


    def store (self, instance, fingerprint, suffix):
        """
        Store instance by fingerprint to cache.
        """
        hashKey = '{:016x}'.format (hash ("path", fingerprint)) + "-" + str (suffix)
        self._weakCache[hashKey] = instance
        if self.noPersistence != True:
            pp = self.persistentPath (fingerprint, suffix, create = True)
            ppPre = pp + ".temp." + self._createTempName ()
            with open (ppPre, "wb") as file:
                instance.store (file)
            try:
                os.rename (ppPre, pp)
            except:
                pass
        return instance


    def persistentPath (self, fingerprint, suffix, create = False):
        """
        Create a persistent path for an item with a fingerprint
        """
        hashStr = '{:016x}'.format (hash ("path", fingerprint))
        hcPath = str (self.cacheDir) + pathlib.os.sep + hashStr[0:2] + pathlib.os.sep + hashStr[2:4]
        hcFile = hcPath + pathlib.os.sep + hashStr[4:len (hashStr)] + "." + suffix
        if create:
            if not pathlib.Path (hcPath).exists ():
                try:
                    pathlib.Path (hcPath).mkdir (parents = True, exist_ok = True)
                except:
                    pass
        return hcFile


    def temppath (self, suffix: str, create: bool = False):
        """
        Create temporary path name.
        """
        pathName = self.tempDir
        fileName = str (pathName) + pathlib.os.sep + self._createTempName ()
        if suffix != None:
            if suffix != "":
                fileName += "." + suffix
        if create:
            if not pathlib.Path (pathName).exists ():
                pathlib.Path (pathName).mkdir (parents = True, exist_ok = True)
        return fileName

"""
Single instance of cache.
"""
_CacheInstance = None




def setup (cachePrefix: str = None, tempPrefix: str = None, noPersistence: bool = False, ignoreIfAlreadySetup: bool = False):
    """
    Setup the cache module. The cache will operate on the directories specified by *cachePrefix* and *tempPrefix*.
    Setup must only be called once, when calling a second time with other parameters, an exception will be thrown.
    """
    global _CacheInstance
    if _CacheInstance != None:
        if not ignoreIfAlreadySetup:
            assert _CacheInstance.cachePrefix == cachePrefix, "Cache was already initialized with different arguments."
            assert _CacheInstance.tempPrefix == tempPrefix, "Cache was already initialized with different arguments."
            assert _CacheInstance.noPersistence == noPersistence, "Cache was already initialized with different arguments."
    else:
        _CacheInstance = _Cache (cachePrefix = cachePrefix, tempPrefix = tempPrefix, noPersistence = noPersistence)
    return _CacheInstance




def instance ():
    """
    Get single instance of cache. If not setup already, the cache will be set up by default parameters.
    """
    global _CacheInstance
    if _CacheInstance != None:
        return _CacheInstance
    else:
        return setup ()




def temporary (suffix: str = None):
    """
    Creates a temporary file name and returns it's absolute path.
    """
    cache = instance ()
    return cache.temppath (suffix)




def load (fingerprint, suffix: str = ""):
    """
    Load data object by fingerprint.
    """
    cache = instance ()
    return cache.load (fingerprint, suffix)




def store (item, fingerprint, suffix: str = ""):
    """
    Store data object by fingerprint.
    """
    cache = instance ()
    return cache.store (item, fingerprint, suffix)




def persistentPath (fingerprint, suffix: str = "", create: bool = False):
    """
    Get persistent absolute path of item by fingerprint.
    """
    cache = instance ()
    return cache.persistentPath (fingerprint, suffix, create)
