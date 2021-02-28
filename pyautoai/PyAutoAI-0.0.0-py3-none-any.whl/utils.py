"""Utility functions"""

import pandas as pd
import numpy as np

class Utils:
    """Utility functions"""


    @classmethod
    def ndarray_to_pandas(cls, data):
        """Convert data from ndarray to DataFrame or Series

        :param data: A np.adarray or pandas object
        :return: DataFrame or Series
        """
        if isinstance(data, np.ndarray):
            if len(data.shape) == 1: # 1D data
                data = pd.Series(data)
            else:
                data = pd.DataFrame(data)
        return data
