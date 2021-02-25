from typing import Union,List,Dict,Optional
import numpy as np
from src.utils import remove_outliers
from sklearn.mixture import GaussianMixture as GMM
from sklearn.ensemble import RandomForestRegressor
from src import BaseTool
from warnings import simplefilter 
simplefilter(action='ignore', category=DeprecationWarning)
class ModeSplitter(BaseTool):
    '''
        Mode Splitter consumes input and target data sets, identifies multimodality and then splits the data into multiple datasets.

        This allows individual predictors to be trained to estimate a smaller hypothesis space, which hopefully increases performance

    '''
    def __init__(
                    self,  
                    split_fn : 'Splitting Function' = GMM,
                    predict_fn : Optional[ callable ] = RandomForestRegressor,
                    predict_kwargs : Optional[dict] = {}
                ):
        super(self.__class__,self).__init__()
        assert hasattr(split_fn, 'fit'), 'Your splitting function requires a "fit(X,y)" function to be usable'
        assert hasattr(split_fn, 'predict'), 'Your splitting function requires a "predict(x)" function to be usable'
        
        if predict_fn is not None:
            assert hasattr(predict_fn, 'fit'), 'Your prediction function requires a "fit(X,y)" function to be usable'
            assert hasattr(predict_fn, 'predict'), 'Your prediction function requires a "predict(x)" function to be usable'

        self.split_fn = split_fn
        self.predict_fn = predict_fn
        self.is_separable = False
        self.is_fit = False
        self.predictors = []
        self.predict_kwargs = predict_kwargs
        self.n_segments    = 0
        self.deg_inter = [[]]

    def _register_predictor(
                            self,
                            fn : 'Trained Predictor Function'
                        ) -> 'self':
        self.predictors.append(
                fn
        )

    def _test_fit(self) -> 'self':
        assert self.is_fit, 'You need to call "fit(X,y)" prior to calling the "_test_fit()" function'

    def fit(
                self,
                X : Union[ np.array,np.matrix ], 
                y : Union[ np.array,np.matrix ],
            ) -> 'self':
        '''
            
        '''
        from .utils import _separate_by_modes
        from ..utils import doi
        _X,_y = X[:],y[:] # copy the arrays
        indexes,peaks = _separate_by_modes(_X,_y)
        self.n_segments = len( indexes )
        separated_xs = [
            _X[idxs].reshape(idxs.shape[0],_X.shape[1]) for idxs in indexes
        ]
        separated_ys = [
            _y[idxs].reshape(idxs.shape[0]) for idxs in indexes
        ]

        labels_n_indexes = np.array([ [i,idx[0]] for i,idxs in enumerate(indexes) for idx in idxs])

        self.idxs = labels_n_indexes[:,1]
        self.labels = labels_n_indexes[:,0]

        self.is_fit = True
        # degrees of intersection
        self.deg_inter = doi(separated_xs)
        self.split_fn = self.split_fn( n_components=len(indexes) ).fit( _X,self.labels )

        # TODO: add bagging
        if self.predict_fn is not None:
            print('creating predictors')
            # scan over input data and then segment out based on the split function's predictions
            # then append the segmented data and fit the predictors for that particular dataset
            datum_x = [ [] ] * self.n_segments
            datum_y = [ [] ] * self.n_segments
            for i,kls in enumerate(self.split_fn.predict(_X) ):
                datum_x[kls].append( _X[i] )
                datum_y[kls].append( _y[i] )
            self.predictors = [
                self.predict_fn( **self.predict_kwargs ).fit( list(separated_xs[_])+datum_x[_],list(separated_ys[_])+datum_y[_] ) for _ in range(len(indexes))
            ]

        return self


    def predict(self,x):
        if len(self.predictors) < 1:return self.split_fn.predict(x)
        else: return [self.predictors[ idx ].predict( [x[idx]] )[0] for idx in self.split_fn.predict(x)]
        



    def vis(
                self,
                mode : Union['Peaks','ConvexHull'] = 'ConvexHull'
            ) -> None:
        pass

        

        


