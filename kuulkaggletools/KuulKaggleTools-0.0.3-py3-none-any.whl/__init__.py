from .mode_splitter import *
from .vis import *

class BaseTool:

    def _test_fit(self):raise NotImplementedError('"_test_fit()" has not been implemented')
    def fit(self,X,y):raise NotImplementedError('"fit(X,y)" has not been implemented')
    def predict(self,X):raise NotImplementedError('"predict(X)" has not been implemented')