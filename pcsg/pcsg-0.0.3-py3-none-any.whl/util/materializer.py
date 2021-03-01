import subprocess
import pathlib
from shutil import copyfile
from .external import openscad




class Materializer:
    """
    Base class of materializer used to render an image from a csg tree or to materialize them into a 3D format.
    """

    def __init__ (self):
        pass


    def name (self):
        """
        Returns the name of the materializer.
        """
        assert False, "To be implemented by child"


    def assertUsable (self):
        """
        Returns None if the materializer is usable, an error string if not.
        """
        assert False, "To be implemented by child"


    def scriptExtension (self):
        """
        Returns the script path extension of the materializer.
        """
        assert False, "To be implemented by child"


    def script (self, csgTree, attributes = None, destinationPath = None):
        """
        Creates a script for materializing or rendering.
        """
        assert False, "To be implemented by child"


    def renderExtensions (self):
        """
        Returns a list of file extensions supported for rendering. When the materializer supports no rendering, the list will be empty.
        """
        assert False, "To be implemented by child"


    def renderDefaultExtension (self):
        """
        Returns the default file extension used for rendering.
        """
        assert False, "To be implemented by child"


    def render (self, csgTree, attributes = None, destinationPath = None, extension = None):
        """
        """
        assert False, "To be implemented by child"


    def materializeExtensions (self):
        """
        Returns a list of file extensions supported for rendering. When the materializer supports no rendering, the list will be empty.
        """
        assert False, "To be implemented by child"


    def materializeDefaultExtension (self):
        """
        Returns the default file extension used for materializing.
        """
        assert False, "To be implemented by child"


    def materialize (self, csgTree, attributes = None, destinationPath = None, extension = None):
        """
        """
        assert False, "To be implemented by child"




class _OpenScadMaterializer (Materializer):
    """
    Materializer using OpenScad.
    """
    def __init__ (self):
        super ().__init__ ()
        self.usableChecked = False
        self.usableError = None


    def name (self):
        return "openscad"


    def assertUsable (self):
        if self.usableChecked:
            return self.usableError
        try:
            result = subprocess.run ([openscad.getOpenScadRunnable (), '--version'], capture_output = True)
            if result.returncode != 0:
                self.usableError = "Can not execute openscad. Is inside PATH variable?"
            else:
                self.usableError = None
        except:
            self.usableError = "Can not execute openscad. Is inside PATH variable?"
        self.usableChecked = True
        return self.usableError
        

    def scriptExtension (self):
        return "scad"


    def script (self, csgTree, attributes = None, destinationPath = None):
        cacheFile = openscad.getScadScript (csgTree, attributes)
        if cacheFile != None:
            if destinationPath != None:
                dstFile = destinationPath + '.' + self.scriptExtension ()
                copyfile (cacheFile, dstFile)
                return dstFile
        return cacheFile


    def renderExtensions (self):
        return ('png', 'svg')


    def renderDefaultExtension (self):
        return 'png'
        

    def render (self, csgTree, attributes = None, destinationPath = None, extension = None):
        # TODO: check valid extension
        if extension == None:
            extension = self.renderExtensions () [0]
        cacheFile = openscad.getRendering (extension, csgTree, attributes)
        if cacheFile != None:
            if destinationPath != None:
                dstFile = destinationPath + '.' + extension
                copyfile (cacheFile, dstFile)
                return dstFile
        return cacheFile

    
    def materializeExtensions (self):
        return ('stl', 'off')


    def materializeDefaultExtension (self):
        return 'stl'


    def materialize (self, csgTree, attributes = None, destinationPath = None, extension = None):
        # TODO: check valid extension
        if extension == None:
            extension = self.materializeExtensions () [0]
        cacheFile = openscad.getMaterialized (extension, csgTree, attributes)
        if cacheFile != None:
            if destinationPath != None:
                dstFile = destinationPath + '.' + extension
                copyfile (cacheFile, dstFile)
                return dstFile
        return cacheFile




#: Static instance of materializer using OpenScad.
OpenScad = _OpenScadMaterializer ()




# list of registered materializers
_registeredMaterializers = [OpenScad]




def getMaterializers ():
    """
    Returns a list of all registered materializer instances.
    """
    return _registeredMaterializers




def getMaterializer (name):
    """
    Returns a materializer by name or None if not found.
    """
    for m in _registeredMaterializers:
        if m.name () == name:
            return m
    return None




def registerMaterializer (materializer):
    """
    Registers a materializer at the registry.
    """
    assert False, "TODO:"
