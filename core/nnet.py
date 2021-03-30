import os
from tensorflow.keras import layers
from tensorflow.keras import Sequential
import numpy as np

from core import config


class NNet:
    def __init__(self, load_weights: bool = True):
        self.nnet: Sequential = self.make_nnet(load_weights)

    def make_nnet(self, load_weights: bool) -> Sequential:
        result: Sequential = Sequential()
        result.add(layers.Input(shape=config.INPUT_SHAPE))

        # convolution 1st layer
        result.add(layers.Conv2D(32, (3, 3), padding='same'))
        result.add(layers.BatchNormalization())
        result.add(layers.Activation('relu'))
        result.add(layers.MaxPool2D())
        result.add(layers.Dropout(config.DROPOUT_RATE))

        # convolution 2st layer
        result.add(layers.Conv2D(32, (3, 3), padding='same'))
        result.add(layers.BatchNormalization())
        result.add(layers.Activation('relu'))
        result.add(layers.MaxPool2D())
        result.add(layers.Dropout(config.DROPOUT_RATE))

        # fully connected 1st layer
        result.add(layers.Flatten())
        result.add(layers.Dense(32, use_bias=False))
        result.add(layers.BatchNormalization())
        result.add(layers.Activation('relu'))
        result.add(layers.Dropout(config.DROPOUT_RATE))

        # fully connected final layer
        result.add(layers.Dense(1))
        result.add(layers.Activation('sigmoid'))

        # result.summary()

        # make & compile
        result.compile(
            optimizer=config.OPTIMIZER,
            loss=config.LOSS,
            metrics=config.METRICS,
        )

        # load trained weights
        if load_weights and os.path.exists(config.MODEL_PATH):
            result.load_weights(config.MODEL_PATH)

        return result

    def train(self, x: np.ndarray, y: np.ndarray) -> None:
        for step in range(config.EPOCHS):
            self.nnet.fit(
                x,
                y,
                initial_epoch=step,
                epochs=step + 1,
                batch_size=config.BATCH_SIZE,
                validation_split=config.VALIDATION_SPLIT,
            )

            # save checkpoint
            self.nnet.save_weights('%s/%d.h5' % (config.MODEL_ROOT_PATH, step))

        # save final weights
        self.nnet.save_weights(config.MODEL_PATH)

    def predict(self, feature: np.ndarray) -> int:
        result: int = np.argmax(self.nnet.predict(np.array([feature]))[0])
        return result

    def evaluate(self, x: np.ndarray, y: np.ndarray) -> float:
        result: float = self.nnet.evaluate(x, y)[1]
        return result
