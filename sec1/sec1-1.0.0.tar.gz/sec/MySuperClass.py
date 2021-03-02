import numpy as np

class gav():
    def __init__ (self):
        print("конструктор")

a = np.array([[1,2,3],
             [4,5,6]])
b = np.array([[7,8],
              [9,10],
              [11,12]])
print (a)
print ("\n",b)
print ("\n hello\n",a.dot(b))