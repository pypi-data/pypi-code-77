from coinlib.helper import log, get_coinlib_backend

class Registrar(object):
    _instance = None
    functionsCallbacks = {}
    statisticsCallbacks = {}
    chartsFactory = None
    statsRuleFactory = None
    statsMethodFactory = None
    iframe_host = get_coinlib_backend()+":3000"
    coinlib_backend = get_coinlib_backend()+":3994"
    chipmunkdb = get_coinlib_backend()

    def __new__(cls):
        if cls._instance is None:
            log.info('Creating the object')
            cls._instance = super(Registrar, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance
    
    def setBackendPath(self, path):
        self.iframe_host = path + ":3000"
        self.coinlib_backend = path + ":3994"
        self.chipmunkdb = path