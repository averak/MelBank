# -*- coding:utf-8 -*-
import pyaudio, wave
import threading
import numpy as np
import matplotlib.pyplot as plt
from separator import Separator


class Filter(object):
    def __init__(self, is_filter=True):
        ## -----*----- コンストラクタ -----*----- ##
        # 分離器
        self.infer = Separator()

        self._pa = pyaudio.PyAudio()
        # 音声入力の設定
        self.settings = {
            'format': pyaudio.paInt16,
            'channels': 1,
            'rate': 8000,
            'chunk': 1024
        }
        self.stream = self._pa.open(
            format=self.settings['format'],
            channels=self.settings['channels'],
            rate=self.settings['rate'],
            input=True,
            output=True,
            frames_per_buffer=self.settings['chunk']
        )

        # 音声波形を格納
        self.wav = None
        self.wav_separate = None
        # フラグ一覧
        self.is_filter = is_filter
        self.is_input = True
        self.is_separate = False
        self.is_end_separate = False

        self.strage = {'original': np.zeros(1024 * 20), 'separated': np.zeros(1024 * 20)}

    def exe(self):
        ## -----*----- 処理実行 -----*----- ##
        thread = threading.Thread(target=self.audio_input)
        thread.start()
        thread = threading.Thread(target=self.audio_seaprate)
        thread.start()

        self.audio_output()

    def graphplot(self):
        if not self.is_end_separate:
            return
        self.strage['original'] = np.append(np.delete(self.strage['original'], range(1024)), self.wav)
        self.strage['separated'] = np.append(np.delete(self.strage['separated'], range(1024)), self.wav_separate)
        plt.clf()
        # Original
        plt.subplot(311)
        plt.specgram(self.strage['original'], Fs=self.settings['rate'])
        # Separated
        plt.subplot(312)
        plt.specgram(self.strage['separated'], Fs=self.settings['rate'])
        # Pause
        plt.pause(.01)

    def audio_input(self):
        ## -----*----- 音声入力 -----*----- ##
        while self.stream.is_active():
            self.wav = np.fromstring(self.stream.read(self.settings['chunk'], exception_on_overflow=False),
                                     np.int16)

            self.graphplot()

            # 録音開始フラグ反転
            self.is_input = False
            self.is_separate = True

    def audio_output(self):
        ## -----*----- 音声出力 -----*----- ##
        while self.stream.is_active():
            if not self.is_input:
                # 録音開始フラグ反転
                self.is_input = True

                # 再生
                if self.is_end_separate:
                    output = b''.join(self.wav_separate)
                    self.stream.write(output)

    def audio_seaprate(self):
        ## -----*----- 音声分離 -----*----- ##
        while self.stream.is_active():
            if self.is_separate:
                spec = self.infer.stft(self.wav, to_log=False).T
                spec_pred = self.infer.stft(self.wav, to_log=True).T

                # 分離
                if self.is_filter:
                    for t in range(spec.shape[0]):
                        pred = self.infer.predict(spec_pred[t])
                        for i in range(129):
                            if pred[i] > 0.75:
                                spec[t][i] *= pred[i]
                            elif pred[i] > 0.5:
                                spec[t][i] *= 0.1
                            else:
                                spec[t][i] = 0

                self.wav_separate = self.infer.istft(spec.T)

                self.is_separate = False
                self.is_end_separate = True


if __name__ == '__main__':
    obj = Filter()
    obj.exe()
