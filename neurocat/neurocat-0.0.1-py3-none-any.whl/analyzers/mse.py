from .analyzer import Analyzer
from sklearn.metrics import mean_squared_error

class MSEAnalyzer(Analyzer):

    def run(self, **kwargs):
        X, Y = self.data
        Y_pred = self.model.predict(X)
        self.explanation = mean_squared_error(Y, Y_pred)

    def show(self, **kwargs):
        print("MSE: %.3f" % (self.explanation))
