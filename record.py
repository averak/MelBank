# -*- coding: utf-8 -*-
from separator import Separator
from lib.scripts.recording import Recording
import time, os, threading
import wave, pyaudio

def player(path):
    ## -----*----- 音楽再生 -----*----- ##
    pa = pyaudio.PyAudio()
    wavFile = wave.open(path, 'rb')
    stream = pa.open(
        format=pa.get_format_from_width(wavFile.getsampwidth()),
        channels=wavFile.getnchannels(),
        rate=wavFile.getframerate(),
        output=True,
    )
    voiceData = wavFile.readframes(1024)
    while len(voiceData) > 0:
        stream.write(voiceData)
        voiceData = wavFile.readframes(1024)
    stream.stop_stream()
    stream.close()
    pa.terminate()


infer = Separator()

record = Recording()
os.system('clear')
print('*** ENTERを押して録音開始・終了 ***')

mode = 0  # 0：録音開始，1：録音終了
cnt = 1

while True:
    key = input()

    if mode == 0:
        # 録音開始
        print("===== {0} START ===============".format(cnt))
        record.record_start.set()
        record.record_end.clear()
        mode = 1

    else:
        # 録音終了
        print("===== END ===============")
        record.record_start.clear()
        while not record.record_end.is_set():
            pass
        infer.separate('./tmp/source.wav')
        player('./tmp/separate.wav')
        mode = 0
        cnt += 1
