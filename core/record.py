import threading
import wave
import pyaudio

from core import config


class Record:
    def __init__(self):
        self.pa: pyaudio.PyAudio = pyaudio.PyAudio()
        self.stream: pyaudio.Stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=config.WAVE_CHANNELS,
            rate=config.WAVE_RATE,
            input=True,
            output=False,
            frames_per_buffer=config.WAVE_CHUNK,
        )

        self.wave: list = []

        self.is_recording: bool = False
        self.is_exit: bool = False

        # recording in sub-thread
        self.thread: threading.Thread = threading.Thread(target=self.recording)
        self.thread.start()

    def recording(self) -> None:
        while not self.is_exit:
            # start recording
            if self.is_recording:
                self.wave.append(self.input_audio())

            # stop recording
            else:
                pass

        # close pyaudio
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()

    def input_audio(self) -> bytes:
        return self.stream.read(config.WAVE_CHUNK, exception_on_overflow=False)

    def save(self, file_name: str) -> None:
        wf = wave.open(file_name, 'wb')
        wf.setnchannels(config.WAVE_CHANNELS)
        wf.setsampwidth(self.pa.get_sample_size(pyaudio.paInt16))
        wf.setframerate(config.WAVE_RATE)
        wf.writeframes(b''.join(self.wave))
        wf.close()

        self.wave = []

    def start(self) -> None:
        self.is_recording = True

    def stop(self) -> None:
        self.is_recording = False

    def exit(self) -> None:
        self.is_exit = True
