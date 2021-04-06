import numpy as np
import sklearn.preprocessing
import pyroomacoustics as pra
import scipy.io.wavfile as wf
from scipy import signal
from pydub import AudioSegment
from pydub.silence import split_on_silence

from core import config


def extract_feature(file_name: str, do_noise_reduction: bool = True, do_remove_silence: bool = True, do_normalize: bool = True, to_log: bool = True) -> np.ndarray:
    """ extract preprocessed feature """

    # read wav file
    wav: np.ndarray = wf.read(file_name)[1]
    wav = wav.astype(np.float32)
    # cleaning wave
    if do_noise_reduction:
        wav = noise_reduction(wav)
    if do_remove_silence:
        wav = remove_silence(wav)
    # convert to spectrogram
    spec: np.ndarray = stft(wav, to_log)

    result: list = []
    for frame in spec:
        # if do_normalize:
        #     frame = normalize(frame)
        frame = filtering(frame)
        frame = np.reshape(frame, config.INPUT_SHAPE)
        result.append(frame)

    return np.array(result)


def stft(wav: np.ndarray, to_log: bool) -> np.ndarray:
    """ convert wave -> spectrogram """

    result: np.ndarray = signal.stft(wav, fs=config.WAVE_RATE)[2]

    # convert to log scale
    if to_log:
        result = np.where(result == 0, 0.1 ** 10, result)
        result = 10 * np.log10(np.abs(result))

    # time <-> freq
    result = result.T

    return result


def istft(spec: np.ndarray) -> np.ndarray:
    """ convert spectrogram -> wave """

    result: np.ndarray = signal.istft(spec.T, fs=config.WAVE_RATE)[1]
    return result


def normalize(feature: np.ndarray) -> np.ndarray:
    """ min-max normalization """

    result: np.ndarray = feature.flatten()
    result_shape: tuple = feature.shape

    result = sklearn.preprocessing.minmax_scale(result)
    result = np.reshape(result, result_shape)

    return result


def filtering(feature: np.ndarray) -> np.ndarray:
    """ band-pass filtering """

    n_sample: int = len(feature)
    delte = (config.WAVE_RATE / 2) / n_sample
    bpf: np.ndarray = np.zeros(n_sample)

    for i in range(n_sample):
        freq: float = i * delte
        if freq > config.BPF_LOW_FREQ and freq < config.BPF_HIGH_FREQ:
            bpf[i] = 1
    bpf = np.reshape(bpf, feature.shape)

    return feature * bpf


# spectral subtraction
def noise_reduction(feature: np.ndarray) -> np.ndarray:
    result: np.ndarray = pra.denoise.spectral_subtraction.apply_spectral_sub(
        feature, config.FFT_LENGTH)
    return result


# extract only voice activity
def remove_silence(feature: str) -> np.ndarray:
    sound: AudioSegment = AudioSegment(
        data=bytes(feature.astype(np.int16)),
        sample_width=config.WAVE_WIDTH,
        frame_rate=config.WAVE_RATE,
        channels=config.WAVE_CHANNELS
    )

    # extract only voice activity
    chunks: list = split_on_silence(
        sound,
        min_silence_len=config.MIN_SILENCE_LENGTH,
        silence_thresh=config.SILENCE_THRESH,
        keep_silence=config.KEEP_SILENCE,
    )

    # select the highest volume
    result: np.ndarray = feature
    for chunk in chunks:
        chunk_wav: list = chunk.get_array_of_samples()
        result = np.append(result, np.array(chunk_wav))

    result = result.astype(np.float32)
    return result
