from pathlib import Path
import os


def index(directory: str) -> list:
    """
    Index all files from directory (including all subdirectories).
    :param directory: directory to index.
    :return: list containing all files found into given directory.
    """

    path = Path(directory)
    return [p for p in path.expanduser().iterdir()]


def get_directories(files: list, ignore_paths: list) -> list:
    """
    Get all directories from a given list of files.
    :param files: set of files to get directories.
    :param ignore_paths: set of paths to be ignored.
    :return: set of all directories from given paths.
    """

    files = [Path(paths) for paths in files]
    ignore_paths = [Path(paths) for paths in ignore_paths]
    return [file for file in files if file.is_dir() and file not in ignore_paths]


def is_source_file(file_path: str, extensions: list) -> bool:
    """
    Check if given path represents source file (based by extensions provided by user).
    :param file_path: file path to check.
    :param extensions: list of possible extensions for source files.
    :return: true, if given path is source file, otherwise returns false.
    """

    path = Path(file_path)
    return path.is_file() and path.suffix[1:] in extensions and len(path.suffixes) == 1


def is_d_file(file_path: str) -> bool:
    """
    Check if given path represents a .d file.
    :param file_path: path to check.
    :return: true, if given path is .d file, otherwise false.
    """

    path = Path(file_path)
    return path.is_file() and path.suffix == '.d' and len(path.suffixes) == 1


def get_d_files(files: list) -> list:
    """
    Get all .d files from given set of paths.
    :param files: paths to check.
    :return: set containing all .d files from given set files.
    """
    return [file for file in files if is_d_file(file)]


def get_source_files(files: list, extensions: list, ignore_paths: list) -> list:
    """
    Get all source files from a given list of files paths.
    :param files: files paths to check.
    :param extensions: list of all possible extensions for source files.
    :param ignore_paths: list of all files to be ignored.
    :return: set containing all source files from given paths.
    """

    return [file for file in files if is_source_file(file, extensions) and file not in ignore_paths]
