"""Utility functions"""

import collections
import math

import numpy as np
from scipy.stats import t
from sklearn.metrics import accuracy_score, matthews_corrcoef, mean_absolute_error, \
     mean_squared_error, median_absolute_error, r2_score
from statsmodels.tsa.stattools import acovf


class Metrics:
    """Contains functions including scoring, statistical testing, etc.
    """

    s = 0.00000001 # smoothing constant to prevent division by zero

    @classmethod
    def mape(cls, actual, predictions):
        """Mean Absolute Percentage Error (MAPE)

        :param actual: Actual values (pd.Series or np.Array)
        :param predictions: Predicted values (pd.Series or np.Array)
        :return: MAPE score
        """

        # ensure they are the same shape
        if len(actual.shape) > 1:
            predictions = predictions.reshape(actual.shape[0], actual.shape[1])
        
        mape = np.mean(np.abs((actual - predictions) / (actual + cls.s))) * 100
        return mape.mean()


    @classmethod
    def regression_scores(cls, actual, predictions, prefix='', metrics=('MAE', 'MAPE')):
        """Calculate scores for regression models

        :param actual: Actual values (pd.Series or np.Array)
        :param predictions: Predicted values (pd.Series or np.Array)
        :param prefix: Key prefix (str), defaults to ''
        :param metrics: A list/tuple of metrics to use (list of str)
        :return: A dict of scores
        """

        functions = {
            'MAE': mean_absolute_error,
            'MAE2': median_absolute_error,
            'MAPE': cls.mape,
            'ME': lambda actual, predictions: np.mean(actual - predictions).mean(),
            'MSE': mean_squared_error,
            'R2': r2_score,
            'RMSE': lambda actual, predictions: math.sqrt(mean_squared_error(actual, predictions)),
            # 'SRC_correlation': spearmanr(actual, predictions).correlation,
        }

        scores = {
            f'{prefix}{key}': round(func(actual, predictions), 4)
            for key, func in functions.items()
            if key in metrics
            }

        return scores


    @classmethod
    def classification_scores(cls, actual, predictions, labels, prefix=''):
        """Calculate scores for classification (or anomaly detection) models

        :param actual: Actual values (pd.Series or np.Array)
        :param predictions: Predicted values (pd.Series or np.Array)
        :return: A dict of scores
        """

        if len(labels) == 0:
            raise ValueError('Missing labels in function classification_scores')

        scores = {
            f'{prefix}accuracy': accuracy_score(actual, predictions),
            f'{prefix}matthews_corrcoef': matthews_corrcoef(actual, predictions),
        }
        return scores


    @classmethod
    def dm_test(cls, errors_1, errors_2, alternative='two_sided', horizon=1, power=2):
        """Diebold Mariano test for determinining if forecasts are statistically
         different

        :param errors_1: forecast errors from the first method
        :param errors_2: forecast errors from the second method
        :param alternative: str specifying the alternative hypothesis,
            'two_sided' (default one), 'less' or 'greater'
        :param horizon: forcasting horizon used in calculating errors (errors_1, errors_2)
        :param power: power used in the loss function (usually 1 or 2)
        :return: named tuple containing DM statistic and p-value
        """

        alternatives = ['two_sided', 'less', 'greater']
        if alternative not in alternatives:
            raise ValueError(f"alternative must be one of {alternatives}")

        difference = np.abs(errors_1) ** power - np.abs(errors_2) ** power
        num_vals = difference.shape[0]
        d_cov = acovf(difference, fft=True, nlag=horizon-1)
        d_var = (d_cov[0] + 2 * d_cov[1:].sum()) / num_vals

        if d_var > 0:
            dm_stat = np.mean(difference) / np.sqrt(d_var)
        elif horizon == 1:
            # logger.error('Variance of DM statistic is zero')
            raise ValueError('Variance of DM statistic is zero')
        else:
            # logger.warning('Variance is negative, using horizon h=1')
            return cls.dm_test(errors_1, errors_2, alternative=alternative, horizon=1, power=power)

        # The corrected statistic suggested by HLN
        k = ((num_vals + 1 - 2 * horizon + horizon / num_vals * (horizon - 1)) / num_vals) ** 0.5
        dm_stat *= k

        if alternative == 'two_sided':
            p_value = 2 * t.cdf(-abs(dm_stat), df=num_vals-1)
        else:
            p_value = t.cdf(dm_stat, df=num_vals-1)
            if alternative == 'greater':
                p_value = 1 - p_value

        dm_test_result = collections.namedtuple('dm_test_result', ['dm_stat', 'p_value'])
        return dm_test_result(dm_stat=dm_stat, p_value=p_value)
