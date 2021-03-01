from .model import Model

import numpy as np
import torch
import torch.nn.functional as F

class TorchModel(Model):
    def fit(self, **kwargs):
        #TODO: To be implemented
        pass

    def predict(self,  X):
        X = torch.from_numpy(X.astype(np.float32))
        return self.model(X).detach().numpy()

    def save(self, path):
        torch.save(self.model.state_dict(), path)

class TorchClassificationModel(TorchModel):
    def predict(self,  X):
        X = torch.from_numpy(X.astype(np.float32))
        return F.softmax(self.model(X)).detach().numpy()
