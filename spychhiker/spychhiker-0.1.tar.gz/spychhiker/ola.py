#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 13:56:52 2020

@author: benjamin
"""

import numpy as np
from .utils import nextpow2, symmetricifft, cepstral_filtering
import scipy.signal as ssg

def ola_param(nwin, novlp=None, sr=None):
    
    if novlp is None:
            novlp = int(nwin * 3 / 4)
    novlp = int(novlp)
    if sr is None:    
        nfft = int(nwin)
    else:
        nfft = 2**nextpow2(sr)
        
    nhop = nwin - novlp
    return novlp, nfft, nhop

def init_ola(x, nwin, nhop):
    
    zeros2add = np.zeros((nhop, 1))
    x2 = np.vstack((zeros2add, x.reshape(-1, 1), zeros2add)).squeeze()
    x_out = np.zeros_like(x2)
       
    return x2, x_out

def check_index(x, k, nwin, nhop):
    
    w = ssg.hann(nwin)
    deb = int(k * nhop)
    fin = deb + nwin - 1
    isC = True
    if fin > len(x) - 1:
        fin = len(x) - 1
        isC = False
    idx = np.arange(deb, fin+1).astype(int)
    xwin = x[idx] * w[:len(idx)]
    
    return xwin, idx, isC

def spec_frame(x, k, nwin, nhop, nfft):
    
    L = int(nfft / 2 + 1)
    xwin, idx, isC = check_index(x, k, nwin, nhop)
    fft_xwin = np.fft.fft(xwin, nfft)[:L]
    
    return xwin, fft_xwin, isC, idx

def change_frame(fft_xwin, h_new, h_orig, nfft, idx, x_out, xwin, isChange=True):
    
    init_en = sum(abs(xwin)**2)
    if init_en != 0 or not np.isnan(init_en):   
        if isChange:
            fft_new = fft_xwin * abs(h_new) / abs(h_orig)
            x_new = symmetricifft(fft_new, nfft)
        else: 
            x_new = xwin
        
        x2add = x_new[:len(idx)]    
        new_en = sum(abs(x2add)**2)
        if new_en == 0 or np.isnan(new_en):            
            pass
        else:
            x_out[idx] = x_out[idx] + x2add * init_en / new_en       
    
    return x_out

def check_frame(k, isC, maxFrame):
    
    k += 1
    if k >= maxFrame:
        isC = False
        
    return k, isC

# def cepstral_transform(x, sxx_in, sxx_out):
    
#     nwin = len(x)
#     L = int(nwin/2 + 1)
#     fft_x = np.fft.fft(x, nwin)[:L]
#     fft_trans = fft_x * abs(sxx_out) / abs(sxx_in)
#     return symmetricifft(fft_trans, nwin)

# def recursive_cepstral_transform(x, sr, sxx_out, thresh=1, eps=1, n_max=2):  
    
#     sxx_in, _ = cepstralenvelope(x, sr)
#     err = nrmse(sxx_out, sxx_in)   
#     d_sxx = 0
#     nb_iter = 0
#     while (err > thresh and nb_iter < n_max):
#         sxx_kp1 = sxx_out + eps * d_sxx
#         sig_k = cepstral_transform(x, sxx_in, sxx_kp1)
#         sxx_k, _ = cepstralenvelope(sig_k, sr)
#         err = nrmse(sxx_out, sxx_k)
#         print(err)
#         d_sxx = sxx_out - sxx_k 
#         nb_iter += 1

#     return sig_k

# def nrmse(x, y):
#     return 100 * np.sqrt(np.mean((x-y)**2)) / np.mean(x) 

# def cepstralenvelope(x, order):
    
#     nwin = len(x)
#     w = np.hamming(nwin)
    
#     xwin = x * w
#     logx = np.log(abs(np.fft.fft(xwin)))
#     L = int(nwin / 2 + 1)
#     xEnv = cepstral_filtering(logx, nwin, order)
#     Sxx = np.exp(xEnv[:L])
    
#     return Sxx

