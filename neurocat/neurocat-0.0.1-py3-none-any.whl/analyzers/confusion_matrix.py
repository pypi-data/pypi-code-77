import pycm
import numpy as np
from .analyzer import Analyzer

class ConfusionMatrixAnalyzer(Analyzer):

    def run(self, **kwargs):
        X, Y = self.data
        y_true = Y.reshape(-1)
        y_one_hot = self.model.predict(X)
        y_pred = np.argmax(y_one_hot, axis=1).reshape(-1)
        self.cm = pycm.ConfusionMatrix(actual_vector=y_true, predict_vector=y_pred)
    
    def show(self, **kwargs):
        print(self.cm)