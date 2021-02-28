import numpy as np
from sklearn.datasets import load_boston
from wsdflow.multipledimensionsfun.fun import *

# Load data
data = load_boston()
X_ = data['data']
Y_ = data['target']
epochs = 500
batch_size = 10

# X_ = np.array([[1,2],[4,5],[7,8]])
# Y_ = np.array([4,5,6])
# epochs = 100
# batch_size = 1

losses, graph = run(X_, Y_, epochs, batch_size)
print(losses)