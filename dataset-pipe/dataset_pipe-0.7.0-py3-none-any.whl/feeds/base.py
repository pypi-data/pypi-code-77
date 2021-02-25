class Dataset:

    def __init__(self, dataset, input_shape, output_shape):
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.dataset = dataset

    def __iter__(self):
        return self.dataset.__iter__()

    def batch(self, batch):
        return self.dataset.batch(batch)


class BaseDataSet:

    def __init__(self, reader):

        def _filter(data):
            return {
                       'input': data,
                   }, {
                       'output': data,
                   }

        self.reader = reader
        self.map_lambda = _filter
        self._processor = None

    def process(self, func):
        self._processor = func
        return self

    def map(self, map_lambda):
        self.map_lambda = map_lambda
        return self
