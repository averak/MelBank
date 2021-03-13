#!/usr/bin/env python
import argparse


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
        pass
    if args.build:
        pass
    if args.demo:
        pass
    else:
        parser.print_help()
