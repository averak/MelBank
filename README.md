MelBank
=======

Sound separation of multiple speakers on a single channel.


## Description

Enables not only noise-speech separation but also speech-speech separation.


## Requirement

- macOS Mojave 10.14.6
- Python 3.5.2
- TensorFlow 2.0.0a0


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
$ git clone https://github.com/Lab-info/MelBank
$ cd MelBank
$ sh setup.sh
```