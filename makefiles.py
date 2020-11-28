#!/usr/bin/env python3

from makefile_creator.iset import Set
from copy import deepcopy

import makefile_creator.file_util as file_util
import makefile_creator.util as util
import os
import re

TARGET = str()
CC = str()
LD = str()
RM = str()
C_FLAGS = Set()
LD_FLAGS = Set()
EXTENSIONS = Set()
INCLUDE_PATHS = Set()
IGNORE_PATHS = Set()
PROJECT_ROOT = str()
BUILD_DIRECTORY = str()
BIN_DIRECTORY = str()
CUSTOM_TARGETS = dict()
VERBOSE = bool()


def set_variables(config: dict) -> None:
    global TARGET
    global CC
    global LD
    global RM
    global C_FLAGS
    global LD_FLAGS
    global EXTENSIONS
    global INCLUDE_PATHS
    global IGNORE_PATHS
    global PROJECT_ROOT
    global BUILD_DIRECTORY
    global BIN_DIRECTORY
    global CUSTOM_TARGETS
    global VERBOSE

    PROJECT_ROOT = config['PROJECT_ROOT'].rstrip()
    BUILD_DIRECTORY = file_util.get_relative_path(config['BUILD_DIRECTORY'], PROJECT_ROOT)
    BIN_DIRECTORY = file_util.get_relative_path(config['BIN_DIRECTORY'], PROJECT_ROOT)
    CC = config['CC']
    LD = config['LD']
    EXTENSIONS.extend(config['EXTENSIONS'])
    IGNORE_PATHS.extend([os.path.abspath(p) for p in config['IGNORE_PATHS']])
    C_FLAGS.extend(config['C_FLAGS'])
    LD_FLAGS.extend(config['LD_FLAGS'])
    RM = config['RM']
    TARGET = config['TARGET']
    CUSTOM_TARGETS = config['CUSTOM_TARGETS']
    VERBOSE = config['VERBOSE']


def create_subdir_mk(source_files: list) -> str:
    """
    Creates subdir.mk file.
    :param source_files: list of all source files located into directory (all files must
    be in the same directory!)
    :return: relative path of created subdir.mk file (relative to root_path parameter).
    """

    objects_list = ''
    deps_list = ''
    src_relative = ''
    built_relative = ''

    source_files.sort()
    for source_file in source_files:
        src_relative = file_util.get_relative_path(source_file, PROJECT_ROOT)

        built_path = BUILD_DIRECTORY + src_relative.strip('.')
        built_relative = file_util.get_relative_path(built_path, PROJECT_ROOT)

        # print(file_util.change_extension(built_relative_path, 'o'))

        objects_list += file_util.change_extension(built_relative, 'o') + ' \\\n'

        deps_list += os.path.dirname(src_relative) + '/deps/'
        deps_list += file_util.change_extension(os.path.basename(src_relative), 'd') + ' \\\n'

    objects_list = objects_list.strip('\\\n')
    deps_list = deps_list.strip('\\\n')

    src_dir_relative = os.path.dirname(src_relative)
    build_dir_relative = os.path.dirname(built_relative)

    # source_files = set(source_files)

    try:
        mk_file_path = os.path.dirname(source_files[0]) + '/subdir.mk'
    except IndexError:
        return ''

    mk_file_content = 'OBJECTS += ' + objects_list + '\n\n'
    mk_file_content += 'CC_DEPS += ' + deps_list + '\n\n'

    c_flags = ' '.join(C_FLAGS)

    for extension in EXTENSIONS:
        mk_file_content += build_dir_relative + '/%.o: ' + src_dir_relative + '/%.' + extension + '\n'
        mk_file_content += '\t@echo \'Building file: $<\'\n'
        mk_file_content += '\t$(CC) ' + c_flags + ' $< -o $@\n'
        mk_file_content += '\t@echo \'Build finished: $<\'\n'
        mk_file_content += "\t@echo\n\n"

    with open(mk_file_path, 'w') as mk_file_pointer:
        mk_file_pointer.write(mk_file_content)
        mk_file_pointer.close()

    return file_util.get_relative_path(mk_file_path, PROJECT_ROOT)


