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
        self.model_path = './model/model_wave.hdf5'

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
        model.add(LSTM(units=128, input_shape=(4096, 1)))
        model.add(Dropout(0.3))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.3))
        # model.add(Dense(4096, activation='linear'))
        model.add(Dense(4096))
        # コンパイル
        model.compile(  # optimizer='adam',
            optimizer='rmsprop',
            loss='binary_crossentropy',
            # loss='mean_squared_error',
            metrics=['accuracy'],
            # loss='mse',
            # metrics=['mae']
        )

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
        wav = []

        # ===== 音声一覧を格納 ===============
        for speaker in glob.glob('./tmp/teach/*'):
            files = glob.glob('./tmp/teach/{0}/*.wav'.format(speaker.split('/')[-1]))
            # 話者インデックス
            wav.append([])

            for f in files:
                # 音源
                wav[-1].append(wf.read(f)[1])

        # 教師データ数
        num = min([len(arr) for arr in wav])

        for i in range(num):
            x.append(None)
            for speaker in wav:
                if x[i] is None:
                    x[i] = np.array(speaker[i])
                else:
                    x[i] += speaker[i]

            y.append(np.arange(x[i].shape[0]))
            for j in range(x[i].shape[0]):
                max = {'index': 0, 'value': 0.0}
                for speaker in range(len(wav)):
                    if wav[speaker][i][j] >= max['value']:
                        max['index'] = speaker
                        max['value'] = wav[speaker][i][j]
                y[i][j] = max['index']

            x[i] = np.array(x[i]).flatten().reshape((x[i].shape[0], 1))
            y[i] = np.array(y[i]).flatten()

        x = np.array(x)
        y = np.array(y)
        return x, y

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
        spec = spec.flatten().reshape((4096, 1))
        return self.__model.predict(np.array([spec]))[0].reshape((4096))

    def separate(self, file):
        ## -----*----- 音源分離 -----*-----##
        wav = np.array(wf.read(file)[1])
        pred = self.predict(wav)

        for i in range(4096):
            #print(pred[i])
            if pred[i] > 0.2:
                wav[i] = 0

        wf.write('./tmp/separate.wav', 8000, wav)


if __name__ == '__main__':
    infer = Infer()
    infer.separate('./tmp/mixed.wav')
    # infer.separate(glob.glob('./tmp/teach/800Hz/*.wav')[0])
    # infer.separate(glob.glob('./tmp/teach/あー/*.wav')[0])
