# MelBank

[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

This project objective is to separate the sound of multiple speakers on a single channel.

It enables not only noise-speech separation, but also speech-speech separation.

## Demo

Cannot play demo audio in GitHub. If you want to listen to demo audio, look [this](demo).

## Requirement

- Python ~> 3.8
- TensorFlow

## Usage

1. Creating teacher data

```
$ make teach.record  # Recording each sound source to be separated
$ make teach.build
```

2. Training

```
$ make train
```

3. Sound source separation

```
$ make exec
```

## Installation

```
$ git clone <this repo>
$ cd <this repo>

$ pipenv install
```
