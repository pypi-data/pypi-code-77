
def npary(arry):
        try:
            try:
                import numpy as np
            except:
                print("Numpy package not installed")
            
        except:
            print("Operation failed! Please check argument type.")   
        x = np.array(arry)
        
        return x


    
def dfv(inpt,val):
    
    for indx, item in enumerate(inpt):
        if type(item)==list:
            dfv(item,val)
        else:
            for i in range(len(inpt)):
                inpt[i]=val
    


def dim(*dim):
    
    def split(arr,parts):
        subEle=len(arr)//parts
        prev=0
        x=[0]*parts
        for i in range(parts): 
            x[i]=arr[prev:prev+subEle]
            prev=prev+subEle
        
        return x

    

    elementsNo=1
    for i in range(len(dim)):
        elementsNo=elementsNo*dim[i]

    c=[0]*(elementsNo)
    
    z=c
    for i in reversed(range(len(dim))):
        if i!=0 :
            z=split(z,len(z)//dim[i])
    return z

 