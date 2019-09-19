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
    def __init__(self, train=False):
        ## -----*----- コンストラクタ -----*-----##
        # サンプリングレート
        self.rate = wf.read('./config/format.wav')[0]
        self.model_path = './model/model.hdf5'

        # モデルのビルド
        self.__model = self.__build()

        x, y = self.__features_extracter()

        if train:
            self.__train(x, y)

        # モデルの読み込み
        self.load_model(self.model_path)

    def __build(self):
        ## -----*----- NNを構築 -----*-----##
        model = Sequential()
        # model.add(LSTM(units=128, input_shape=(129, 33)))
        model.add(LSTM(units=128, input_shape=(129 * 33, 1)))
        model.add(Dropout(0.3))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(129 * 33, activation='sigmoid'))
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
                spec[-1].append(self.__stft(file=f))

        # 教師データ数
        num = min([len(arr) for arr in spec])

        for i in range(num):
            x.append(None)
            for speaker in spec:
                if x[i] is None:
                    x[i] = speaker[i]
                else:
                    x[i] += speaker[i]

            y.append(np.arange(x[i].shape[0] * x[i].shape[1]).reshape(x[i].shape[0], x[i].shape[1]))
            for j in range(x[i].shape[0]):
                for k in range(x[i].shape[1]):
                    max = {'index': 0, 'value': 0.0}
                    for speaker in range(len(spec)):
                        if spec[speaker][i][j][k] >= max['value']:
                            max['index'] = speaker
                            max['value'] = spec[speaker][i][j][k]
                    y[i][j][k] = max['index']

            x[i] = np.array(x[i]).flatten().reshape((129 * 33, 1))
            y[i] = np.array(y[i]).flatten()

        x = np.array(x)
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

    def predict(self, spec):
        ## -----*----- 推論 -----*-----##
        return self.__model.predict(np.array([spec]))[0].reshape((129, 33))

    def separate(self, file):
        ## -----*----- 音源分離 -----*-----##
        spec = self.__stft(file=file, to_log=False)
        pred = self.predict(spec)

        for i in range(129):
            for j in range(33):
                if float(pred[i][j]) > 0.001:
                    print(100)
                    spec[i][j] = 0

        wav = self.__istft(spec)
        wf.write('./tmp/separate.wav', 8000, wav)


if __name__ == '__main__':
    infer = Infer()
    infer.separate('./tmp/mixed.wav')
