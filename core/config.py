# data path
DATA_ROOT_PATH: str = './data'
TEACHER_ROOT_PATH: str = DATA_ROOT_PATH + '/teacher'
TEACHER_X_PATH: str = TEACHER_ROOT_PATH + '/x.npy'
TEACHER_Y_PATH: str = TEACHER_ROOT_PATH + '/y.npy'
RECORD_ROOT_PATH: str = DATA_ROOT_PATH + '/record'
SPEECH_ROOT_PATH: str = RECORD_ROOT_PATH + '/speech'
NOISE_ROOT_PATH: str = RECORD_ROOT_PATH + '/noise'
RECORD_WAV_PATH: str = DATA_ROOT_PATH + '/record.wav'
CLEANED_WAV_PATH: str = DATA_ROOT_PATH + '/cleaned.wav'
MODEL_ROOT_PATH: str = './ckpt'
MODEL_PATH: str = MODEL_ROOT_PATH + '/final.h5'

# wave config
WAVE_RATE: int = 16000
WAVE_WIDTH: int = 2
WAVE_CHANNELS: int = 1
WAVE_CHUNK: int = 1024
WAVE_DEFECT_SEC: float = 0.4
WAVE_AMP_SAMPLES: int = 6
N_MIXED_NOISES: int = 50
FREQ_LENGTH: int = 129
INPUT_SHAPE: tuple = (FREQ_LENGTH, 1)

# wave preprocessing config
BPF_LOW_FREQ: int = 100
BPF_HIGH_FREQ: int = 8000
FFT_LENGTH: int = 512
MIN_SILENCE_LENGTH: int = 100
SILENCE_THRESH: int = -20
KEEP_SILENCE: int = 100

# training params
EPOCHS: int = 50
BATCH_SIZE: int = 32
VALIDATION_SPLIT: float = 0.1
DROPOUT_RATE: float = 0.5
OPTIMIZER: str = 'adam'
LOSS: str = 'binary_crossentropy'
METRICS: list = ['accuracy']
