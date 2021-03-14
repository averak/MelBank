# data path
DATA_ROOT_PATH: str = './data'
TEACHER_ROOT_PATH: str = DATA_ROOT_PATH + '/teacher'
TEACHER_X_PATH: str = TEACHER_ROOT_PATH + '/x.npy'
TEACHER_Y_PATH: str = TEACHER_ROOT_PATH + '/y.npy'
RECORD_ROOT_PATH: str = DATA_ROOT_PATH + '/record'
SPEAKER_ROOT_PATH: str = RECORD_ROOT_PATH + '/speaker'
NOISE_ROOT_PATH: str = RECORD_ROOT_PATH + '/noise'
MODEL_ROOT_PATH: str = './ckpt'
MODEL_PATH: str = MODEL_ROOT_PATH + '/final.h5'
RECORD_WAV_PATH: str = DATA_ROOT_PATH + '/record.wav'
CLEANED_WAV_PATH: str = DATA_ROOT_PATH + '/cleaned.wav'

# wave config
WAVE_RATE: int = 16000
WAVE_SPLIT_INTERVAL: float = 1.0
WAVE_CHANNELS: int = 1
WAVE_CHUNK: int = 2048
DATA_SAMPLES: int = 129

# training params
EPOCHS: int = 50
BATCH_SIZE: int = 32
VALIDATION_SPLIT: float = 0.1
OPTIMIZER: str = 'adam'
LOSS: str = 'binary_crossentropy'
METRICS: list = ['accuracy']
INPUT_SHAPE: list = (DATA_SAMPLES, 1)
