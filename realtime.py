# -*- coding: utf-8 -*-
import pyaudio, wave
import os, sys, gc, time, threading, math
import numpy as np
from lib.scripts.console import Console
from filter import Filter


class Detection(object):
    def __init__(self):
        ## -----*----- コンストラクタ -----*----- ##
        # 分離器
        self.filter = Filter()
        thread = threading.Thread(target=self.filter.exe)
        thread.start()

        self._pa = pyaudio.PyAudio()
        # 音声入力の設定
        self.settings = {
            'format': pyaudio.paInt16,
            'channels': 1,
            'rate': 8000 * 4,
            'chunk': 1024,
            'past_second': 0.2
        }
        self.f_stream = self._pa.open(
            format=pyaudio.paFloat32,
            channels=self.settings['channels'],
            rate=self.settings['rate'],
            input=True,
            output=False,
            frames_per_buffer=self.settings['chunk']
        )
        # 音量・閾値などの状態保管
        self.state = {'amp': 0, 'total': 0, 'cnt': 0, 'border': 9999, 'average': 0}
        # コンソール出力
        self.console = Console('./config/outer.txt')

        self.is_exit = False

    def start(self):
        ## -----*----- 検出スタート -----*----- ##
        time.sleep(self.settings['past_second'])
        # 閾値の更新を行うサブスレッドの起動
        self.thread = threading.Thread(target=self.update_border)
        self.thread.start()

        self.pastTime = time.time()

        while not self.is_exit:
            try:
                if time.time() - self.pastTime > 0.5:
                    self.reset_state()
                self.state['cnt'] += 1
                self.detection()
                sys.stdout.flush()
            except KeyboardInterrupt:
                os.system('clear')
                self.is_exit = True

    def detection(self):
        ## -----*----- 立ち上がり・立ち下がり検出 -----*----- ##
        voiceData = np.fromstring(self.f_stream.read(self.settings['chunk'], exception_on_overflow=False), np.float32)
        voiceData *= np.hanning(self.settings['chunk'])
        # 振幅スペクトル（0~8000[Hz]）
        x = np.fft.fft(voiceData)
        # パワースペクトル
        amplitudeSpectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in x]
        # バンドパスフィルタ（100~5000[Hz]）
        amplitudeSpectrum = amplitudeSpectrum[
                            int((self.settings['chunk'] / (self.settings['rate'] * 2)) * 100):
                            int((self.settings['chunk'] / (self.settings['rate'] * 2)) * 5000)]

        # Amp値・平均値の算出
        self.state['amp'] = sum(amplitudeSpectrum)
        self.state['total'] += self.state['amp']
        self.state['average'] = self.state['total'] / self.state['cnt']

        # コンソール出力
        self.console.draw(int(self.state['average']), int(self.state['amp']), int(self.state['border']),
                          '', '', *self.meter())

    def reset_state(self):
        ## -----*----- 状態のリセット -----*----- ##
        self.state['total'] = self.state['average'] * 15
        self.state['cnt'] = 15
        self.pastTime = time.time()

    def update_border(self):
        ## -----*----- 閾値の更新 -----*----- ##
        while not self.is_exit:
            time.sleep(0.2)
            self.state['border'] = pow(10, 1.13) * pow(self.state['average'], 0.72)

    def meter(self):
        ## -----*----- 音量メーター生成 -----*----- ##
        meter = [''] * 3
        keys = ['average', 'amp', 'border']
        for i in range(3):
            for j in range(int(self.state[keys[i]] / 20 + 3)):
                meter[i] += '■■'
        if self.state['amp'] >= self.state['border']:
            meter[1] = '\033[94m' + meter[1] + '\033[0m'
        return meter


if __name__ == '__main__':
    detection = Detection()
    detection.start()
