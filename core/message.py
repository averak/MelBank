class FontColors:
    RED: str = '\033[31m'
    GREEN: str = '\033[32m'
    YELLOW: str = '\033[33m'
    RESET: str = '\033[0m'


ERROR_INVALID_SOURCE_NAME: str = FontColors.RED + \
    'Cannot find such source name. Try again.' + FontColors.RESET


RECORDING_HELP_MSG: str = 'Press enter to start recording.' + \
    '\n' + \
    'Enter the <q> key to quit.'


def CREATED_FILE_MSG(file_name: str) -> str:
    result: str = 'Created ' + FontColors.YELLOW + file_name + FontColors.RESET
    return result


def DELETE_FILE_MSG(file_name: str) -> str:
    result: str = 'Deleted ' + FontColors.YELLOW + file_name + FontColors.RESET
    return result


def VOCODE_COMPLETE_MSG(file_name: str) -> str:
    result: str = 'Vocodede ' + \
        FontColors.YELLOW + \
        file_name + \
        FontColors.RESET
    return result


def CREATED_DATA_MSG(n_data: int) -> str:
    result: str = 'Created %d data' % n_data
    return result


def RECORDING_VOICE_MSG(index: int) -> str:
    result: str = 'Recording %d...' % index
    return result


def PROCESSING_SOURCE_MSG(source_str: str) -> str:
    result: str = 'Processing %s data...' % source_str
    return result


def MIXING_DATA_MSG(n_data: int) -> str:
    result = 'Mixing %d samples...' % n_data
    return result


def SOURCE_INPUT_GUIDE(default_source_str: str) -> str:
    result: str = 'which source type? ' + \
        FontColors.GREEN + \
        default_source_str + \
        ' (speaker or noise)' + \
        FontColors.RESET + \
        ' : '
    return result
