# -*- coding:utf-8 -*-
import numpy as np
import scipy.io.wavfile as wf
import matplotlib.pyplot as plt


fs, wave = wf.read('./tmp/source.wav')
pxx, freq, bins, t = plt.specgram(wave, Fs = fs)
plt.show()