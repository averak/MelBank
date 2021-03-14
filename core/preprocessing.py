import numpy as np
import scipy.io.wavfile as wf
from scipy import signal

from core import config


# output spectrogram
def exec(file_name: str) -> np.ndarray:
    wav: np.ndarray = wf.read(file_name)[1]
    spec: np.ndarray = stft(wav, True)

    result: np.ndarray = np.empty((0, config.DATA_SAMPLES))

    for frame in spec:
        # preprocessing
        frame = normalize(frame)
        frame = filter(frame)

        result = np.vstack([result, frame])

    return result


# convert wave -> spectrogram
def stft(wav: np.ndarray, to_log: bool) -> np.ndarray:
    result: np.ndarray = signal.stft(wav, fs=config.WAVE_RATE)[2]

    # convert to log scale
    if to_log:
        result = np.where(result == 0, 0.1 ** 10, result)
        result = 10 * np.log10(np.abs(result))

    # time <-> freq
    result = result.T

    return result


# convert spectrogram -> wave
def istft(spec: np.ndarray) -> np.ndarray:
    result: np.ndarray = signal.istft(spec.T, fs=config.WAVE_RATE)[1]
    return result


# normalize to 0~1
def normalize(data: np.ndarray) -> np.ndarray:
    n_min: int = data.min(keepdims=True)
    n_max: int = data.max(keepdims=True)

    result: np.ndarray = None

    if (n_max - n_min) == 0:
        result = data
    else:
        result = (data - n_min) / (n_max - n_min)

    return result


# band-pass filter
def filter(data: np.ndarray) -> np.ndarray:
    # edge freq [Hz]
    low_edge = 100
    high_edge = 8000

    delte = (config.WAVE_RATE / 2) / config.DATA_SAMPLES
    bpf: np.ndarray = np.zeros(config.DATA_SAMPLES)

    for i in range(config.DATA_SAMPLES):
        freq: float = i * delte
        if freq > low_edge and freq < high_edge:
            bpf[i] = 1

    return data * bpf
