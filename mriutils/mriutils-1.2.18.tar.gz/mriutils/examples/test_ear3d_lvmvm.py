#!/usr/bin/env python

import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

class Test:
    def __init__(self, data_path, process_path, input_shape, label_shape, channels, n_classes, save_name, save_path):
        self.data_path = data_path
        self.process_path = process_path
        self.input_shape = input_shape
        self.label_shape = label_shape
        self.channels = channels
        self.n_classes = n_classes
        self.save_name = save_name
        self.save_path = save_path

    def test(self):
        # # [0] configure
        # data_path = 'lvmvm/'
        # process_path = 'processed/lvmvm/'
        # input_shape = (50, 128, 128, 4)
        # label_shape = (50, 128, 128, 1)
        # channels = 4
        # n_classes = 2
        # save_name = 'ear3d_1000e_2b.hdf5'
        # save_path = 'processed/lvmvm/pred/'

        # # [1] process data
        # from mriutils.datasets.lvmvm import LoadH5
        # lh5 = LoadH5(self.data_path, self.process_path)
        # data = lh5.read()
        # lh5.save()

        # [2] load data
        from mriutils.utils.load_data import LoadData
        ld = LoadData(self.process_path)
        ld.load_data_dict()
        train, test, mode_list = ld.data_split()

        from mriutils.utils.resize import Resize
        res = Resize(train, 'data', self.input_shape)
        train = res.run()
        res = Resize(test, 'label', self.label_shape)
        test = res.run()

        # [3] build the model
        from mriutils.models.ear3d import EAR3D
        model = EAR3D(self.input_shape, model_level = 2, n_classes = 2, loss = 'dice', metric = 'dice')

        # [4] train the model
        from mriutils.train import Train
        training = Train(model, train, self.channels, self.n_classes)
        training.train(mode_list[0], mode_list[1], epochs = 1000, batch_size = 2, save_name = self.save_name)

        # [5] test the model
        from mriutils.test import Test
        testing = Test(model, self.save_name, self.channels, self.n_classes, test)
        testing.test(mode_list[0], mode_list[1], self.save_path)
