from alibi.explainers import ALE, plot_ale
from .analyzer import Analyzer

class ALEAnalyzer(Analyzer):
    def __init__(self, **kwargs):
        self.model = kwargs.pop('model')
        self.data = kwargs.pop('data')
        self.fig_kw = kwargs.pop('fig_kw')
        self.ale = ALE(self.model.predict, **kwargs)

    def run(self, **kwargs):
        self.explanation = self.ale.explain(self.data)
    
    def show(self, **kwargs):
        plot_ale(self.explanation, fig_kw=self.fig_kw)