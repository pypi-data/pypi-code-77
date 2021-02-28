class Heap:
    def __init__(self,data=[],get_key = lambda x:x):
        self.data = data
        self.get_key = lambda x:get_key(self.data[x][0])
        self.indices = {}
        
        for i in range(len(data)):
            self.indices[data[i][1]]=i
        for i in range((len(data)-1)//2,-1,-1):
            self.percolate_down(i)

        
    def __str__(self):
        if len(self)==0:
            return 'Empty Heap'
        res=''
        new=0
        for i in range(len(self)):
            res+=str(self.data[i])+' '
            if i==new:
                res+='| '
                new=new*2+2
        return res
    
    
    def __len__(self):
        return len(self.data)
    
    
    def parent(self,i):
        return (i-1)//2
    
    
    def lchild(self,i):
        return i*2+1
    
    
    def rchild(self,i):
        return i*2+2
    
    
    def __getitem__(self,i):
        if i>=len(self):
            raise Exception("trying to retrieve value out of heap")
        
        return self.data[i]
        
        
    def __setitem__(self,i,new):
        if i>=len(self):
            raise Exception("trying to set value out of heap")
        
        self.data[i]=new
            
            
    def swap(self,i,j):
        if i>=len(self) or j>=len(self):
            raise Exception("trying to swap out of heap")
            
            
        self.indices[self[i][1]],self.indices[self[j][1]] = self.indices[self[j][1]],self.indices[self[i][1]]
        self[i],self[j]=self[j],self[i]
            
        
    def percolate_up(self,i):
        parent = self.parent(i)
        while i > 0 and self.get_key(i) < self.get_key(parent):
              self.swap(i,parent)
              i = parent
              parent = self.parent(i)
        
        
    def percolate_down(self,i):
        lchild = self.lchild(i)
        rchild = self.rchild(i)
        
        if lchild >= len(self):
            return
        
        elif rchild >= len(self):
            if self.get_key(lchild) < self.get_key(i):
                self.swap(i,lchild)
                
        else:
            if self. get_key(lchild) <= self.get_key(rchild):
                if self.get_key(lchild) < self.get_key(i):
                    self.swap(i,lchild)
                    self.percolate_down(lchild)
            else:
                if self.get_key(rchild) < self.get_key(i):
                    self.swap(i,rchild)
                    self.percolate_down(rchild)

    
    def get_min(self):
        if len(self) == 0:
            raise Exception('Called get_min on Empty Heap')
        
        return self[0]
    
    
    def extract_min(self):
        if len(self) == 0:
            raise Exception('Called extract_min on Empty Heap')
        last = len(self)-1
        self.swap(0,last)
        
        self.indices.pop(self.data[last][1])
        res = self.data.pop()
        
        self.percolate_down(0)
        return res
        
        
    def insert(self,new):
        self.data.append(new)
        last = len(self)-1
        self.indices[new[1]] = last
        
        self.percolate_up(last)
        
        
    def update_key(self,value,new_key):
        i = self.indices[value]
        self.data[i][0] = new_key
    
        self.percolate_up(i)
        self.percolate_down(i)
        