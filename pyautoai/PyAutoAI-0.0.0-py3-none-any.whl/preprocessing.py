"""Functionality for preprocessing data
"""
import logging
import os

from imblearn.combine import SMOTETomek, SMOTEENN
from imblearn.over_sampling import RandomOverSampler, SMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.feature_selection import f_regression, mutual_info_regression, SelectKBest
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, Normalizer, RobustScaler, StandardScaler

from pyautoai.utils import Utils

logger = logging.getLogger('pyautoai')

class Preprocessor:
    """Preprocesses data via imputing, scaling, resampling, etc.
    """

    def __init__(self, **kwargs):
        self.params = {**kwargs}


    def preprocess(self, **kwargs):
        """Divide a dataset into training, validation and test data

        :param X: Features
        :param y: Target(s)
        :return: A dict of DataFrames and Series (11 items)
        """

        self.params.update({**kwargs})
        test_split = kwargs.get('test_split', 0.1)
        val_split = kwargs.get('val_split', 0.1)
        testing = kwargs.get('testing', False)

        if self.params['data_src'] is not None:
            os.makedirs(self.params['data_src'], exist_ok=True)

        # 1. Impute missing data
        features = self.impute(kwargs['features'])
        targets = self.impute(kwargs['targets'])
        data = {'X': features, 'y': targets}

        # 2. Feature Selection
        if len(targets.shape) == 1:
            data = self.feature_selection(data, **kwargs)
        elif kwargs['feature_selection'] is not None:
            logger.warning('Cannot apply 1D feature selection methods to multiple targets')

        # 3. Get test data
        res = train_test_split(data['X'], data['y'], test_size=test_split)
        data.update({
            'X_train_val': res[0], # Training & validation features
            'X_test': res[1], # Test features
            'y_train_val': res[2], # Training and validation target variables
            'y_test': res[3] # Test variables
            })

        # 4. Feature Engineering
        data = self.feature_engineering(data, None, None)

        # 5. Apply resampling to training/validation data
        data = self.resample(data, kwargs['resampling'])

        # 6. Split training and validation sets
        res = train_test_split(data['X_train_val'], data['y_train_val'], test_size=val_split)
        data.update({
            'X_train': res[0], # Training features
            'X_val': res[1], # Validation features
            'y_train': res[2], # Training target variable
            'y_val': res[3] # Validation target variable
            })

        # 7. Apply scaling
        data = self.scale_data(data, kwargs['scaling'], testing)

        return data


    def resample(self, data, mask=None, resampling=None):
        """Apply resampling to dataset

        :param data: A dict of DataFrames & Series, (pd.DataFrame/pd.Series)
        :param mask: Needed if y_train_val is not 1D and contains str labels, defaults to None
        :param resampling: Method of resampling. Expects one of: None, adasyn'
            'random_over_sampling' 'random_under_sampling', 'smote', 'smote_enn', 'smote_tomek'
        :return: The updated 'data' dict
        """

        if mask is not None:
            assert ValueError('Mask functionality not implemented yet')

        resamplers = {
            'adasyn': ADASYN,
            'random_over_sampling': RandomOverSampler,
            'random_under_sampling': RandomUnderSampler,
            'smote': SMOTE,
            'smote_enn': SMOTEENN,
            'smote_tomek': SMOTETomek,
        }

        if resampling is not None:
            resampler = resamplers[resampling.lower()]()
            if mask is not None:
                data['X_train_val'], data['y_train_val'] = resampler \
                    .fit_resample(data['X_train_val'], data['y_train_val'], mask)
            else:
                data['X_train_val'], data['y_train_val'] = resampler \
                    .fit_resample(data['X_train_val'], data['y_train_val'])

        return data


    def scale_data(self, data, method, testing=False):
        """Scales data and checks for NaN and inf.

        Allowed methods: None, minmax, normalize or standard

        :param data: A dict of DataFrames & Series, (pd.DataFrame/pd.Series)
        :param method: Scaling method (str or None)
        :return: The updated 'data' dict
        """

        scalers = {
            'minmax': MinMaxScaler,
            'normalize': Normalizer,
            'robust': RobustScaler,
            'standard': StandardScaler,
        }

        data['X_scaled'] = data['X'].copy()
        if method is not None:
            scaler = scalers[method.lower()]()

            # Fit scaler and transform
            cols = list(data['X_train_val'].columns)
            data['X_scaled'][cols] = scaler.fit_transform(data['X_scaled'][cols])
            data['X_train_val'][cols] = scaler.fit_transform(data['X_train_val'][cols])

			# Transform, but do not re-fit scaler
            data['X_train'][cols] = scaler.transform(data['X_train'][cols])
            data['X_test'][cols] = scaler.transform(data['X_test'][cols])

        if testing:
            assert not np.isnan(data['X_train_val'].values).any()
            assert np.isfinite(data['X_train_val'].values).all()
            assert not np.isnan(data['X_test'].values).any()
            assert np.isfinite(data['X_test'].values).all()
        return data


    def impute(self, data):
        """Forward and back fill missing values in dataframe
            (ignoring the target variable)

        :param data: input data (pd.dataFrame)
        :return: DatFrame with imputed values (pd.dataFrame)
        """

        data = Utils.ndarray_to_pandas(data)

        if len(data.shape) == 1: # 1D data
            data = data.fillna(method='bfill') # backward fill
            data = data.fillna(method='ffill') # backward fill

        else: # 2D data
            for col in data.columns:
                data[col] = data[col].fillna(method='bfill') # backward fill
                data[col] = data[col].fillna(method='ffill') # forward fill
        return data


    def feature_selection(self, data, method='f_regression', **kwargs):
        """Perform feature selection on a dataset

        :param data: A dict of DataFrames & Series, (pd.DataFrame/pd.Series)
        :param method: Feature selection method, defaults to 'f_regression'
        :raises ValueError: Unexpected feature selection method
        :return: Updated dict of data
        """

        method = method.lower()
        cols = list(data['X'].columns)
        feature_limit = kwargs['feature_limit']
        if feature_limit > len(cols):
            feature_limit = 'all'

        if method in ('f_regression', 'fr'):
            selector = SelectKBest(f_regression, feature_limit) # pylint: disable=C0103

        elif method in ('mutual_info_regression', 'mi'):
            selector = SelectKBest(mutual_info_regression, feature_limit) # pylint: disable=C0103

        elif method in ('pearson', 'absolute_pearson_correlation', 'apc'):
            results = []
            # Get Absolute Pearson correlation for each variable
            for col in data['X'].columns:
                weights = abs(stats.pearsonr(data['X'][col], data['y'].iloc[:, 0])[0])
                results.append({'feature': col, 'weight': weights})
            data['scores'] = pd.DataFrame(results)

            # Sort features by score
            data['scores'] = data['scores'].sort_values('weight', ascending=False)
            # Shortlist best features
            features = data['scores'].head(kwargs['feature_limit'])['feature'].values.tolist()
            # Select best features
            data['X'] = data['X'].iloc[:,features]
            selector = None

        elif method is None:
            data['scores'] = None
            selector = None

        else:
            raise ValueError(f'Unexpected method {method}.')

        # Select K best
        if selector is not None:
            selector.fit(data['X'], data['y'])
            # Record and sort scores
            data['scores'] = pd.DataFrame({'feature': cols, 'weight': selector.scores_})
            data['scores'] = data['scores'].sort_values('weight', ascending=False)
            # Select best features
            features = selector.get_support(indices=True)
            data['X'] = data['X'].iloc[:,features]

        data['X'] = Utils.ndarray_to_pandas(data['X'])

        return data


    def feature_engineering(self, data, lag_features, time_features):
        """Create features in a dataset

        :param data: A dict of DataFrame/Series
        :param targets: Target variable(s)
        :param lag_features: A list of column names
        :param time_features: A list of column names
        :return: DataFrame with new and old features
        """

        return data
