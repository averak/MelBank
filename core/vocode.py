import numpy as np
import scipy.io.wavfile as wf

from core import config
from core import nnet
from core import preprocessing


class Vocode:
    def __init__(self):
        self.nnet: nnet.NNet = nnet.NNet()

    def exec(self, file_name: str) -> np.ndarray:
        """ vocode separated wave """

        wav: np.ndarray = wf.read(file_name)[1]
        # original spectrogram
        spec: np.ndarray = preprocessing.stft(wav, False)
        # preprocessed spectrogram
        spec_prep: np.ndarray = preprocessing.extract_feature(file_name)

        # time-freq masking
        for t, frame in enumerate(spec_prep):
            freq_mask: np.ndarray = self.nnet.predict(frame)
            spec[t] *= self.masking(spec[t], freq_mask)
            spec[t] = preprocessing.filter(spec[t])

        result: np.ndarray = preprocessing.istft(spec)
        return result

    def masking(self, frame: np.ndarray, freq_mask: np.ndarray) -> np.ndarray:
        return frame * freq_mask

    def save(self, wav: np.ndarray, file_name: str) -> None:
        wav = wav.astype(np.int16)
        wf.write(file_name, config.WAVE_RATE, wav)
