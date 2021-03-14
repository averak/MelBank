#!/usr/bin/env python
import os
import glob
import tqdm
import argparse
import numpy as np

from core import config
from core import message
from core import nnet
from core import preprocessing
from core import record
from core import util
from core import vocode


def train_mode():
    x: np.ndarray = np.load(config.TEACHER_X_PATH)
    y: np.ndarray = np.load(config.TEACHER_Y_PATH)

    nnet_: nnet.NNet = nnet.NNet(False)
    nnet_.train(x, y)


def record_mode():
    default_source: str = 'speaker'
    input_str: str = input(message.SOURCE_INPUT_GUIDE(default_source)) \
        or default_source

    # set save path
    save_root_path: str = ''
    if input_str == 'speaker':
        save_root_path = config.SPEAKER_ROOT_PATH
    elif input_str == 'noise':
        save_root_path = config.NOISE_ROOT_PATH
    else:
        print(message.ERROR_INVALID_SOURCE_NAME)
        exit(1)

    # mkdir & count number of exists files
    util.mkdir(save_root_path)
    save_index: int = util.get_number_of_files(save_root_path, 'wav')

    recorder: record.Record = record.Record()
    start_recording: bool = True

    print(message.RECORDING_HELP_MSG)
    while input() != 'q':
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

    print(message.CREATED_DATA_MSG(save_index))
    recorder.exit()


def build_mode():
    # teacher data(x: frames, y: freq-masks)
    x: list = []
    y: list = []

    speaker_files: list = glob.glob(config.SPEAKER_ROOT_PATH + '/*.wav')
    noise_files: list = glob.glob(config.NOISE_ROOT_PATH + '/*.wav')

    # convert to spectrogram
    print(message.PROCESSING_SOURCE_MSG('speaker'))
    speaker_specs: list = []
    for file in tqdm.tqdm(speaker_files):
        speaker_specs.extend(preprocessing.exec(file))

    print(message.PROCESSING_SOURCE_MSG('noise'))
    noise_specs: list = []
    for file in tqdm.tqdm(noise_files):
        noise_specs.extend(preprocessing.exec(file))

    n_samples = max([len(speaker_specs), len(noise_specs)])

    # make teacher data
    print(message.MIXING_DATA_MSG(n_samples))
    for i in range(n_samples):
        speaker_spec: np.ndarray = speaker_specs[i % len(speaker_specs)]
        noise_spec: np.ndarray = noise_specs[i % len(noise_specs)]
        mixed_frame = speaker_spec + noise_spec
        x.append(mixed_frame)

        freq_mask = np.zeros(config.DATA_SAMPLES)
        for f in range(config.DATA_SAMPLES):
            if speaker_spec[f] > noise_spec[f]:
                freq_mask[f] = 1
        y.append(freq_mask)

    # save teacher data
    np.save(config.TEACHER_X_PATH, np.array(x))
    np.save(config.TEACHER_Y_PATH, np.array(y))


def demo_mode():
    vocoder: vocode.Vocode = vocode.Vocode()
    wav: np.array = vocoder.exec(config.RECORD_WAV_PATH)
    vocoder.save(wav, config.CLEANED_WAV_PATH)
    print(message.CREATED_FILE_MSG(config.CLEANED_WAV_PATH))


def clear_mode():
    data_dirs: list = [
        config.SPEAKER_ROOT_PATH,
        config.NOISE_ROOT_PATH,
    ]

    for dir_name in data_dirs:
        files: list = glob.glob(dir_name + '/*.wav')

        for file_name in files:
            os.remove(file_name)
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
