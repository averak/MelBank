#!/usr/bin/env python
import argparse

from core import config
from core import record
from core import preprocessing

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
    args = parser.parse_args()

    if args.train:
        pass

    if args.record:
        import time

        rec: record.Record = record.Record()
        print('start')
        rec.start()
        time.sleep(1.5)
        print('stop')
        rec.stop()
        rec.exit()

    if args.build:
        preprocessing.exec(config.RECORD_WAV_PATH)

    if args.demo:
        pass
