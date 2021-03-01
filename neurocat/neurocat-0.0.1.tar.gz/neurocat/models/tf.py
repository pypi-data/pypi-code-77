from .model import Model

class TFModel(Model):

    def fit(self, **kwargs):
        res =  self.model.fit(kwargs)
        return res.history

    def predict(self, X):
        return self.model.predict(X)

    def save(self, path):
        self.model.save(path)

class TFClassificationModel(TFModel):
    def predict(self, X):
        return self.model.predict(X)
