#!/usr/bin/env python
import os
import sys
import glob
import tqdm
import random
import shutil
import argparse
import numpy as np

from core import config
from core import message
from core import util


def train_mode():
    from core import nnet
    from sklearn.model_selection import train_test_split

    x: np.ndarray = np.load(config.TEACHER_X_PATH)
    y: np.ndarray = np.load(config.TEACHER_Y_PATH)

    # split data for training & validation
    x_train, x_val, y_train, y_val = train_test_split(x, y, train_size=0.8)

    nnet_: nnet.NNet = nnet.NNet(False)
    nnet_.train(x_train, y_train)
    print(message.ACCURACY_MSG(nnet_.evaluate(x_val, y_val)))


def record_mode():
    from core import record

    default_source: str = 'speech'
    input_str: str = input(message.SOURCE_INPUT_GUIDE(default_source)) \
        or default_source

    # set save path
    save_root_path: str = ''
    if input_str == 'speech':
        save_root_path = config.SPEECH_ROOT_PATH
    elif input_str == 'noise':
        save_root_path = config.NOISE_ROOT_PATH
    else:
        print(message.ERROR_INVALID_SOURCE_NAME)
        sys.exit(1)

    # mkdir & count number of exists files
    util.mkdir(save_root_path)
    save_index: int = util.get_number_of_files(save_root_path, 'wav')

    recorder: record.Record = record.Record()
    start_recording: bool = True

    print(message.RECORDING_HELP_MSG)
    while True:
        try:
            if input() == 'q':
                break

            if start_recording:
                recorder.start()
                print(message.RECORDING_VOICE_MSG(save_index), end='')
            else:
                recorder.stop()

                # <save_root_path>/<save_index>.wav
                file_name: str = '%s/%d.wav' % (save_root_path, save_index)
                recorder.save(file_name)
                print(message.CREATED_FILE_MSG(file_name))
                save_index += 1

            start_recording = not start_recording

        except KeyboardInterrupt:
            break

    print(message.CREATED_DATA_MSG(save_index))
    recorder.exit()


def build_mode():
    from core import preprocessing

    # teacher data(x: freq, y: freq-masks)
    x: list = []
    y: list = []

    # speech data
    print(message.PROCESSING_SOURCE_MSG('speech'))
    speech_files: list = glob.glob(config.SPEECH_ROOT_PATH + '/*.wav')
    speech_samples: list = []
    for file in tqdm.tqdm(speech_files):
        speech_samples.extend(preprocessing.extract_feature(file))

    # noise data
    print(message.PROCESSING_SOURCE_MSG('noise'))
    noise_files: list = glob.glob(config.NOISE_ROOT_PATH + '/*.wav')
    noise_samples: list = []
    for file in tqdm.tqdm(noise_files):
        noise_samples.extend(preprocessing.extract_feature(file, False))

    # mixing
    print(message.MIXING_DATA_MSG(len(speech_samples) + len(noise_samples)))
    for speech_frame in tqdm.tqdm(speech_samples):
        for noise_frame in random.choices(noise_samples, k=config.N_MIXED_NOISES):
            sn_rate: float = np.random.rand()
            noise_frame *= sn_rate
            mixed_frame = speech_frame + noise_frame

            freq_mask = np.zeros(config.FREQ_LENGTH)
            for fi in range(config.FREQ_LENGTH):
                if speech_frame[fi] > noise_frame[fi]:
                    freq_mask[fi] = 1

            x.append(mixed_frame)
            y.append(freq_mask)

    # save teacher data
    np.save(config.TEACHER_X_PATH, np.array(x))
    np.save(config.TEACHER_Y_PATH, np.array(y))


def demo_mode():
    from core import demo

    demo_: demo.Demo = demo.Demo()
    demo_.exec()


def clear_mode():
    data_dirs: list = [
        config.SPEECH_ROOT_PATH,
        config.NOISE_ROOT_PATH,
        config.MODEL_ROOT_PATH,
    ]

    for dir_name in data_dirs:
        files: list = glob.glob(dir_name + '/*')

        for file_name in files:
            if os.path.isfile(file_name):
                os.remove(file_name)
            else:
                shutil.rmtree(file_name)

            print(message.DELETE_FILE_MSG(file_name))


if __name__ == '__main__':
    # options
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train',
                        help='training with data you prepared',
                        action='store_true')
    parser.add_argument('-r', '--record',
                        help='voice recording audio for training',
                        action='store_true')
    parser.add_argument('-b', '--build',
                        help='build data for training',
                        action='store_true')
    parser.add_argument('-d', '--demo',
                        help='start demo',
                        action='store_true')
    parser.add_argument('-c', '--clear',
                        help='clear data',
                        action='store_true')
    args = parser.parse_args()

    if args.train:
        train_mode()
    if args.record:
        record_mode()
    if args.build:
        build_mode()
    if args.demo:
        demo_mode()
    if args.clear:
        clear_mode()
