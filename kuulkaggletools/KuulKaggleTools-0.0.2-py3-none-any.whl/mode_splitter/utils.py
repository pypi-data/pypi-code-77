import numpy as np
from typing import Union,List,Optional

def _separate_by_modes(
                        X : Union[np.array,np.matrix],
                        y : Union[np.array,np.matrix],
                        r : Optional[float] = None
                    ) -> (np.array,np.array):
    '''
        Separate the input data based on the peaks of of the output space density

        :param X: input space
        :param y: output space
        :param r: radius around output space to collect data from

        :returns input sets, peak_indexes:
    '''        
    from ..utils import get_peaks 
    peaks = get_peaks( y )
    if r is None: r = np.sqrt(len( peaks )) # uniform radius
    std = y.std()
    # means = np.zeros( [len(peaks)]  + list(X.shape[1:])  ) # in case dimensions are greater than 2
    return [np.argwhere( (y >= p-(std/r)) & (p+(std/r) >= y) ) for i,p in enumerate(peaks) ], peaks