def remove_comments(code: str) -> str:
    uncommented = code.split('//', 1)[0].strip()

    tokens = uncommented.split('/*')
    tokens = [token for token in tokens]

    buff = deepcopy(tokens)
    tokens = [buff[0]]

    for elem in buff:
        try:
            tokens.append(elem.split('*/', 1)[1])
        except IndexError:
            pass

    return ''.join(tokens).strip()


def get_dependencies_from_source(file_path: str) -> list:
    """
    Get all dependencies of a source file.
    :param file_path: file to extract dependencies from.
    :return: list containing all dependencies given file.
    """

    try:
        with open(file_path, "r") as file_pointer:  # open file
            dependencies = list()
            include_detected = False
            lines = file_pointer.readlines()

            for line in lines:
                line = line.strip('\n')
                if '#include' in line:
                    include_detected = True
                    uncommented = remove_comments(line)
                    dependencies.extend(re.findall('(?:#include)\\s+\"(.+)\"', uncommented))
                elif line and include_detected:
                    break

            return dependencies
    except FileNotFoundError:  # if file not found, inform user about error end close
        print('[-] Error: Cannot open file:', file_path)
        raise FileNotFoundError


def index_dependencies(source_file: str, found: list) -> None:
    """
    Index all dependencies of a source file recursively (Depth-first Search approach).
    :param source_file: source file to index dependencies.
    :param found: found dependencies.
    :return: None.
    """

    source_dir_name = os.path.dirname(source_file)
    current_dir = os.getcwd()

    if VERBOSE:
        print('\n[+] Reading file:', source_file)

    dependencies = get_dependencies_from_source(source_file)
    os.chdir(source_dir_name)

    for dependency in dependencies:
        dep_abs_path = os.path.abspath(dependency)

        if not os.path.isfile(dep_abs_path):
            for include_path in INCLUDE_PATHS:
                possible_path = include_path + '/' + dependency
                if os.path.isfile(possible_path):
                    dep_abs_path = possible_path
                    break
            else:
                print('[-] Error:', source_file, 'depends on', dependency, 'but this file cannot be found.')
                raise FileNotFoundError

        if dep_abs_path in IGNORE_PATHS:
            continue

        if VERBOSE:
            print('\t-->', dep_abs_path)

        if dep_abs_path not in found:
            found.append(dep_abs_path)
            index_dependencies(dep_abs_path, found)

    os.chdir(current_dir)


def create_d_files(source_files: list) -> list:
    """
    Creates .d file (dependency file). It also deletes redundant .d files if CLEAN
    parameter is set to True.
    :param source_files: set containing all source files from a directory
    (all files must be located in the same directory).
    :return: relative path of created .d file (relative to root_path param).
    """

    try:
        path = source_files[0]
    except KeyError:
        return []

    d_files_directory = os.path.dirname(path) + '/deps/'
    file_util.create_directory(d_files_directory)

    # existent_d_files = set()
    # if CLEAN and deps_exists:
    #     existent_d_files = set(util.get_d_files(util.index(d_files_directory)))

    d_files = set()
    source_files.sort()

    for file in source_files:
        dependencies = []

        if VERBOSE:
            print('[+] Indexing', file)
        index_dependencies(file, dependencies)
        if VERBOSE:
            print('\n[+] Done', file, '\n')

        dependencies.sort()

        file_relative = file_util.get_relative_path(file, PROJECT_ROOT)
        dependencies_list = ' \\\n'.join([file_relative] + [file_util.get_relative_path(dependency, PROJECT_ROOT)
                                                            for dependency in dependencies])

        object_relative = BUILD_DIRECTORY + file_relative.strip('.')
        object_relative = file_util.get_relative_path(object_relative, PROJECT_ROOT)
        object_relative = file_util.change_extension(object_relative, 'o')

        d_file_content = object_relative + ': ' + dependencies_list

        d_file_path = d_files_directory + file_util.change_extension(os.path.basename(file), 'd')
        with open(d_file_path, 'w') as d_file_pointer:
            d_file_pointer.write(d_file_content)
            d_file_pointer.close()

        d_files.add(d_file_path)

    # redundant_d_files = existent_d_files - d_files
    # if redundant_d_files:
    #     file_util.remove_files(list(redundant_d_files))

    return list(d_files)


