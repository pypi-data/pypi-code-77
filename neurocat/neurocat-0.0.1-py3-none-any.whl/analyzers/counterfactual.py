from .analyzer import Analyzer
import alibi

class CounterFactualAnalyzer(Analyzer):

    def __init__(self, **kwargs):
        self.model = kwargs.pop('model')
        self.instance = kwargs.pop('instance')
        self.shape = kwargs.pop('shape')

        self.cf = alibi.explainers.CounterFactual(self.model.predict, self.shape, **kwargs)

    def run(self, **kwargs):
        self.explanation = self.cf.explain(self.instance)

    def show(self, **kwargs):
        print(self.explanation.data['cf'])
