import os
import glob


def get_number_of_files(dir_name: str, extension: str = None) -> int:
    glob_pattern: str = dir_name + '/*'
    if extension is not None:
        glob_pattern += '.' + extension
    files = glob.glob(glob_pattern)
    return len(files)


def mkdir(dir_name: str) -> None:
    os.makedirs(dir_name, exist_ok=True)
