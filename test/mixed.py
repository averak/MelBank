# -*- coding:utf-8 -*-
import scipy.io.wavfile as wf
import glob
print(glob.glob('./tmp/teach/*'))
voice1 = wf.read(glob.glob('./tmp/teach/阿部/*.wav')[0])[1]
voice2 = wf.read(glob.glob('./tmp/teach/お天気お姉さん/*.wav')[0])[1]
mixed = voice1 + voice2
wf.write('./tmp/mixed.wav', 8000, mixed)
