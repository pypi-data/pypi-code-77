from random import randint
    
class HashMap:
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
        return len(self)==0
    
        
    def hash(self,key):
        return ((self.a*hash(key)+self.b)%self.p)%self.capacity
    
    def resize(self,new_size):
        self.capacity=new_size
        new_table=[ [] for _ in range(self.capacity)]
         
        for row in self.table:
            for pair in row:
                hashed_key=self.hash(pair[0])
                new_table[hashed_key].append(pair)
        self.table=new_table
        
        
    def __setitem__(self,key,val):
        #doubles if at capacity
        if self.len==self.capacity:
            self.resize(self.capacity*2)
            
        hashed_key=self.hash(key)
        for pair in self.table[hashed_key]:
            if pair[0]==key:
                pair[1]=val
                break
        else:
            self.table[hashed_key].append([key,val])
            self.len+=1
            
    def __getitem__(self,key):
        hashed_key=self.hash(key)
        for pair in self.table[hashed_key]:
            if pair[0]==key:
                return pair[1]
        raise Exception("key not in table")
        
    def __contains__(self,key):
        hashed_key=self.hash(key)
        for pair in self.table[hashed_key]:
            if pair[0]==key:
                return True
        return False
        
    def get(self,key,default=None):
        hashed_key=self.hash(key)
        for pair in self.table[hashed_key]:
            if pair[0]==key:
                return pair[1]
            
        if default!=None:
            return default
        else:
            raise Exception("key not in table")
            
    def pop(self,key):
        #halfs if below 1/4 of capacity
        if self.len*4==self.capacity:
            self.resize(self.capacity//2)
            
        hashed_key=self.hash(key)
        for tup in self.table[hashed_key]:
            if tup[0]==key:
                self.table[hashed_key].remove(tup)
                self.len -= 1
            
    def __str__(self):
        if self.is_empty():
            return 'Empty Map'
        else:
            res=''
            for row in self.table:
                for pair in row:
                    if res=='':
                        res='{'+repr(pair[0])+': '+repr(pair[1])
                    else:
                        res+=', '+repr(pair[0])+': '+repr(pair[1])
            res+='}'
            return res
        
    def __repr__(self):
        return str(self)
    

    
class OAMap:
    '''Hash Map, Open Addressing with linear probing used to 
    resolve collisions'''
    def __init__(self):
        self.p=3049
        self.a=randint(1,self.p-1)
        self.b=randint(0,self.p-1)
        
        self.len=0
        self.capacity=16
        
        #for first slot, 0 is empty, 1 is valid, 2 is deleted
        self.table=[ [0,None,None] for _ in range(self.capacity)]
        

    def __len__(self):
        return self.len
    
    def is_empty(self):
        return len(self)==0
    
    
    def hash(self,key,trial):
        return (((self.a*hash(key)+self.b)%self.p)+trial)%self.capacity
    
    def resize(self,new_size):
        self.capacity=new_size
        new_table=[ [0,None,None] for _ in range(self.capacity)]
        for entry in self.table:
            if entry[0]==1:
                key = entry[1]
                val = entry[2]
                for i in range(self.capacity):
                    hashed_key=self.hash(key,i)
                    if new_table[hashed_key][0]!=1:
                        new_table[hashed_key][0]=1
                        new_table[hashed_key][1]=key
                        new_table[hashed_key][2]=val
                        break
        self.table=new_table
    
       
    def __setitem__(self,key,val):
        #doubles if over 1/4 of capacity
        if self.len*4==self.capacity:
            self.resize(self.capacity*2)
            
        for i in range(self.capacity):
            hashed_key=self.hash(key,i)
            if self.table[hashed_key][0]==1:
                if self.table[hashed_key][1]==key:
                    self.table[hashed_key][2]=val
                    break
            else:
                self.table[hashed_key][0]=1
                self.table[hashed_key][1]=key
                self.table[hashed_key][2]=val
                self.len+=1
                break
        else:
            raise Exception('not added to table')
            
    def __getitem__(self,key):
        for i in range(self.capacity):
            hashed_key=self.hash(key,i)
            if self.table[hashed_key][0]==1:
                if self.table[hashed_key][1]==key:
                    return self.table[hashed_key][2]
                
            if self.table[hashed_key][0]==0:
                raise Exception("key not in table")
                
    def __contains__(self,key):
        for i in range(self.capacity):
            hashed_key=self.hash(key,i)
            if self.table[hashed_key][0]==1:
                if self.table[hashed_key][1]==key:
                    return True
            elif self.table[hashed_key][0]==0:
                return False 
            
    def pop(self,key):
        #halves if below 1/16 of capacity
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

    def get(self,key,default=None):
        if key in self:
            return self[key]
        elif default!=None:
            return default
        else:
            raise Exception('key not in table')
                
    
    def __str__(self):
        if self.is_empty():
            return 'Empty Map'
        else:
            res=''
            for entry in self.table:
                if entry[0]==1:
                    if res=='':
                        res='{'+repr(entry[1])+': '+repr(entry[2])
                    else:
                        res+=', '+repr(entry[1])+': '+repr(entry[2])
            res+='}'
            return res
    
    def __repr__(self):
        return str(self)
        
        
    
    
    
    
        
    
  

    
    
        
