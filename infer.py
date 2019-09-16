# -*- coding: utf-8 -*-
import numpy as np
import scipy.io.wavfile as wf
from scipy import signal
import glob, sys


class Infer(object):
    def __init__(self):
        ## -----*----- コンストラクタ -----*-----##
        # サンプリングレート
        self.rate = wf.read('./config/format.wav')[0]

        rate, wav = wf.read('./tmp/source.wav')
        spec = self.__stft(wav, False)
        ispec = self.__istft(spec)
        print(wav)
        print(ispec)
        self.__build()

    def __build(self):
        ## -----*----- NNを構築 -----*-----##
        return

    def __train(self):
        ## -----*----- 学習 -----*-----##
        return

    def __features_extracter(self):
        ## -----*----- 特徴量を抽出 -----*----- ##
        return

    def __stft(self, wav, to_log=True):
        ## -----*----- 短時間フーリエ変換 -----*----- ##
        _, _, spec = signal.stft(wav, fs=self.rate, nperseg=256)
        if to_log:
            spec = 10 * np.log10(np.abs(spec))
        return spec

    def __istft(self, spec, to_int=True):
        ## -----*----- 逆短時間フーリエ変換 -----*----- ##
        _, wav = signal.istft(spec, fs=self.rate, nperseg=256)
        if to_int:
            wav = np.array(wav,dtype='int16')
        return wav


if __name__ == '__main__':
    infer = Infer()
