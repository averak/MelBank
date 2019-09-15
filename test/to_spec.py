# -*- coding:utf-8 -*-
import numpy as np
import scipy.io.wavfile as wf
from scipy import signal

def stft(wav, to_log=True):
    ## -----*----- STFT -----*----- ##
    _, _, spec = signal.stft(wav, fs=8000, nperseg=255)
    if to_log:
        spec = 10 * np.log(np.abs(spec))
    return spec


wav = wf.read('./lib/assets/format.wav')[1]
wav = wf.read('./tmp/source.wav')[1]
spec = stft(wav)