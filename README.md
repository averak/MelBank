MelBank
=======

Sound separation of multiple speakers on a single channel.


## Description

Enables not only noise-speech separation but also speech-speech separation.


## Requirement

- macOS Catalina  10.15.2
- Python 3.7.4
- TensorFlow 2.0.0


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