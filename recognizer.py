# -*- coding: utf-8 -*-
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dropout
from tensorflow.keras import Sequential
import numpy as np
import scipy.io.wavfile as wf
from scipy import signal
import glob, os


class Recognizer(object):
    def __init__(self, train=False):
        ## -----*----- コンストラクタ -----*-----##
        # ファイルパス
        self.format_path = './config/format.wav'
        self.model_path = './model/model_freq.hdf5'
        self.output_path = './tmp/separate.wav'

        # サンプリングレート
        self.rate = wf.read(self.format_path)[0]
        # スペクトログラムのサイズ
        self.size = self.__stft(file=self.format_path).shape

        # モデルのビルド
        self.__model = self.__build()

        if train:
            # 学習
            x, y = self.__features_extracter()
            self.__train(x, y)
        else:
            # モデルの読み込み
            self.load_model(self.model_path)

    def __build(self):
        ## -----*----- NNを構築 -----*-----##
        model = Sequential()
        model.add(LSTM(units=128, input_shape=(self.size[0], 1)))
        model.add(Dropout(0.3))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(self.size[0], activation='sigmoid'))
        # コンパイル
        model.compile(optimizer='rmsprop',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])

        return model

    def __train(self, x, y):
        ## -----*----- 学習 -----*-----##
        self.__model.fit(x, y, epochs=20, batch_size=30)
        # 学習モデルを保存
        self.__model.save_weights(self.model_path)

    def __features_extracter(self):
        ## -----*----- 特徴量を抽出 -----*----- ##
        x = []
        y = []
        spec = []

        # ===== スペクトログラム一覧を格納 ===============
        for speaker in glob.glob('./tmp/teach/*'):
            files = glob.glob('./tmp/teach/{0}/*.wav'.format(speaker.split('/')[-1]))
            # 話者インデックス
            spec.append([])

            for f in files:
                # スペクトログラム
                spec[-1].append(self.__stft(file=f).T)

        # 教師データ数
        num = min([len(arr) for arr in spec])

        for i in range(num):
            for t in range(self.size[1]):
                # 時間毎に区切る
                x.append(spec[0][i][t] + spec[1][i][t])

                # 周波数成分を話者に分類
                y.append(np.zeros(self.size[0]))
                for j in range(self.size[0]):
                    if spec[0][i][t][j] > spec[1][i][t][j]:
                        y[-1][j] = 1

        x = np.array(x).reshape((len(x), self.size[0], 1))
        y = np.array(y)
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
            self.__model.load_weights(path)

    def predict(self, data):
        ## -----*----- 推論 -----*-----##
        data = np.reshape(data, (self.size[0], 1))
        return self.__model.predict(np.array([data]))[0]

    def separate(self, file):
        ## -----*----- 音源分離 -----*-----##
        spec = self.__stft(file=file, to_log=False).T
        for t in range(self.size[1]):
            # 推論
            pred = self.predict(spec[t])

            # 分類
            for i in range(self.size[0]):
                if pred[i] < 0.5:
                    spec[t][i] = 0

        wav = self.__istft(spec.T)
        wf.write(self.output_path, self.rate, wav)


if __name__ == '__main__':
    infer = Recognizer()
    infer.separate('./tmp/mixed.wav')
    #infer.separate(glob.glob('./tmp/teach/800Hz/*.wav')[0])
    #infer.separate(glob.glob('./tmp/teach/あー/*.wav')[0])
