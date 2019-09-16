# -*- coding: utf-8 -*-
import numpy as np
import scipy.io.wavfile as wf
from scipy import signal
import glob, sys


class Infer(object):
    def __init__(self):
        ## -----*----- コンストラクタ -----*-----##
        return

    def __train(self):
        ## -----*----- 学習 -----*-----##
        return

    def stft(self, wav, to_log=True):
        ## -----*----- STFT -----*----- ##
        _, _, spec = signal.stft(wav, fs=8000, nperseg=255)
        if to_log:
            spec = 10 * np.log(np.abs(spec))
        return spec


if __name__ == '__main__':
    infer = Infer()
    rate, wav = wf.read('./tmp/source.wav')
    print(wav)
    spec = infer.stft(wav)
    print(spec)
