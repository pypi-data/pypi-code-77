import inspect
import pickle
from . import util




class Object:
    """
    Base class for immutable objects: only allows attributes to be assigned from the constructor.
    Assigment of attributes outside the constructor will be prohibited.
    """
    def __init__ (self):
        pass


    def __setattr__ (self, name, value):
        """
        Prevent assigning attributes outside from own constructor as tree nodes are immutable.
        """
        stackframe = inspect.stack()[1]
        message = "Can not assign attribute: object is immutable"
        assert stackframe.function in ("__init__", "__setstate__"), message
        assert stackframe[0].f_locals["self"].__class__ == self.__class__, message
        super ().__setattr__ (name, value)


    def __delattr__ (self, name):
        """
        Prevent deleting attributes outside from own constructor as tree nodes are immutable.
        """
        stackframe = inspect.stack()[1]
        message = "Can not assign attribute: object is immutable"
        assert stackframe.function == "__init__", message
        assert stackframe[0].f_locals["self"].__class__ == self.__class__, message
        super ().__delattr__ (name)




class DataObject (Object):
    """
    Base class implementing copy construction, hash and comparison functions for immutable data structures.

    Each derived class must define a static method *_copyConstructorAttributes ()* returning a tuple containing base classes and field names.
    The returned tuple defines which attributes are supplied to the constructor when using the *copy ()* function.

    Each derived class could implement a static method *_compareAttributes ()* to select the fields used for hash and comparision functions.
    When this method is not implemented, *_copyConstructorAttributes ()* will be used instead.
    """
    def __init__ (self):
        super ().__init__ ()

        #: Class hash to check if a persisted objects class has been changed.
        self._restore_class_hash_ = None

        #: Cache dictionary for precomputed values.
        self._cache = {}


    def store (self, file):
        """
        Store *DataObject* to file, serializes all attributes defined by *_compareAttributes ()*.
        """
        pickle.dump (self, file)


    @staticmethod
    def restore (file, noException: bool = True):
        """
        Restore *DataObject* from file, calls the copy constructor after deserialization.
        When *noException* is True, None will be returned on failed restoration, othwerwise an exception will be thrown.
        Restoration will fail if the implementation has been changed.
        """
        if noException:
            try:
                return pickle.load (file)
            except:
                return None
        else:
            return pickle.load (file)


    def copy (self, **assignments):
        """
        Creates a copy of this object with altered parameters.
        All named parameters of the constructor can be applied to this method,
        when a parameter of the constructor is not supplied, the parameter will be
        inherited from the current instance.
        """
        params = {}
        attributes = DataObject._class_get_copy_fields (self.__class__)
        for attribute in attributes:
            params[attribute] = getattr (self, attribute, None)
        for key in assignments:
            params[key] = assignments[key]
        return self.__class__ (**params)


    def __hash__ (self):
        """
        Returns the hash code of this object.
        """
        if 'hash' in self._cache:
            return self._cache['hash']
        h = self._calculateHash ()
        self._cache['hash'] = h
        return h


    def __getstate__ (self):
        """
        Get attributes for persisting item.
        """
        params = {'_restore_class_hash_': util.hash (self.__class__)}
        attributes = DataObject._class_get_compare_fields (self.__class__)
        for attribute in attributes:
            params[attribute] = getattr (self, attribute, None)
        return params

    
    def __setstate__ (self, state):
        """
        Restore object state after reading persisted item.
        """
        self.__dict__ = state
        if self._restore_class_hash_ != util.hash (self.__class__):
            assert False, "Implement proper exception: persisted class doesn't match own implementation."
        params = {}
        attributes = DataObject._class_get_compare_fields (self.__class__)
        for attribute in attributes:
            params[attribute] = getattr (self, attribute, None)
        self.__init__ (**params)


    def _calculateHash (self):
        """
        Default implementation for computing the hash of a tree element. This function depends on the classes
        *_compareAttributes ()* or *_copyConstructorAttributes()* declarations.
        """
        clz = self.__class__
        fields = DataObject._class_get_compare_fields (clz)
        h = str (util.hash (clz)) + "@"
        for field in fields:
            h = h + "," + str (util.hash (getattr (self, field, None)))
        return util.hash (h)


    @staticmethod
    def _class_collect_compare_fields (clz, fields):
        # declares own _copyConstructorAttributes() ?
        attributes = None
        m = getattr (clz, '_compareAttributes', None)
        if m != None:
            mq = m.__qualname__
            if mq == (clz.__qualname__ + '._compareAttributes') and (clz.__module__ == m.__module__):
                attributes = m ()
        if attributes == None:
            m = getattr (clz, '_copyConstructorAttributes', None)
            if m != None:
                mq = m.__qualname__
                if mq == (clz.__qualname__ + '._copyConstructorAttributes') and (clz.__module__ == m.__module__):
                    attributes = m ()
        # process declared class attributes if supplied
        if attributes != None:
            for attribute in attributes:
                if inspect.isclass (attribute):
                    DataObject._class_collect_compare_fields (attribute, fields)
                elif isinstance (attribute, str):
                    if not attribute in fields:
                        fields.append (attribute)
                else:
                    assert False, "Unexpected type in _copyConstructorAttributes"
            return
        # fallback: collect from base classes
        for base in clz.__bases__:
            DataObject._class_collect_compare_fields (base, fields)


    @staticmethod
    def _class_collect_copy_fields (clz, fields):
        # declares own _copyConstructorAttributes() ?
        attributes = None
        className = clz.__qualname__
        m = getattr (clz, '_copyConstructorAttributes', None)
        if m != None:
            mq = m.__qualname__
            if mq == (clz.__qualname__ + '._copyConstructorAttributes') and (clz.__module__ == m.__module__):
                attributes = m ()
        # process declared class attributes if supplied
        if attributes != None:
            for attribute in attributes:
                if inspect.isclass (attribute):
                    DataObject._class_collect_copy_fields (attribute, fields)
                elif isinstance (attribute, str):
                    if not attribute in fields:
                        fields.append (attribute)
                else:
                    assert False, "Unexpected type in _copyConstructorAttributes"
            return
        # fallback: collect from base classes
        for base in clz.__bases__:
            DataObject._class_collect_copy_fields (base, fields)


    @staticmethod
    def _class_get_compare_fields (clz):
        """
        Returns a pre-computed list of field names to be used for hash and equality operations.
        """
#        cache = getattr (clz, '_cache_compare_fields_', None)
        # TODO: fix cache, this is not threadsafe!
#        if cache != None:
#            return cache
        fields = []
        DataObject._class_collect_compare_fields (clz, fields)
#        setattr (clz, '_cache_compare_fields_', fields)
        return fields


    @staticmethod
    def _class_get_copy_fields (clz):
        """
        Returns a pre-computed list of field names to be used to supply to the copy constructor.
        """
#        cache = getattr (clz, '_cache_copy_fields_', None)
        # TODO: fix cache, this is not threadsafe!
#        if cache != None:
#            return cache
        fields = []
        DataObject._class_collect_copy_fields (clz, fields)
#        setattr (clz, '_cache_copy_fields_', fields)
        return fields
