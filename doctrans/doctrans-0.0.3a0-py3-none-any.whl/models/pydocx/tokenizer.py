from nltk.tokenize.punkt import PunktParameters, PunktTrainer
import nltk.data

class Tokenizer:
    def __init__(self, text):
        self.sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        self._train_tokenizer(self.sent_tokenizer._params, text)

    def _train_tokenizer(self, params: PunktParameters, text):
        trainer = PunktTrainer()
        trainer.train(text)
        trained_params = trainer.get_params()
        params.abbrev_types = set.union(params.abbrev_types, trained_params.abbrev_types)
        params.collocations = set.union(params.collocations, trained_params.collocations)
        params.sent_starters = set.union(params.sent_starters, trained_params.sent_starters)

    def sent_tokenize(self, text) -> [str]:
        return self.sent_tokenizer.tokenize(text)
