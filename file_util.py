import os


def change_extension(file: str, new: str) -> str:
    """
    Change extension of file.
    :param file: file path to change extension.
    :param new: new file extension.
    :return: path of file with newly set extension.
    """

    return file.rsplit('.', 1)[0] + '.' + new


def get_relative_path(file_path: str, root_dir: str) -> str:
    if not file_path:
        return root_dir

    if file_path[0] == '.':
        return file_path.rstrip('/')

    if root_dir in file_path:
        return './' + file_path.split(root_dir, 1)[-1].strip(' /')

    file_path = file_path.strip('/')
    root_dir = root_dir.strip('/')

    file_path_tokens = file_path.split('/')
    root_dir_tokens = root_dir.split('/')

    i = 0
    maximum = min(len(file_path_tokens), len(root_dir_tokens))
    while i < maximum:
        if file_path_tokens[i] != root_dir_tokens[i]:
            break
        i += 1

    relative_path = '../' * (len(root_dir_tokens) - i)
    relative_path += '/'.join(file_path_tokens[i:])

    return relative_path.rstrip('/')


def create_directory(path: str) -> bool:
    """
    Creates a directory at a given path. If path already exist, just ignore.
    :param path: path to create directory.
    :return: True if directory created, otherwise false, if directory already exists.
    """

    try:
        os.mkdir(path)
        return True
    except FileExistsError:
        return True
    except Exception:
        return False


def remove_files(files: list) -> None:
    """
    Removes given set of files.
    :param files: files to remove.
    :return: None.
    """

    for file in files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
