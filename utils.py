#!/usr/bin/env python3

from pathlib import Path
import os
import re


TARGET = str()
CC = str()
RM = str()
C_FLAGS = set()
EXTENSIONS = list()
IGNORE_PATHS = set()
PROJECT_ROOT = str()
CLEAN = bool()


def index(directory: str) -> set:
    """
    Index all files from directory (including all subdirectories).
    :param directory: directory to index.
    :return: set containing all files found into given directory.
    """

    path = Path(directory)
    return set([str(p) for p in path.expanduser().iterdir()])


def get_directories(files: set, ignore_paths: set) -> set:
    """
    Get all directories from a given list of files.
    :param files: set of files to get directories.
    :param ignore_paths: paths to ignore.
    :return: set of all directories from given paths.
    """

    return set([file for file in files if os.path.isdir(file) and file not in ignore_paths])


def is_source_file(file_path: str) -> bool:
    """
    Check if given path represents source file (based by extensions provided by user).
    :param file_path: file path to check.
    :return: true, if given path is source file, otherwise returns false.
    """

    return os.path.isfile(file_path) and file_path.rsplit('.', maxsplit=1)[-1] in EXTENSIONS


def is_d_file(file_path: str) -> bool:
    """
    Check if given path represents a .d file.
    :param file_path: path to check.
    :return: true, if given path is .d file, otherwise false.
    """

    return os.path.isfile(file_path) and file_path.rsplit('.', maxsplit=1)[-1] == 'd'


def get_source_files(files: set, ignore_paths: set) -> set:
    """
    Get all source files from a given list of files paths.
    :param files: files paths to check.
    :param ignore_paths: paths to ignore.
    :return: set containing all source files from given paths.
    """

    # [print(file, is_source_file(file), file not in ignore_paths) for file in files]
    return set([file for file in files if is_source_file(file) and file not in ignore_paths])


def get_d_files(files: set) -> set:
    """
    Get all .d files from given set of paths.
    :param files: paths to check.
    :return: set containing all .d files from given set files.
    """
    return set([file for file in files if is_d_file(file)])


def change_extension(file: str, new: str) -> str:
    """
    Change extension of file.
    :param file: file path to change extension.
    :param new: new file extension.
    :return: path of file with newly set extension.
    """

    return file.rsplit('.', 1)[0] + '.' + new


def get_relative_path(file_absolute_path: str, root_path: str) -> str:
    """
    Get relative path.
    :param file_absolute_path: file obsolute path.
    :param root_path: get paths relative to this path.
    :return: relative path.
    """

    return './' + file_absolute_path.split(root_path, 1)[-1].strip(' /')


def create_subdir_mk(source_files: set, root_path: str) -> str:
    """
    Creates subdir.mk file.
    :param source_files: list of all source files located into directory (all files must
    be in the same directory!)
    :param root_path: resolve all paths into subdir.mk file relative to this path.
    :return: relative path of created subdir.mk file (relative to root_path parameter).
    """

    objects_list = ''
    deps_list = ''

    relative_path = ''
    for source_file in source_files:
        relative_path = get_relative_path(source_file, root_path)

        objects_list += change_extension(relative_path, 'o') + '\\\n'

        deps_list += os.path.dirname(relative_path) + '/deps/'
        deps_list += change_extension(os.path.basename(relative_path), 'd') + '\\\n'

    objects_list = objects_list.strip('\\\n')
    deps_list = deps_list.strip('\\\n')

    dir_relative_path = os.path.dirname(relative_path)

    try:
        elem = source_files.pop()
        mk_file_path = os.path.dirname(elem) + '/subdir.mk'
        source_files.add(elem)
    except KeyError:
        return ''

    mk_file_content = 'OBJECTS += ' + objects_list + '\n\n'
    mk_file_content += 'CC_DEPS += ' + deps_list + '\n\n'

    c_flags = ' '.join(C_FLAGS)

    for extension in EXTENSIONS:
        mk_file_content += dir_relative_path + '/%.o: ' + dir_relative_path + '/%.' + extension + '\n'
        mk_file_content += '\t$(CC) ' + c_flags + ' $< -o $@\n\n'

    with open(mk_file_path, 'w') as mk_file_pointer:
        mk_file_pointer.write(mk_file_content)
        mk_file_pointer.close()

    return get_relative_path(mk_file_path, root_path)


def get_dependencies_from_source(file_path: str) -> list:
    """
    Get all dependencies of a source file.
    :param file_path: file to extract dependencies from.
    :return: list containing all dependencies given file.
    """

    try:
        with open(file_path, "r") as file_pointer:  # open file
            file_content = file_pointer.read()  # read content

            # get all included header files
            dependencies = re.findall('(?:#include)\\s+\"(.+)\"', file_content)
            file_pointer.close()  # close file

            # return dependencies
            return dependencies
    except FileNotFoundError:  # if file not found, inform user about error end close
        print('[-] Error: Cannot open file:', file_path)
        raise FileNotFoundError


