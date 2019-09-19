# -*- coding:utf-8 -*-
import scipy.io.wavfile as wf
import glob

voice1 = wf.read(glob.glob('./tmp/teach/あー/*.wav')[0])[1]
voice2 = wf.read(glob.glob('./tmp/teach/800Hz/*.wav')[0])[1]
mixed = voice1 + voice2
wf.write('./tmp/mixed.wav', 8000, mixed)
