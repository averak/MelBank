# -*- coding:utf-8 -*-
import scipy.io.wavfile as wf
import glob
print(glob.glob('./tmp/teach/*'))
voice1 = wf.read(glob.glob('./tmp/teach/target/*.wav')[0])[1]
voice2 = wf.read(glob.glob('./tmp/teach/other/*.wav')[0])[1]
print(voice1)
mixed = voice1 + voice2
wf.write('./tmp/mixed.wav', 8000, mixed)
