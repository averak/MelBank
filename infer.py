# -*- coding: utf-8 -*-
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dropout
from tensorflow.keras import Sequential
import numpy as np
import scipy.io.wavfile as wf
from scipy import signal
import glob, os


class Infer(object):
    def __init__(self):
        ## -----*----- コンストラクタ -----*-----##
        # サンプリングレート
        self.rate = wf.read('./config/format.wav')[0]
        self.speakers = 2

        self.__features_extracter()

        # モデルのビルド
        self.__model = self.__build()
        # モデルの読み込み
        self.load_model('./model/model.hdf5')

    def __build(self):
        ## -----*----- NNを構築 -----*-----##
        model = Sequential()
        model.add(LSTM(units=100, input_shape=(129, 33)))
        model.add(Dropout(0.1))
        model.add(Dense(self.speakers, activation='softmax'))
        # コンパイル
        model.compile(optimizer='rmsprop',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])

        return model

    def __train(self, x, y):
        ## -----*----- 学習 -----*-----##
        self.__model.fit(x, y, nb_epoch=50, batch_size=30)
        return

    def __features_extracter(self):
        ## -----*----- 特徴量を抽出 -----*----- ##
        x = []
        y = []
        speakers = []

        # ===== 音声一覧を格納 ===============
        for speaker in glob.glob('./tmp/teach/*'):
            speakers.append({})
            speakers[-1]['name'] = speaker.split('/')[-1]
            speakers[-1]['stft'] = []

            files = glob.glob('./tmp/teach/{0}/*.wav'.format(speakers[-1]['name']))
            for f in files:
                speakers[-1]['stft'].append(self.__stft(file=f))

        for speaker in speakers:
            print(speaker['stft'][-1].shape)
            return

        return x, y

    def __stft(self, wav=None, file=None, to_log=True):
        ## -----*----- 短時間フーリエ変換 -----*----- ##
        if file != None:
            wav = wf.read(file)[1]
        spec = signal.stft(wav, fs=self.rate, nperseg=256)[2]
        if to_log:
            spec = 10 * np.log10(np.abs(spec))
        return spec

    def __istft(self, spec, to_int=True):
        ## -----*----- 逆短時間フーリエ変換 -----*----- ##
        wav = signal.istft(spec, fs=self.rate, nperseg=256)[1]
        if to_int:
            wav = np.array(wav, dtype='int16')
        return wav

    def nomalize(self, x, axis=None):
        ## -----*----- 0~1に正規化 -----*----- ##
        min = x.min(axis=axis, keepdims=True)
        max = x.max(axis=axis, keepdims=True)
        result = (x - min) / (max - min)
        return result

    def load_model(self, path):
        ## -----*----- 学習済みモデルの読み込み -----*-----##
        # モデルが存在する場合，読み込む
        if os.path.exists(path):
            self.__model.load_model(path)


if __name__ == '__main__':
    infer = Infer()
