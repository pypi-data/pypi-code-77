import numpy as np
from typing import Union,List
import cvxpy
# from .enum import TaskType

# def resolve_task_type(y:  Union[np.array,np.matrix] ) -> TaskType:
#     '''
#         Try to resolve the task type based on the output space
#     '''
#     pass
    
def _find_convex_hull(
                        x : Union[np.array,np.matrix]
                    ) -> Union[np.array,np.matrix]:
    '''
        Calculate the convex hull from the set of points in "x"
    '''
    from scipy.spatial import Delaunay,ConvexHull

    triangulation = Delaunay(x)
    unordered = list(triangulation.convex_hull)
    ordered = list(unordered.pop(0))
    while len(unordered) > 0:
        _next = list(i for i, seg in enumerate(unordered) if ordered[-1] in seg) 
        ordered += [point for point in unordered.pop(_next) if point != ordered[-1]]
    return x[ordered]

def _calculate_hypersphere(
                        x : Union[np.array,np.matrix]
                    ) -> Union[np.array,np.matrix]:
    '''
        return the centroid and radius
    '''
    mu = x.mean(axis=0)
    r = (x.max(axis=0) - mu).max() # we could take the mean, but we're going to be safe since this is largely going to be an approximation for separability
    return mu,r

def percentage_in_sphere(
                        x : Union[np.array,np.matrix],
                        mu : float,
                        r : float
                    ) -> float:
    '''
        Calculate the number of points that lie within the hypersphere
    '''
    r2 = r**2
    return  sum( 1 if ((x_i-mu)**2).sum() > r2 else 0  for x_i in x )/len(x)


def doi(
        X : List[Union[np.array,np.matrix]]
    ) -> np.array:
    '''
        Degrees Of Intersection:

        Calculate the percentage of intersection of two or more convex hulls.
        This is valuable for measuring separability in the input space.

        :param X: this should be an n-dimensional array/matrix of shape [b , ...] where "b" is the batch size or number of convex hulls        
    '''
    from matplotlib.path import Path as mplPath
    # X = np.array( X )
    batch_size = len(X)
    m = np.zeros( (batch_size,batch_size) ) # this is the matrix that we'll return
    cnvx_hls = [
        # _find_convex_hull( X[i] ) # this takes too long for high dimensional data, so instead we will approximate with a hypersphere
        _calculate_hypersphere( X[i] )
        for i in range( batch_size )
    ]
    seen = set()
    for i in range( batch_size ):
        for j in range( batch_size ):
            if i == j:m[i,j] = 1.
            elif ( i,j ) not in seen and ( j,i ) not in seen:
                # because we're approximating with a hypersphere, we won't be calling this, instead, we'll just call another function
                # m[i,j] = (1.0 * mplPath( cnvx_hls[i] ).contains_points( X[j] ) ).mean()
                m[i,j] = percentage_in_sphere( X[j], *cnvx_hls[i] )
                m[j,i] = m[i,j] # this isn't neccesarily true since that's not symmetric, but it's faster to make the assumption
                seen.add( (i,j) )
                seen.add( (j,i) )
    return m


def get_peaks(
                X : Union[np.array,np.matrix], 
                bandwidth : float = 0.19310344827586207,
                fast_bandwidth: bool = True # if set to False we will grid search to find the best bandwidth selection, though this can be slow which is why it is not a default
                ) -> Union[np.array,np.matrix]:
    '''
        Apply a KDE or Histogram to the vector x.
        If the bandwidth is None, then we will automatically resolve the bandwitch size
    '''
    from sklearn.neighbors import KernelDensity # density estimator (using sklearn because they scale better, for details see: https://nbviewer.jupyter.org/url/jakevdp.github.com/downloads/notebooks/KDEBench.ipynb)
    from scipy.signal import find_peaks
    if bandwidth is None:
        if fast_bandwidth is False:pass #TODO: implement grid search
    # kde = KernelDensity(kernel='gaussian', bandwidth=bandwidth).fit( X )
    hist,_ = np.histogram( X,
                            # bins=int(np.sqrt(len(X)))+1,
                            density=True )
    peaks,_ = find_peaks( hist )
    return peaks

            


def remove_outliers(
                        M : Union[np.array,np.matrix],
                        return_params : bool = False
                    ) -> (Union[np.array,np.matrix],np.array,'q25s','q75s','medians'):
    '''
        Calculate the quartiles of the input data columns and return the cleaned input arrray
    '''
    q25s,q75s, medians = [], [], []
    for col in M:
        q25 = np.quantile(col,0.25)
        q75 = np.quantile(col,0.75)
        iqr = q75 - q25
        median_ = median.median(col)    
        medians.append( median_ )
        q25s.append( q25 )
        q75s.append( q75 )
        col[ ( col < ( q25 - 1.5*iqr ) ) & ( col < ( q75 + 1.5*iqr ) ) ] = median_
    return M if not return_params else ( M,  q25s, q75s, medians)