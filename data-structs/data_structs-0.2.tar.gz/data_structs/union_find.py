class UnionFind():
    def __init__(self):
        self.pointer = {}
        self.size = {}
    
    def add(self,x):
        self.pointer[x] = None
        self.size[x] = 1
        
    def union(self,x,y):
        s1 = self.find(x)
        s2 = self.find(y)
        
        if s1 == s2:
            return
        
        if self.size[s1]>=self.size[s2]:
            self.pointer[s2]=s1
            self.size[s1]+=self.size[s2]
            self.size.pop(s2)
        else:
            self.pointer[s1]=s2
            self.size[s2]+=self.size[s1]
            self.size.pop(s1)
            
    def find(self,x):
        curr = x
        while self.pointer[curr] is not None:
            curr = self.pointer[curr]
        res = curr   
        
        curr = x
        while self.pointer[curr] is not None:
            prev = curr
            curr = self.pointer[curr]
            self.pointer[prev] = res
            
        return res
    
    def same_component(self,x,y):
        return self.find(x) == self.find(y)
    