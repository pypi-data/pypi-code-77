import numpy as np

np.random.seed(1)

X = np.random.randn( 1000, 12 )
X[:300] *= np.pi+np.random.random( (300,12) )
X[:600] *= np.pi+np.random.random( (600,12) )

y = np.random.randn( 1000 )
y[:300] *= np.pi+np.random.random( 300 )
y[:600] *= np.pi+np.random.random( 600 )

from ..src.mode_splitter import ModeSplitter

ms = ModeSplitter()

ms.fit( X,y )