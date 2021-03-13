class FontColors:
    RED: str = '\033[31m'
    GREEN: str = '\033[32m'
    YELLOW: str = '\033[33m'
    RESET: str = '\033[0m'


def CREATED_DATA_MSG(n_data: int) -> str:
    result: str = 'Created %d data.' % n_data
    return result


def SOURCE_TYPE_INPUT_GEIDE(default_speaker_str: str) -> str:
    result: str = 'which source type? ' + \
        FontColors.GREEN + \
        default_speaker_str + \
        ' (speaker or noise)' + \
        FontColors.RESET + \
        ' : '
    return result
