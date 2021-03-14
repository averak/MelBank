#!/usr/bin/env python
import os
import glob
import argparse
import numpy as np

from core import config
from core import message
from core import nnet
from core import preprocessing
from core import record
from core import util
from core import vocode


recorder: record.Record = record.Record()
vocoder: vocode.Vocode = vocode.Vocode()
nnet_: nnet.NNet = nnet.NNet()


def train_mode():
    # FIXME
    nnet_.train([], [])


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
        recorder.exit()
        exit(1)

    # mkdir & count number of exists files
    util.mkdir(save_root_path)
    save_index: int = util.get_number_of_files(save_root_path, 'wav')

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


def build_mode():
    # FIXME
    return


def demo_mode():
    wav: np.array = vocoder.exec(config.RECORD_WAV_PATH)
    vocoder.save(wav, config.CLEANED_WAV_PATH)


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

    recorder.exit()
