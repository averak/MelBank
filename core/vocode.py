import tqdm
import numpy as np
import scipy.io.wavfile as wf

from core import config
from core import nnet
from core import preprocessing


class Vocode:
    def __init__(self):
        self.nnet: nnet.NNet = nnet.NNet()

    def exec(self, file_name: str, display_progress: bool = False) -> np.ndarray:
        """ vocode separated wave """

        # original spectrogram
        spec: np.ndarray = preprocessing.extract_feature(file_name, True, False, False, False)
        # preprocessed spectrogram
        spec_prep: np.ndarray = preprocessing.extract_feature(file_name, True, False)

        # time-freq masking
        loop_frames = tqdm.tqdm(spec_prep) if display_progress else spec_prep
        for t, frame in enumerate(loop_frames):
            freq_mask: np.ndarray = self.nnet.predict(frame)
            spec[t] = self.masking(spec[t], freq_mask)

        result: np.ndarray = preprocessing.istft(spec)
        return result

    def masking(self, frame: np.ndarray, freq_mask: np.ndarray) -> np.ndarray:
        freq_mask = np.where(freq_mask < np.median(freq_mask) - 0.1, 0, 1)
        freq_mask = np.reshape(freq_mask, frame.shape)
        return frame * freq_mask

    def save(self, wav: np.ndarray, file_name: str) -> None:
        wav = wav.flatten()
        wav = wav.astype(np.int16)
        wf.write(file_name, config.WAVE_RATE, wav)
