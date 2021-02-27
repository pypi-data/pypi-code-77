
class Helper:
    @staticmethod
    def rreplace(s, old, new, occurrence=1):
        li = s.rsplit(old, occurrence)
        return new.join(li)

class Manager():
    def __init__(self,mgr):
        self.list = {}
        self.mgr=mgr
        self.type = Helper.rreplace(type(self).__name__, 'Manager', '') 

    def add(self,type):
        key = Helper.rreplace(type.__name__,self.type , '')        
        self.list[key]= type(self.mgr)  

    def addConfig(self,key,value):
        self.list[key]= value

    def __getitem__(self,key):
        return self.list[key]  

    def list(self):
        return self.list 

class Enum():
    def __init__(self,values):
        self.values =values

    def values(self):
        return self.values
    
    def value(self,key):
        return self.values[key]

class Task():
    def __init__(self,mgr):
        self.mgr=mgr
 
    def setSpec(self,value):
        self.spec=value

    @property
    def input(self):
        return self.spec['input'] 
    @property
    def output(self):
        return self.spec['output'] 