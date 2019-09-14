# -*- coding: utf-8 -*-
import pyaudio, wave
import time, os, threading, requests


class Recording(object):
    def __init__(self):
        ## -----*----- コンストラクタ -----*----- ##
        self._pa = pyaudio.PyAudio()
        # 音声入力の設定
        self.settings = {
            'format': pyaudio.paInt16,
            'channels': 1,
            'rate': 8000,
            'chunk': 1024,
            'past_second': 0.2
        }
        self.stream = self._pa.open(
            format=self.settings['format'],
            channels=self.settings['channels'],
            rate=self.settings['rate'],
            input=True,
            output=False,
            frames_per_buffer=self.settings['chunk']
        )
        # 音声データの格納リスト（past：欠け補完，main：メインの録音）
        self.audio = {'past': [], 'main': []}
        # 録音開始・終了フラグ
        self.record_start = threading.Event()
        self.record_end = threading.Event()
        # 録音ファイル
        self.file = './tmp/source.wav'

        self.exe()

    def exe(self):
        ## -----*----- 処理実行 -----*----- ##
        # フラグの初期化
        self.is_exit = False
        self.record_start.clear()
        self.record_end.set()

        # 欠け補完部分の録音
        self.past_record(True)

        # サブスレッド起動
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()

    def loop(self):
        ## -----*----- ループ（録音） -----*----- ##
        while not self.is_exit:
            if self.record_start.is_set():
                self.record()
                self.past_record(True)
            else:
                self.past_record(False)

        # 音声録音を行うスレッドを破壊
        del self.thread

    def record(self):
        ## -----*----- 音声録音 -----*----- ##
        # 開始フラグが降りるまで音声データを格納
        while self.record_start.is_set():
            self.audio['main'].append(self.input_audio())
        # ファイル保存
        self.save_audio()

    def past_record(self, init=False):
        ## -----*----- 欠け補完部分の録音 -----*----- ##
        if init:
            self.audio['past'] = []
            for i in range(int(self.settings['rate'] / self.settings['chunk'] * self.settings['past_second'])):
                self.audio['past'].append(self.input_audio())
        else:
            self.audio['past'].pop(0)
            self.audio['past'].append(self.input_audio())



    def save_audio(self):
        ## -----*----- 音声データ保存 -----*----- ##
        # 音声ファイルのフォーマット指定
        wav = wave.open(self.file, 'wb')
        wav.setnchannels(self.settings['channels'])
        wav.setsampwidth(self._pa.get_sample_size(self.settings['format']))
        wav.setframerate(self.settings['rate'])

        # 音声データをファイルに書き込み
        for data in [self.audio['past'], self.audio['main']]:
            wav.writeframes(b''.join(data))
        wav.close()

        # 音声データの初期化
        self.audio = {'past': [], 'main': []}
        self.record_end.set()

    def input_audio(self):
        ## -----*----- 音声入力 -----*----- ##
        return self.stream.read(self.settings['chunk'], exception_on_overflow=False)


if __name__ == '__main__':
    record = Recording()
    time.sleep(1)
    print('start')
    record.record_start.set()
    time.sleep(0.3)
    record.record_start.clear()
    record.is_exit = True