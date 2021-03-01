#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 01:12:02 2020

@author: kuangmeng
"""

from tensorflow.keras.layers import Concatenate, LeakyReLU, Conv2D, Reshape, Input, BatchNormalization, Multiply
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import os
import tensorflow as tf
import sys
sys.path.append(".")
from .modules.losses import Loss
from .modules.metrics import Metric
strategy = tf.distribute.MirroredStrategy()
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

class ProximatorNet:
    def __init__(self, input_shape, n_classes = 2, filter_size = (3, 3), nr_layers = 5, nr_filters = 32, loss = None, metric = None, pretrained_weights = None):
        self.input_shape = input_shape
        self.channels = input_shape[2]
        self.n_classes = n_classes
        self.filter_size = filter_size
        self.nr_filters = nr_filters
        self.nr_layers = nr_layers
        self.pretrained_weights = pretrained_weights
        with strategy.scope():
            self.model = self.structure()
            self.model.compile(optimizer = Adam(lr = 1e-5), 
                           loss = Loss(loss).loss, 
                           metrics = [Metric(metric).metric])
    
    def subproximator(self, tensor, filter_size = (3,3), nr_layers = 5, nr_filters = 32):
        for i in range(int(nr_layers) - 1):
            tensor = Conv2D(kernel_size = filter_size, padding = 'same', filters = nr_filters)(tensor)
            tensor = LeakyReLU(alpha = 0.3)(tensor)
        output_tensor = Conv2D(kernel_size = filter_size, padding = 'same', filters = nr_filters)(tensor)
        return output_tensor

    def structure(self):
        inputs = Input(self.input_shape)
        out1 = self.subproximator(inputs, self.filter_size, self.nr_layers, self.nr_filters)
        out2 = Concatenate(axis = -1)([inputs,out1])
        out3 = Concatenate(axis = -1)([out2, inputs])
        out4 = LeakyReLU()(out3)
        out5 = self.subproximator(out4, self.filter_size, self.nr_layers, self.nr_filters)
        out6 = Concatenate(axis = -1)([inputs, out5])
        out7 = Concatenate(axis = -1)([out4, out6])
        out8 = LeakyReLU()(out7)
        out9 = Conv3D(kernel_size = (1, 1, 1), padding = 'same', filters = self.n_classes)(out8)
        outputs = tf.keras.layers.Softmax(axis=-1)(out9)
        model = Model(inputs, outputs)
        model.summary()
        if(self.pretrained_weights):
        	    model.load_weights(self.pretrained_weights)
        return model
