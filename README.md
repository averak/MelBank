MelBank
=======

Sound separation of multiple speakers on a single channel.


## Description

Enables not only noise-speech separation but also speech-speech separation.


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
