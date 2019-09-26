# -*- coding:utf-8 -*-
from separator import Separator
import numpy as np
import pyaudio
import threading
from scipy import signal
import scipy.io.wavfile as wf


class Exec(object):
    def __init__(self):
        ## -----*----- コンストラクタ -----*----- ##
        # 分離器
        self.infer = Separator()

        self._pa = pyaudio.PyAudio()
        # 音声入力の設定
        self.settings = {
            'format': pyaudio.paInt16,
            'channels': 1,
            'rate': 8000,
            'chunk': 1024,
        }
        self.stream = self._pa.open(
            format=self.settings['format'],
            channels=self.settings['channels'],
            rate=self.settings['rate'],
            input=True,
            output=True,
            frames_per_buffer=self.settings['chunk']
        )

        self.wav = None
        self.wav_separate = None
        self.is_input = True
        self.is_separate = False
        self.is_end_separate = False

        thread = threading.Thread(target=self.audio_input)
        thread.start()
        thread = threading.Thread(target=self.audio_seaprate)
        thread.start()
        self.audio_output()

    def audio_input(self):
        ## -----*----- 音声入力 -----*----- ##
        while self.stream.is_active():
            self.wav = np.fromstring(self.stream.read(self.settings['chunk'], exception_on_overflow=False),
                                     np.int16)

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
                #wav = self.__istft(spec.T)
                if self.is_end_separate:
                    output = b''.join(self.wav_separate)
                    self.stream.write(output)

    def audio_seaprate(self):
        ## -----*----- 音声分離 -----*----- ##
        while self.stream.is_active():
            if self.is_separate:
                spec = self.__stft(self.wav, to_log=False).T
                spec_pred = self.__stft(self.wav, to_log=True).T

                # 分離
                for t in range(spec.shape[0]):
                    pred = self.infer.predict(spec_pred[t])
                    for i in range(129):
                        if pred[i] > 0.75:
                            spec[t][i] *= pred[i]
                        elif pred[i] > 0.5:
                            spec[t][i] *= 0.1
                        else:
                            spec[t][i] = 0

                self.wav_separate = self.__istft(spec.T)

                self.is_separate = False
                self.is_end_separate = True

    def __stft(self, wav=None, file=None, to_log=True):
        ## -----*----- 短時間フーリエ変換 -----*----- ##
        if file != None:
            wav = wf.read(file)[1]
        spec = signal.stft(wav, fs=self.settings['rate'], nperseg=256)[2]
        if to_log:
            spec = np.where(spec ==0, 0.1**10, spec)
            spec = 10 * np.log10(np.abs(spec))
        return spec

    def __istft(self, spec, to_int=True):
        ## -----*----- 逆短時間フーリエ変換 -----*----- ##
        wav = signal.istft(spec, fs=self.settings['rate'], nperseg=256)[1]
        if to_int:
            wav = np.array(wav, dtype='int16')
        return wav

    def separate(self, wav):
        ## -----*----- 音源分離 -----*-----##
        spec = self.__stft(wav, to_log=False).T
        spec_pred = self.__stft(wav, to_log=True).T

        # 各時間ごとにループ
        for t in range(spec.shape[0]):
            # 推論
            pred = self.predict(spec_pred[t])
            # 分類
            for i in range(self.size[0]):
                if pred[i] > 0.75:
                    spec[t][i] *= pred[i]
                elif pred[i] > 0.5:
                    spec[t][i] *= 0.1
                else:
                    spec[t][i] = 0

        return self.__istft(spec.T)


if __name__ == '__main__':
    obj = Exec()
