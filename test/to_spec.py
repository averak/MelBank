# -*- coding:utf-8 -*-
import numpy as np
import scipy.io.wavfile as wf
from scipy import signal

def stft(wav, to_log=True):
    ## -----*----- STFT -----*----- ##
    _, _, spec = signal.stft(wav, fs=8000, nperseg=256)
    if to_log:
        spec = 10 * np.log(np.abs(spec))
    return spec


wav_format = wf.read('./config/format.wav')[1]
rate, wav = wf.read('./tmp/source.wav')
spec_format = stft(wav_format)
spec = stft(wav)
print(spec_format.shape)
print(spec.shape)