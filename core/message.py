class FontColors:
    RED: str = '\033[31m'
    GREEN: str = '\033[32m'
    YELLOW: str = '\033[33m'
    RESET: str = '\033[0m'


ERROR_INVALID_SOURCE_NAME: str = FontColors.RED + \
    'Cannot find such source name. Try again.' + FontColors.RESET


HOWTO_RECORDING_MSG: str = 'Press enter to start recording.' + \
    '\n' + \
    'Enter the <q> key to quit.'


def CREATED_FILE_MSG(file_name: str) -> str:
    result: str = 'Created ' + file_name + ' .'
    return result


def DELETE_FILE_MSG(file_name: str) -> str:
    result: str = 'Deleted ' + file_name + ' .'
    return result


def CREATED_DATA_MSG(n_data: int) -> str:
    result: str = 'Created %d data.' % n_data
    return result


def RECORDING_VOICE_MSG(index: int) -> str:
    result: str = 'Recording %d...' % index
    return result


def SOURCE_INPUT_GUIDE(default_source_str: str) -> str:
    result: str = 'which source type? ' + \
        FontColors.GREEN + \
        default_source_str + \
        ' (speaker or noise)' + \
        FontColors.RESET + \
        ' : '
    return result
