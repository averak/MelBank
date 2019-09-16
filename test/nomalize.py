# -*- coding:utf-8 -*-
import numpy as np
import scipy.io.wavfile as wf
from scipy import signal


def nomalize(x, axis=None):
    min = x.min(axis=axis, keepdims=True)
    max = x.max(axis=axis, keepdims=True)
    result = (x - min) / (max - min)
    return result


def stft(wav, to_log=True):
    ## -----*----- STFT -----*----- ##
    _, _, spec = signal.stft(wav, fs=8000, nperseg=255)
    if to_log:
        spec = 10 * np.log(np.abs(spec))
    return spec


rate, wav = wf.read('./tmp/source.wav')
spec = stft(wav)
print(spec)
print(min_max(spec))