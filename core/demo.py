import os
import time
import threading
import pyaudio
import numpy as np
import anal

from core import config
from core import preprocessing
from core import record
from core import vocode


class AudioStateInfo:
    def __init__(self):
        self.n_up_edge: int = 0
        self.n_down_edge: int = 0
        self.current_vol: float = 0
        self.total_vol: float = 0
        self.average_vol: float = 0
        self.border: float = 9999
        self.n_sample: int = 0


class Demo:
    def __init__(self):
        self.recorder: record.Record = record.Record()

        self.stream: pyaudio.Stream = self.recorder.pa.open(
            format=pyaudio.paFloat32,
            channels=config.WAVE_CHANNELS,
            rate=config.WAVE_RATE,
            input=True,
            output=False,
            frames_per_buffer=config.WAVE_CHUNK,
        )

        # vocoder
        self.vocoder: vocode.Vocode = vocode.Vocode()

        # analyzer in stdout
        self.anal: anal.Anal = anal.Anal('config/demo.txt.anal')

        # detection params
        self.audio_state: AudioStateInfo = AudioStateInfo()
        self.reset_state_interval: float = 0.3
        self.past_time: time.time

        self.is_recording: bool = False
        self.enable_detect: bool = True
        self.is_exit: bool = False

    def exec(self):
        # update border in sub-thread
        self.thread: threading.Thread = \
            threading.Thread(target=self.update_border)
        self.thread.start()

        self.past_time = time.time()

        while not self.is_exit:
            try:
                if time.time() - self.past_time > self.reset_state_interval:
                    self.reset_audio_state()

                self.audio_state.n_sample += 1
                self.detection()
                self.draw_field()

                if self.is_recording:
                    self.recorder.start()
                else:
                    self.recorder.stop()

                if not self.enable_detect:
                    self.recorder.save(config.RECORD_WAV_PATH)

                    # sound source separation
                    self.predict()
                    self.enable_detect = True
                    self.reset_audio_state()

            except KeyboardInterrupt:
                os.system('clear')
                self.is_exit = True
                break

        self.recorder.exit()

    def detection(self):
        wav = np.fromstring(self.stream.read(
            config.WAVE_CHUNK, exception_on_overflow=False), np.float32)
        wav *= np.hanning(config.WAVE_CHUNK)
        # amplitude spectrum
        amp_spec = np.fft.fft(wav)
        # power spectrum
        power_spec = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in amp_spec]
        power_spec = np.array(power_spec)
        # band-pass filter
        power_spec = preprocessing.filtering(power_spec)

        self.audio_state.current_vol = sum(power_spec)
        self.audio_state.total_vol += self.audio_state.current_vol
        self.audio_state.average_vol = \
            self.audio_state.total_vol / self.audio_state.n_sample

        # start/stop recording
        if self.enable_detect:
            if self.is_recording:
                if self.judge_down_edge():
                    self.audio_state.n_down_edge = 0
                    self.is_recording = False
                    self.enable_detect = False
            else:
                if self.judge_up_edge():
                    self.audio_state.n_up_edge = 0
                    self.is_recording = True
                    self.audio_state.border = self.audio_state.average_vol

    def judge_up_edge(self) -> bool:
        judge_border: int = int(config.WAVE_RATE / config.WAVE_CHUNK / 10)

        if self.audio_state.current_vol >= self.audio_state.border:
            self.audio_state.n_up_edge += 1

        return self.audio_state.n_up_edge > judge_border

    def judge_down_edge(self) -> bool:
        judge_border: int = int(config.WAVE_RATE / config.WAVE_CHUNK / 2)

        if self.audio_state.average_vol <= self.audio_state.border:
            self.audio_state.n_down_edge += 1

        return self.audio_state.n_down_edge > judge_border

    def reset_audio_state(self) -> None:
        self.audio_state.total_vol = \
            self.audio_state.average_vol * config.WAVE_AMP_SAMPLES
        self.audio_state.n_sample = config.WAVE_AMP_SAMPLES
        self.audio_state.n_up_edge = 0
        self.past_time = time.time()

    def draw_field(self) -> None:
        self.anal.draw(
            str(int(self.audio_state.average_vol)),
            str(int(self.audio_state.current_vol)),
            str(int(self.audio_state.border)),
            '\033[%dm録音中' % (32 if self.is_recording else 90),
            '\033[%dm分離中' % (32 if not self.enable_detect else 90),
            self.generate_meter(self.audio_state.average_vol, True),
            self.generate_meter(self.audio_state.current_vol, True),
            self.generate_meter(self.audio_state.border),
        )

    def update_border(self) -> None:
        while not self.is_exit:
            time.sleep(0.2)

            # update border only when not recording
            if not self.is_recording:
                self.audio_state.border = \
                    pow(10, 1.13) * pow(self.audio_state.average_vol, 0.72)

    def generate_meter(self, volume: float, to_green: bool = False) -> str:
        result: str = ''
        result = '■' * int(volume / 20.0 + 3.0)
        if to_green and \
                self.audio_state.current_vol >= self.audio_state.border:
            result = '\033[94m' + result

        return result

    def predict(self) -> None:
        wav: np.ndarray = self.vocoder.exec(config.RECORD_WAV_PATH)
        self.vocoder.save(wav, config.CLEANED_WAV_PATH)

        # FIXME: paly cleaned wav
        os.system('afplay %s' % config.CLEANED_WAV_PATH)


if __name__ == '__main__':
    demo = Demo()
    demo.exec()
