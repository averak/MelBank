# MelBank

[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

This project objective is to separate the sound of multiple speakers on a single channel.

It enables not only noise-speech separation, but also speech-speech separation.

## Demo

Cannot play demo audio in GitHub. If you want to listen to demo audio, look [this](demo).

## Requirement

- Python ~> 3.8
- TensorFlow

## Installation

```
$ git clone <this repo>
$ cd <this repo>

$ pipenv install
```

## Usage

### 1. Create teacher data

```
$ pipenv run record # Recording each sound source to be separated
$ pipenv run build  # Build teacher data
```

### 2. Training

```
$ pipenv run train
```

### 3. Start demo!

```
$ pipenv run demo
```

If you want to know the details of how to use this, run the following command.

```sh
$ pipenv run help
```
