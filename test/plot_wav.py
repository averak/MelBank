# -*- coding:utf-8 -*-
import numpy as np
import scipy.io.wavfile as wf
import matplotlib.pyplot as plt
import glob


fs, wave1 = wf.read('./tmp/mixed.wav')
fs, wave1 = wf.read(glob.glob('./tmp/teach/800Hz/*.wav')[0])
fs, wave2 = wf.read('./tmp/separate.wav')
plt.plot(wave1)
plt.plot(wave2)
plt.show()