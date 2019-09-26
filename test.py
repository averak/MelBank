# -*- coding:utf-8 -*-
from separator import Separator
import numpy as np
import pyaudio
from scipy import signal


def stft(wav, to_log=True):
    ## -----*----- STFT -----*----- ##
    _, _, spec = signal.stft(wav, fs=8000, nperseg=256)
    if to_log:
        spec = 10 * np.log(np.abs(spec))
    return spec

def istft(spec, to_int=True):
    ## -----*----- 逆短時間フーリエ変換 -----*----- ##
    wav = signal.istft(spec, fs=8000, nperseg=256)[1]
    if to_int:
        wav = np.array(wav, dtype='int16')
    return wav


p = pyaudio.PyAudio()
CHUNK = 2048

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=8000,
                frames_per_buffer=CHUNK,
                input=True,
                output=True)

infer = Separator()
while stream.is_active():
    output = []
    wav = np.fromstring(stream.read(CHUNK, exception_on_overflow=False), np.int16)
    print(wav.shape)
    spec = stft(wav, False).T
    spec_pred = stft(wav, True).T
    for t in range(spec.shape[0]):
        pred = infer.predict(spec_pred[t])
        for i in range(129):
            if pred[i] > 0.75:
                spec[t][i] *= pred[i]
            elif pred[i] > 0.5:
                spec[t][i] *= 0.1
            else:
                spec[t][i] = 0

    wav = istft(spec.T)
    output = b''.join(wav)
    stream.write(output)


stream.stop_stream()
stream.close()
p.terminate()

print("Stop Streaming")
