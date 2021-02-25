import tensorflow as tf
from collections import OrderedDict

from dataset_pipe.encoder_list import EncoderList
from dataset_pipe.feeds.base import BaseDataSet, Dataset
from dataset_pipe.generator import XGenerator, XYGenerator
from dataset_pipe.readers.csv_reader import csv_reader
from dataset_pipe.readers.file_reader import file_reader
from dataset_pipe.readers.json_reader import json_reader


class XYDataset(BaseDataSet):

    def __init__(self, content, custom_reader=None):

        self.output_encoder_list = None

        if content == 'json':
            reader = json_reader
        elif content == 'csv':
            reader = csv_reader
        elif content == 'file':
            reader = file_reader
        elif custom_reader is None:
            raise ValueError(
                "Unknown or not supported content type. If you want to use custom reader set custom reader param.")
        else:
            reader = custom_reader

        super().__init__(reader)

    @staticmethod
    def _get_generator(reader, encoders):
        inputs, outputs = encoders

        return XYGenerator(
            data=reader,
            input_encoders=inputs,
            output_encoders=outputs
        )

    @staticmethod
    def _get_tf_data(generator):
        return tf.data.Dataset.from_generator(
            generator,
            output_types=generator.types(),
            output_shapes=generator.shapes()
        ).repeat().prefetch(-1)

    def _get_reader(self, file, skip=None):

        def _data_reader(dataset_file):
            record = 0
            while True:
                for data in self.reader(dataset_file):

                    if skip:
                        record += 1
                        if record < skip:
                            continue

                    if self.map_lambda:
                        # yields data via filter
                        filtered_data = self.map_lambda(data)

                        # skip not mapped values
                        if filtered_data is None:
                            continue

                        if not isinstance(filtered_data, tuple) or len(filtered_data) != 2:
                            raise ValueError("Filter function must return tuple with 2 arguments: input and output")

                        x, y = filtered_data

                        if self._processor is None:
                            yield OrderedDict(x), OrderedDict(y)
                        else:
                            for _x, _y in self._processor(x, y):
                                yield _x, _y
                    else:
                        yield data

        return _data_reader(file)

    def _get_data_generators(self, file):
        encoders = (self.input_encoder_list, self.output_encoder_list)
        reader = self._get_reader(file)
        return self._get_generator(reader, encoders)

    def feed(self, file) -> Dataset:
        generator = self._get_data_generators(file)

        if self.input_encoder_list and self.output_encoder_list:
            dataset = self._get_tf_data(generator)
        else:
            dataset = generator

        input_shapes, output_shapes = generator.shapes()

        return Dataset(dataset, input_shapes, output_shapes)

    def encode(self, input: dict, output=None):
        if output is None:
            output = {}
        self.input_encoder_list = EncoderList(OrderedDict(input))
        self.output_encoder_list = EncoderList(OrderedDict(output))


class XDataset(BaseDataSet):

    def __init__(self):

        def _reader(source):
            for x in source:

                if self.map_lambda:
                    # yields data via filter
                    x = self.map_lambda(x)

                    # skip not mapped values
                    if x is None:
                        continue

                    if self._processor is None:
                        yield OrderedDict(x)
                    else:
                        for _x in self._processor(x):
                            if isinstance(_x, OrderedDict):
                                yield _x
                            else:
                                yield OrderedDict(_x)
                else:

                    yield x

        super().__init__(_reader)

    def encode(self, input: dict):
        self.input_encoder_list = EncoderList(OrderedDict(input))

    def feed(self, data):

        generator = XGenerator(
            data=self.reader(data),
            input_encoders=self.input_encoder_list
        )

        dataset = tf.data.Dataset.from_generator(
            generator,
            output_types=generator.types()
        ).prefetch(-1)

        return Dataset(dataset, generator.shapes(), None)
