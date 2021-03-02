#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 09:45:57 2020

@author: benjamin
"""

from tensorflow.keras.models import load_model
import h5py
import silence_tensorflow.auto
import scipy.stats
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # To silence tensorflow warnings
import numpy as np
from .utils import symmetricifft


def open_frequency_decoder(file_name):
    """ open DNN file for frequency domain """
    if not os.path.isfile(file_name):
        raise ValueError('DNN operator file does not exist')
    autoencoder = load_model(file_name)
    f = h5py.File(file_name, 'r')
    fxx = f['frequency'][()]
    return autoencoder, fxx

def open_time_decoder(file_name):  
    """ open DNN file for time domain """
    return load_model(file_name)
    
def predict(file_name, x, train_domain='frequency'):
    """ returns prediction by DNN """
    if train_domain == 'frequency':
        autoencoder, fxx = open_frequency_decoder(file_name)
        return autoencoder.predict(scipy.stats.zscore(x))
    else:
        L = x.shape[0]
        nfft = int(2 * (L-1))
        ceps_coeff = symmetricifft(20 * np.log10(np.abs(x)), nfft)        
        autoencoder = open_time_decoder(file_name)       
        nFeat = autoencoder.input_shape[1]
        ceps_coeff = scipy.stats.zscore(ceps_coeff[:nFeat, :])
        cepsT2 = scipy.stats.zscore(autoencoder.predict(ceps_coeff.T).T)
        Sxx_in = 10**(np.real(np.fft.fft(ceps_coeff, nfft, axis=0))[:L, :] / 20)
        Sxx_trans = 10**(np.real(np.fft.fft(cepsT2, nfft, axis=0))[:L, :] / 20)
    return Sxx_in, Sxx_trans

# def predict(autoencoder, x, train_domain='frequency'):
#     """ returns prediction by DNN """
#     if train_domain == 'frequency':
#         autoencoder.predict(scipy.stats.zscore(x))
#     else:
#         L = x.shape[0]
#         nfft = int(2 * (L - 1))
#         ceps_coeff = symmetricifft(20 * np.log10(np.abs(x)), nfft)        
#         nFeat = autoencoder.input_shape[1]
#         ceps_coeff = scipy.stats.zscore(ceps_coeff[:nFeat, :])
#         cepsT2 = scipy.stats.zscore(autoencoder.predict(ceps_coeff.T).T)
#         Sxx_in = 10**(np.real(np.fft.fft(ceps_coeff, nfft, axis=0))[:L, :] / 20)
#         Sxx_trans = 10**(np.real(np.fft.fft(cepsT2, nfft, axis=0))[:L, :] / 20)
#     return Sxx_in, Sxx_trans