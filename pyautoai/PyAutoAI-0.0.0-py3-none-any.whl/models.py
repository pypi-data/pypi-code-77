"""Classes for training and selecting models"""

import gc
import random
from time import perf_counter

from sklearn.multioutput import MultiOutputRegressor, RegressorChain

from pyautoai.metrics import Metrics
from pyautoai.ml.sklearn_regression import SklearnRegression
from pyautoai.ml.sklearn_classification import SklearnClassification


class ModelBuilder:
    """Trains Machine Learning models
    """

    def __init__(self, data, io_handler, **kwargs):
        assert isinstance(data, dict)
        self.params = {**kwargs}
        self.data = data
        self.model_type = kwargs['model_type']
        self.io_handler = io_handler

        if self.params['model_type'] == 'regression':
            self.model_spec = SklearnRegression
        elif self.params['model_type'] == 'classification':
            self.model_spec = SklearnClassification
        elif self.params['model_type'] == 'anomaly_detection':
            raise NotImplementedError('Anomaly detection models not implemented yet')
        else:
            raise KeyError(self.params['model_type'])

        self.model_names = self.model_spec.get_model_names()

        models = kwargs['models']
        if models is not None and len(models) > 0:
            for model in models:
                assert model in self.model_names
            self.model_names = models


    def build_models(self, **kwargs):
        """Train machine learning models

        :return: A dict of results
        """

        self.params.update(**kwargs)
        self.modelling_params = {
            k: v for k, v in self.params.items()
            if k not in ('features', 'targets', 'models', 'output', 'io', 'model_type')
            }

        for model_name in self.model_names: # for each model

            # Get unique hyperparameter samples
            model_func, hyperparams = self.model_spec.get_model_spec(model_name)
            param_options = self.get_param_options(hyperparams, kwargs['num_samples'])

            # Train model for each hyperparameter sample
            for params in param_options:
                result, y_pred = self.train_model_instance(model_name, model_func, params)
                self.record_result(result, y_pred)


    def get_param_options(self, search_space, num_samples, seed=0):
        """Sample parameters randomly for a model

        :param search_space: A dict of search space options for a model
        :returns: Hyperparameters for the selected model
        """

        all_samples = []
        if len(search_space) > 0:
            for _ in range(num_samples):
                param_selection = {}

                for i, param in enumerate(search_space): # for each model parameter
                    param_values = search_space[param] # list of grid search values for parameter

                    if len(param_values) > 0:
                        if isinstance(param_values[0], float): # if float select any real number
                            param_selection[param] = random.SystemRandom(seed+i) \
                                .uniform(min(param_values), max(param_values))
                        else: # otherwise choose from grid search list
                            param_selection[param] = random.SystemRandom(seed+i) \
                                .choice(param_values)

                all_samples.append(param_selection)
        else:
            all_samples = [{}]

        # Drop duplicates
        all_samples = [
            dict(t) for t in {
                tuple(sorted(d.items())) for d in all_samples
                }
            ]

        return all_samples


    def train_model_instance(self, model_name, model_func, params):
        """Train a machine learning model instance

        :param model_name: Model name (str)
        :param model_func: Model constructor
        :param params: Model hyperparameters
        :return: A dict of results
        """

        start_time = perf_counter()

        # Initialise model
        model = model_func(**params)
        model.set_params(**params)
        model_params = model.get_params()

        # Handle multiple outputs
        if len(self.data['y'].shape) > 1:
            model = self.multioutput_wrapper(model, model_params)

        # Fit on training data and pre-test on validation data
        model.fit(self.data['X_train'], self.data['y_train'])
        self.data['y_val_pred'] = model.predict(self.data['X_val'])

        # Fit model on training *and* validation data before final testing
        model.fit(self.data['X_train_val'], self.data['y_train_val'])

        # Test model on test data
        self.data['y_test_pred'] = model.predict(self.data['X_test'])

        # Run model across whole dataset
        self.data['y_pred'] = model.predict(self.data['X_scaled'])

        runtime = round(perf_counter() - start_time, 4)

        # Calculate model scores
        val_scores = Metrics.regression_scores(\
            self.data['y_val'], self.data['y_val_pred'], 'val_')

        test_scores = Metrics.regression_scores(\
            self.data['y_test'], self.data['y_test_pred'], 'test_')

        all_data_scores = Metrics.regression_scores(\
            self.data['y'], self.data['y_pred'], 'all_')

        # print(f'{model_name}, {round(runtime, 2)} secs, {test_scores["test_MAPE"]}')

        num_outputs = 1 if len(self.data['y'].shape) == 1 else self.data['y'].shape[1]

        result = {
            'model': model_name,
            'num_outputs': num_outputs,
            **model_params,
            **test_scores,
            'time': runtime,
            **all_data_scores,
            **val_scores,
            **self.modelling_params,
        }

        del model
        gc.collect()
        return result, self.data['y_pred']


    def multioutput_wrapper(self, model, params):
        """Adds a wrapper to a regression model to allow it to deal with
         multiple target variables

        :param model: Model constructor
        :param params: Model hyperparameters
        """

        method = self.params['multioutput']

        # Handle multiple outputs
        if method == 'multi':
            model = MultiOutputRegressor(model)
            model.set_params(**{f'estimator__{k}': v for k, v in params.items()})

        elif method == 'chain':
            model = RegressorChain(model)

        return model


    def record_result(self, result, y_pred):
        """Record the results of training a model to file, DB or API

        (Only file is currently supported)

        :param result: A dict of model scores and params
        :param y_pred: Model predictions
        """

        if self.params['io'] == 'csv':
            self.io_handler.save_results([result], self.params['output_src'])
            self.io_handler.save_predictions(y_pred, result['all_MAE'], \
                result['model'], self.params['output_src'])

        elif self.params['io'] is None:
            pass