def index_dependencies(source_file: str, found: list) -> None:
    """
    Index all dependencies of a source file recursively (Depth-firt Search approach).
    :param source_file: source file to index dependencies.
    :param found: found dependencies.
    :return: None.
    """

    source_dir_name = os.path.dirname(source_file)
    current_dir = os.getcwd()

    print('\n[+] Reading file:', source_file)

    dependencies = get_dependencies_from_source(source_file)
    os.chdir(source_dir_name)

    for dependency in dependencies:
        new_dependency = os.path.abspath(dependency)

        print('\t-->', new_dependency)

        if new_dependency not in found:
            found.append(new_dependency)
            index_dependencies(new_dependency, found)

    os.chdir(current_dir)


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
        return False


def remove_files(files: set) -> None:
    """
    Removes given set of files.
    :param files: files to remove.
    :return: None.
    """

    for file in files:
        os.remove(file)


def get_path_from_set(paths_set: set) -> str:
    """
    Get an arbitrary path from given set.
    :param paths_set: set to retrieve a path from.
    :return: an arbitrary path from given set.
    """

    elem = paths_set.pop()
    paths_set.add(elem)

    return elem


def create_d_files(source_files: set, root_path: str) -> set:
    """
    Creates .d file (dependency file). It also deletes redundant .d files if CLEAN
    parameter is set to True.
    :param source_files: set containing all source files from a directory
    (all files must be located in the same directory).
    :param root_path: resolve all paths from .d file relative to this path.
    :return: relative path of created .d file (relative to root_path param).
    """

    try:
        path = get_path_from_set(source_files)
    except KeyError:
        return set()

    d_files_directory = os.path.dirname(path) + '/deps/'
    deps_exists = not create_directory(d_files_directory)

    existent_d_files = set()
    if CLEAN and deps_exists:
        existent_d_files = get_d_files(index(d_files_directory))

    d_files = set()

    for file in source_files:
        dependencies = []

        print('[+] Indexing', file)
        index_dependencies(file, dependencies)
        print('\n[+] Done', file, '\n')

        file_relative_path = get_relative_path(file, root_path)
        dependencies_list = '\\\n'.join([file_relative_path] + [get_relative_path(dependency, root_path)
                                        for dependency in dependencies])

        d_file_content = change_extension(file_relative_path, 'o') + ': ' + dependencies_list

        d_file_path = d_files_directory + change_extension(os.path.basename(file), 'd')
        with open(d_file_path, 'w') as d_file_pointer:
            d_file_pointer.write(d_file_content)
            d_file_pointer.close()

        d_files.add(d_file_path)

    redundant_d_files = existent_d_files - d_files
    if redundant_d_files:
        remove_files(redundant_d_files)

    return d_files


def traverse(starting_path: str, root_path: str, ignore_paths: set) -> tuple:
    """
    Traverse project source tree.
    :param starting_path: path to start from.
    :param root_path: porject root path.
    :param ignore_paths: paths to ignore.
    :return: tuple, containing a set of all subdir.mk files and a set of all .d files.
    """

    all_files = index(starting_path)
    directories = get_directories(all_files, ignore_paths)

    subdir_mk_files = set()
    d_files = set()

    for directory in directories:
        mk, d = traverse(directory, root_path, ignore_paths)
        subdir_mk_files.update(mk)
        d_files.update(d)

    source_files = get_source_files(all_files, ignore_paths)

    if source_files:
        subdir_mk_files.add(create_subdir_mk(source_files, root_path))
        d_files.update(create_d_files(source_files, root_path))

    return subdir_mk_files, d_files


def create_makefile() -> None:
    """
    Creates makefiles for project at path PROJECT_ROOT
    :return: None
    """
    project_root_directory = PROJECT_ROOT
    ignore_paths = set([os.path.abspath(file) for file in IGNORE_PATHS])

    try:
        mk_files, d_files = traverse(project_root_directory, project_root_directory, ignore_paths)
    except FileNotFoundError:
        return

    makefile_content = 'CC=' + CC + '\n'\
                       'TARGET=' + TARGET + '\n'\
                       'CC_DEPS :=\n'\
                       'OBJECTS :=\n'\
                       'RM=' + RM

    makefile_content += '\n\nall: ' + TARGET + '\n\n'

    includes = ['-include ' + mk_file for mk_file in mk_files] + ['-include $(CC_DEPS)']

    makefile_content += '\n'.join(includes) + '\n\n'

    c_flags = ' '.join(C_FLAGS - {'-c'})

    makefile_content += TARGET + ': $(OBJECTS)\n'
    makefile_content += '\t$(CC) $(OBJECTS) ' + c_flags + ' -o $(TARGET)\n\n'
    makefile_content += 'clean:\n\t$(RM) $(OBJECTS) $(TARGET)'

    makefile_path = project_root_directory + '/Makefile'

    with open(makefile_path, 'w') as makefile_pointer:
        makefile_pointer.write(makefile_content)
        makefile_pointer.close()

    print('[+] Done.')