def update_build_tree(source_dir: str):
    source_relative = file_util.get_relative_path(source_dir, PROJECT_ROOT)
    levels = source_relative.strip('./').split('/')

    build_relative = ''
    for level in levels:
        build_relative += '/' + level

        build_path = os.path.abspath(BUILD_DIRECTORY + build_relative)
        file_util.create_directory(build_path)


def traverse(starting_path: str) -> tuple:
    """
    Traverse project source tree.
    :param starting_path: path to start from.
    :return: tuple, containing a set of all subdir.mk files and a set of all .d files.
    """

    all_files = util.index(starting_path)
    sources = util.get_source_files(all_files, EXTENSIONS, IGNORE_PATHS)

    subdir_mk_files = Set()
    d_files = Set()

    if sources:
        update_build_tree(starting_path)
        subdir_mk_files.append(create_subdir_mk(sources))
        d_files.extend(create_d_files(sources))

    directories = util.get_directories(all_files, IGNORE_PATHS)
    for directory in directories:
        mk, d = traverse(directory)
        subdir_mk_files.extend(mk)
        d_files.extend(d)

    return subdir_mk_files, d_files


def get_include_paths(compiler_flags: list) -> list:
    paths = list()

    for flag in compiler_flags:
        if flag[:2] == '-I':
            paths.append(os.path.abspath(flag[2:]).rstrip('/'))

    return paths


def create_makefiles() -> None:
    """
    Creates makefiles for project at path PROJECT_ROOT
    :return: None
    """

    INCLUDE_PATHS.extend(get_include_paths(C_FLAGS))

    if not file_util.create_directory(BUILD_DIRECTORY):
        print('[-] Cannot create directory', BUILD_DIRECTORY)
        return

    if not file_util.create_directory(BIN_DIRECTORY):
        print('[-] Cannot create directory', BIN_DIRECTORY)
        return

    try:
        mk_files, d_files = traverse(PROJECT_ROOT)
    except FileNotFoundError:
        return
    
    out_bin = BIN_DIRECTORY + '/' + TARGET
    makefile_content = 'CC=' + CC + '\n' \
                       'LD=' + LD + '\n' \
                       'TARGET=' + out_bin + '\n' \
                       'CC_DEPS :=\n' \
                       'OBJECTS :=\n' \
                       'RM=' + RM

    makefile_content += '\n\nall: ' + out_bin + '\n\n'

    includes = sorted(['-include ' + mk_file for mk_file in mk_files])
    includes.extend(['-include $(CC_DEPS)'])

    makefile_content += '\n'.join(includes) + '\n\n'

    linkage_flags = ' '.join(LD_FLAGS)

    makefile_content += out_bin + ': $(OBJECTS)\n'
    makefile_content += '\t@echo Building target: "$@".\n'
    makefile_content += '\t@echo Invoking $(LD) Linker ...\n'
    makefile_content += '\t$(LD) $(OBJECTS) ' + linkage_flags + ' -o ' + out_bin + '\n'
    makefile_content += '\t@echo Target ' + TARGET + ' build successfully.\n'
    makefile_content += '\t@echo Done.\n\n'

    makefile_content += 'clean:\n\t$(RM) $(OBJECTS) ' + out_bin + '\n\n'

    for target, command in CUSTOM_TARGETS.items():
        makefile_content += target + ':\n'
        makefile_content += '\t' + command + '\n\n'

    makefile_path = PROJECT_ROOT + '/Makefile'

    with open(makefile_path, 'w') as makefile_pointer:
        makefile_pointer.write(makefile_content)
        makefile_pointer.close()

    print('[+] Makefiles successfully created.')
    print('[+] Done.')
