# -*- coding: utf-8 -*-
import pyaudio, wave
import os, sys, gc, time, threading, math
import numpy as np
from lib.scripts.recording import Recording
from lib.scripts.console import Console
from separator import Separator


class Detection(Recording):
    def __init__(self):
        ## -----*----- コンストラクタ -----*----- ##
        super().__init__()

        # 分離器
        self.infer = Separator()

        # 親クラスのstreamとは異なる（Float32，rateが2倍）
        self.f_stream = self._pa.open(
            format=pyaudio.paFloat32,
            channels=self.settings['channels'],
            rate=self.settings['rate'] * 4,
            input=True,
            output=False,
            frames_per_buffer=self.settings['chunk']
        )
        # 立ち上がり・下がり検出数
        self.cnt_edge = {'up': 0, 'down': 0}
        # 音量・閾値などの状態保管
        self.state = {'amp': 0, 'total': 0, 'cnt': 0, 'border': 9999, 'average': 0}
        # コンソール出力
        self.console = Console('./config/outer.txt')
        self.color_record = 90
        self.color_separate = 90

        self.is_separate = False

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
                          '\033[{0}m録音中\033[0m'.format(self.color_record), '\033[{0}m分離中\033[0m'.format(self.color_separate), *self.meter())

        if self.is_separate and self.record_end.is_set():
            thread = threading.Thread(target=self.separator)
            thread.start()
            self.is_separate = False
        else:
            # 立ち上がり検出
            if self.up_edge() and self.record_end.is_set() and self.color_separate == 90:
                self.record_start.set()
                self.record_end.clear()
                self.state['border'] = self.state['average']
                self.color_record = 32
            if self.down_edge() and (not self.record_end.is_set()):
                self.record_start.clear()
                self.reset_state()
                self.color_record = 90
                self.is_separate = True
                self.color_separate = 32

    def up_edge(self):
        ## -----*----- 立ち上がり検出 -----*----- ##
        if not self.record_start.is_set():
            if self.state['amp'] >= self.state['border']:
                self.cnt_edge['up'] += 1
            if self.cnt_edge['up'] > 5:
                return True
        return False

    def down_edge(self):
        ## -----*----- 立ち下がり検出 -----*----- ##
        if self.record_start.is_set():
            if self.state['average'] <= self.state['border']:
                self.cnt_edge['down'] += 1
            if self.cnt_edge['down'] > 10:
                self.cnt_edge['up'] = self.cnt_edge['down'] = 0
                return True
        return False

    def reset_state(self):
        ## -----*----- 状態のリセット -----*----- ##
        self.state['total'] = self.state['average'] * 15
        self.state['cnt'] = 15
        if self.state['average'] >= self.state['amp']:
            self.cnt_edge['up'] = 0
        self.pastTime = time.time()

    def update_border(self):
        ## -----*----- 閾値の更新 -----*----- ##
        offset = range(50, 201, 10)
        while not self.is_exit:
            time.sleep(0.2)
            if self.cnt_edge['up'] < 3 and not self.record_start.is_set():
                if int(self.state['average'] / 20) > len(offset) - 1:
                    i = len(offset) - 1
                else:
                    i = int(self.state['average'] / 20)
                self.state['border'] = pow(10, 1.13) * pow(self.state['average'], 0.72)

    def meter(self):
        ## -----*----- 音量メーター生成 -----*----- ##
        meter = [''] * 3
        keys = ['average', 'amp', 'border']
        for i in range(3):
            for j in range(int(self.state[keys[i]] / 20 + 3)):
                meter[i] += '■■'
        if self.record_start.is_set():
            if self.state['average'] >= self.state['border']:
                meter[0] = '\033[94m' + meter[0] + '\033[0m'
        elif self.state['amp'] >= self.state['border']:
            meter[1] = '\033[94m' + meter[1] + '\033[0m'
        return meter

    def separator(self):
        ## -----*----- 音楽分離 -----*----- ##
        self.infer.separate(self.file)
        self.player('./tmp/separate.wav')
        self.color_separate = 90
        return

    def player(self, path):
        ## -----*----- 音楽再生 -----*----- ##
        pa = pyaudio.PyAudio()
        wavFile = wave.open(path, 'rb')
        stream = pa.open(
            format=pa.get_format_from_width(wavFile.getsampwidth()),
            channels=wavFile.getnchannels(),
            rate=wavFile.getframerate(),
            output=True,
        )
        voiceData = wavFile.readframes(self.settings['chunk'])
        while len(voiceData) > 0:
            stream.write(voiceData)
            voiceData = wavFile.readframes(self.settings['chunk'])
        stream.stop_stream()
        stream.close()
        pa.terminate()


if __name__ == '__main__':
    detection = Detection()
    detection.start()
