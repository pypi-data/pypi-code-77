"""Defines main entrypoint(s)"""
import logging

import numpy as np
import pandas as pd

from pyautoai.preprocessing import Preprocessor
from pyautoai.models import ModelBuilder
from pyautoai.io import CsvWriter, IoHandler

logger = logging.getLogger('pyautoai')


class Engine:
    """Main entry point for accessing AI functionality"""

    model_types = ['regression', 'classification', 'anomaly_detection']

    # pylint: disable=R0913
    def __init__(self,
                 features,
                 targets,
                 model_type=None,
                 models=None,
                 scaling=(None, 'minmax', 'normalize', 'robust', 'standard'),
                 resampling=None,
                 feature_selection='pearson',
                 feature_limit=35,
                 multioutput=(None, 'multi', 'chain'),
                 num_iterations=1,
                 num_samples=30,
                 io='csv',
                 output_src='pyautoai_results',
                 data_src='pyautoai_data',
                 seed=0,
                 ):
        """Create an AI 'engine' that will generate models

        :param features: Input data (pd.DataFrame)
        :param targets: Target variable(s) (pd.DataFrame or pd.Series or np.Array)
        :param model_type: Type of model to use. Defaults to None in which case
             Engine will try to guess
        :param models: Names of models to use. Defaults to None in which case
             Engine will use all available
        :param scaling: Feature scaling method. Defaults to tuple of options
        :param resampling: Data resampling method. Defaults to None
        :param feature_selection: Feature selection method. Defaults to 'f_regression'
        :param feature_limit: Preferred number of features. Defaults to 35
        :param multioutput: Multioutput method. Defaults to tuple of options
        :param num_iterations: Number of times to repeat simulation
        :param num_samples: Number of randomized hyperparameter samples to use. Defaultss to 30
        :param io: How to save results. Defaults to 'csv'
        :param output_src: Where to save results. Defaults to 'pyautoai_results'
        :param data_src: Where to save preprocessed data. Defaults to 'pyautoai_data'
        :param seed: Seed for pseudorandom generators. Defaults to 0
        """

        self.params = {
            'features': features,
            'targets': targets,
            'model_type': self.get_model_type(model_type),
            'models': models,
            'scaling': scaling,
            'resampling': resampling,
            'feature_selection': feature_selection,
            'feature_limit': feature_limit,
            'multioutput': multioutput,
            'num_iterations': num_iterations,
            'num_samples': num_samples,
            'io': io,
            'output_src': output_src,
            'data_src': data_src,
            'seed': seed,
        }

        self.validate_params()
        self.get_io_handler()


    def validate_params(self):
        """Valdiate Engine parameters
        """

        # Assert features are a DataFrame
        features = self.params['features']
        if not isinstance(features, pd.DataFrame):
            raise ValueError(f'Features must be a Pandas DataFrame. Got: {type(features)}')

        # Assert features have columns and rows
        if features.shape[0] == 0 or features.shape[1] == 0:
            raise ValueError('Features has no data.')

        # Assert targets are ndarray/pandas object
        targets = self.params['targets']
        if not isinstance(targets, (pd.Series, pd.DataFrame, np.ndarray)):
            raise ValueError(f'Targets must be DataFrame, Series or array. Got: {type(features)}')

        # Assert targets have at least one column
        if targets.shape[0] == 0:
            raise ValueError('Target(s) has no data')

        # Check IO options
        assert self.params['io'] in ('csv', None)

        # Assert scaling is allowed. Convert to iterable if not already
        scaling = self.params['scaling']
        if not isinstance(scaling, (tuple, list)):
            assert scaling in (None, 'minmax', 'normalize', 'robust', 'standard')
            self.params['scaling'] = [scaling]

        # Assert multioutput is allowed. Convert to iterable if not already
        if not isinstance(self.params['multioutput'], (tuple, list)):
            assert self.params['multioutput'] in (None, 'multi', 'chain')
            self.params['multioutput'] = [self.params['multioutput']]

        # Assert models option is None or list with greater than length zero
        assert self.params['models'] is None \
            or (isinstance(self.params['models'], list) and len(self.params['models']) > 0)



    def get_io_handler(self):
        """Select a class for handling IO operations
        """

        if self.params['io'] == 'csv':
            self.io_handler = CsvWriter
        else:
            self.io_handler = IoHandler


    def get_model_type(self, model_type):
        """Validation of model type

        :param model_type: [description]
        :type model_type: [type]
        :raises ValueError: [description]
        :raises NotImplementedError: [description]
        :return: [description]
        :rtype: [type]
        """

        if model_type is None:
            model_type = 'regression'

        elif model_type.lower() not in self.model_types:
            raise ValueError(f'Accepted model types: {self.model_types}')

        elif model_type.lower() == 'anomaly_detection':
            raise NotImplementedError('Anomaly Detection models not implemented yet')

        return model_type.lower()


    def run(self, **kwargs):
        """Process data and create models
        """

        self.params.update(**kwargs)
        self.validate_params()

        scaler_options = self.params['scaling']
        multioutput_options = self.params['multioutput']

        for _ in range(self.params['num_iterations']):

            for scaling in scaler_options:
                self.params['scaling'] = scaling
                data = self.preprocess_data(**kwargs)

                for multioutput in multioutput_options:
                    self.params['multioutput'] = multioutput
                    self.run_models(data, **kwargs)

                self.params['seed'] += 1


    def preprocess_data(self, **kwargs):
        """Preprocess input data via imputation, scaling, resampling, etc.
        """

        self.params.update(**kwargs)
        data = {}

        # try:
        #     data = self.io_handler.read_data(self.params['data_src'])
        # except FileNotFoundError as error:
        #     logger.debug(f'Cannot load preprocessed data: {str(error)}')

        if len(data) == 0:
            logger.debug('Preprocessing...')
            preprocessor = Preprocessor()
            data = preprocessor.preprocess(**self.params)
            self.io_handler.save_data(data, self.params['data_src'])

        return data


    def run_models(self, data, **kwargs):
        """Initiate modelling process
        """

        self.params.update(**kwargs)
        model_builder = ModelBuilder(data, self.io_handler, **self.params)
        model_builder.build_models(**self.params)
