# data path
DATA_ROOT_PATH: str = '../data'
TEACHER_ROOT_PATH: str = DATA_ROOT_PATH + '/teacher'
RECORD_ROOT_PATH: str = DATA_ROOT_PATH + '/record'
SPEAKER_ROOT_PATH: str = RECORD_ROOT_PATH + '/speaker'
NOISE_ROOT_PATH: str = RECORD_ROOT_PATH + '/noise'
MODEL_ROOT_PATH: str = '../ckpt'
MODEL_PATH: str = MODEL_ROOT_PATH + '/final.h5'
RECORD_WAV_PATH: str = '../record.wav'
CLEANED_WAV_PATH: str = '../cleaned.wav'

# wave config
WAVE_RATE: int = 16000
WAVE_BIT: int = 16
WAVE_SPLIT_INTERVAL: float = 1.0
DATA_SAMPLES: int = 641

# training params
EPOCHS: int = 50
OPTIMIZER: str = 'adam'
LOSS: str = 'binary_crossentropy'
INPUT_SHAPE: list = (DATA_SAMPLES, 1)
