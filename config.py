import copy
import json
import os

VERSION = str()
NAME = str()
PACKAGE_NAME = str()

DEFAULTS = {
    'TARGET': 'my_project',
    'CC': 'g++',
    'RM': 'rm -v',
    'C_FLAGS': {'-Wall', '-c'},
    'LD_FLAGS': set(),
    'EXTENSIONS': ['cpp'],
    'IGNORE_PATHS': set(),
    'PROJECT_ROOT': os.getcwd(),
    'CLEAN': False,
    'CUSTOM_TARGETS': dict()
}


def import_config() -> dict:
    """
    Imports user configurations from mfc.config.json file.
    :return: dict containing user configurations.
    """
    path = DEFAULTS['PROJECT_ROOT'] + '/mfc.config.json'
    required = copy.deepcopy(DEFAULTS)

    try:
        # open config file, if exists
        with open(path, 'r') as config_file:
            user_configuration = json.load(config_file)
            user_configuration = dict([(conf[0].upper(), conf[1]) for conf in user_configuration.items()])
            required.update(user_configuration)
            config_file.close()
    except FileNotFoundError:
        print('[-] Configuration file does not exist')
    finally:
        return required
