# -*- coding:utf-8 -*-
import numpy as np
import scipy.io.wavfile as wf
import matplotlib.pyplot as plt


fs, wave = wf.read('./tmp/source.wav')
plt.plot(wave)
plt.show()