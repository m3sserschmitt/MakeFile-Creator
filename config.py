import makefile_creator.file_util as file_util
from makefile_creator.iset import Set

import copy
import json
import sys
import os

VERSION = str()
PACKAGE_NAME = str()

DEFAULTS = {
    'TARGET': os.path.basename(os.getcwd()),
    'CC': 'gcc',
    'LD': 'gcc',
    'C_FLAGS': Set(['-c', '-Wall']),
    'LD_FLAGS': Set(),
    'LIBS': Set(),
    'INCLUDE_PATHS': Set(),
    'EXTENSIONS': Set(['c', 'cc', 'cpp']),
    'IGNORE_PATHS': Set(),
    'CUSTOM_TARGETS': dict(),
    'VERBOSE': False,
    'RM': 'rm -v',
    'PROJECT_ROOT': os.getcwd(),
    'BUILD_DIRECTORY': file_util.get_relative_path(os.getcwd() + '/build', os.getcwd()),
    'BIN_DIRECTORY': file_util.get_relative_path(os.getcwd() + '/build', os.getcwd())
}


def remove_irrelevant(config: dict) -> None:
    for key in ('PROJECT_ROOT', 'CONFIG', 'CONFIG_UPDATE', 'IGNORE_CONFIG_FILE', 'VERSION'):
        try:
            del config[key]
        except KeyError:
            continue


def get_user_set_config() -> list:
    defaults = copy.deepcopy(DEFAULTS)
    remove_irrelevant(defaults)

    cmd = [arg.split('=', 1)[0].strip('-').upper() for arg in sys.argv[1:]]
    user_set_config = set(cmd).intersection(set(defaults))

    return list(user_set_config)


def import_config(defaults: bool = True) -> dict:
    """
    Imports user configurations from mfc.config.json file.
    :return: dict containing user configurations.
    """
    path = DEFAULTS['PROJECT_ROOT'] + '/mfc.config.json'

    required = {}
    if defaults:
        required = copy.deepcopy(DEFAULTS)

    # open config file, if exists
    with open(path, 'r') as config_file:
        user_configuration = json.load(config_file)
        user_configuration = dict([(conf[0].upper(), conf[1]) for conf in user_configuration.items()])
        required.update(user_configuration)
        config_file.close()

    return required


def export_config(config: dict) -> None:
    path = DEFAULTS['PROJECT_ROOT'] + '/mfc.config.json'

    with open(path, 'w') as file_pointer:
        json.dump(config, file_pointer, indent=2)
        file_pointer.close()


def update_config(config: dict) -> None:
    user_set_config = get_user_set_config()
    user_set_config = dict([(option, config[option]) for option in user_set_config])

    existing_config = import_config(False)
    existing_config.update(user_set_config)
    export_config(existing_config)
