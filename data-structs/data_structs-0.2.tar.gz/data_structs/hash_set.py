from random import randint

class HashSet:
    'Hash Set that uses chaining to resolve conflicts'
    def __init__(self):
        self.p=3049
        self.a=randint(1,self.p-1)
        self.b=randint(0,self.p-1)
        
        self.len=0
        self.capacity=4
        
        self.table=[ [] for _ in range(self.capacity)]
        

    def __len__(self):
        return self.len
    
    
    def is_empty(self):
        return self.len==0
    
    
    def hash(self,key):
        return ((self.a*hash(key)+self.b)%self.p)%self.capacity
    
    
    def resize(self,new_size):
        self.capacity=new_size
        new_table=[ [] for _ in range(self.capacity)]
         
        for row in self.table:
            for key in row:
                hashed_key=self.hash(key)
                new_table[hashed_key].append(key)
        self.table=new_table
         
         
    def add(self,key):
        #doubles if is at capacity
        if self.len==self.capacity:
            self.resize(self.capacity*2)
            
        hashed_key=self.hash(key)
        if key not in self.table[hashed_key]:
            self.table[hashed_key].append(key)
            self.len+=1
     
            
    def remove(self,key):
        #halfs if below 1/4 of capacity
        if self.len*4==self.capacity and self.capacity>4:
            self.resize(self.capacity//2)
        
        hashed_key=self.hash(key)
        if key in self.table[hashed_key]:
            self.table[hashed_key].remove(key)
            self.len-=1
    
            
    def __contains__(self,key):
        hashed_key=self.hash(key)
        return key in self.table[hashed_key]
    
    
    def __str__(self):
        if self.is_empty():
            return 'Empty Set'
        else:
            res=''
            for row in self.table:
                for entry in row:
                    if res=='':
                        res='{'+repr(entry)
                    else:
                        res+=', '+repr(entry)
            res+='}'
            return res
    
    
    def __repr__(self):
        return str(self)

class OASet:
    ''' Hash Set, Open Addressing with Linear Probing 
    used to resolve collisions'''
    def __init__(self):
        self.p=3049
        self.a=randint(1,self.p-1)
        self.b=randint(0,self.p-1)
        
        self.len=0
        self.capacity=16
        
        #for first slot, 0 is empty, 1 is valid, 2 is deleted
        self.table=[ [0,None] for _ in range(self.capacity)]
        

    def __len__(self):
        return self.len
    
    def is_empty(self):
        return len(self)==0
    
    
    def hash(self,key,trial):
        return (((self.a*hash(key)+self.b)%self.p)+trial)%self.capacity
    
    def resize(self,new_size):
        self.capacity=new_size
        new_table=[ [0,None] for _ in range(self.capacity)]
        for entry in self.table:
            if entry[0]==1:
                key = entry[1]
                for i in range(self.capacity):
                    hashed_key=self.hash(key,i)
                    if new_table[hashed_key][0]!=1:
                        new_table[hashed_key][0]=1
                        new_table[hashed_key][1]=key
                        break
        self.table=new_table
       
         
    def add(self,key):
        #doubles if over 1/4 of capacity
        if self.len*4==self.capacity:
            self.resize(self.capacity*2)
            
        for i in range(self.capacity):
            hashed_key=self.hash(key,i)
            if self.table[hashed_key][0]==1:
                if self.table[hashed_key][1]==key:
                    break
            else:
                self.table[hashed_key][0]=1
                self.table[hashed_key][1]=key
                self.len+=1
                break
        else:
            raise Exception("not added to table")

       
    def remove(self,key):
        #halfs if below 1/16 of capacity
        if self.len*16==self.capacity:
            self.resize(self.capacity//2)
        
        for i in range(self.capacity):
            hashed_key=self.hash(key,i)
            if self.table[hashed_key][0]==1:
                if self.table[hashed_key][1]==key:
                    self.table[hashed_key][0]=2
                    self.len-=1
                    break
            elif self.table[hashed_key][0]==0:
                break
                
            
    def __contains__(self,key):
        for i in range(self.capacity):
            hashed_key=self.hash(key,i)
            if self.table[hashed_key][0]==1:
                if self.table[hashed_key][1]==key:
                    return True
            elif self.table[hashed_key][0]==0:
                return False
    
    def __str__(self):
        if self.is_empty():
            return 'Empty Set'
        else:
            res=''
            for entry in self.table:
                if entry[0]==1:
                    if res=='':
                        res='{'+repr(entry[1])
                    else:
                        res+=', '+repr(entry[1])
            res+='}'
            return res
    
    def __repr__(self):
        return str(self)