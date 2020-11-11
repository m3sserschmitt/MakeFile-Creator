import copy
import json
import os

VERSION = str()
NAME = str()
PACKAGE_NAME = str()

DEFAULTS = {
    'TARGET': 'my_project',
    'CC': 'g++',
    'C_FLAGS': ['-Wall', '-c'],
    'LD_FLAGS': [],
    'EXTENSIONS': ['c', 'cc', 'cpp'],
    'IGNORE_PATHS': [],
    'CUSTOM_TARGETS': dict(),
    'VERBOSE': False,
    'RM': 'rm -v',
    'CLEAN': False,
    'PROJECT_ROOT': os.getcwd(),
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
        print('[-] Configuration file does not exist.')
        del DEFAULTS['PROJECT_ROOT']

        with open('mfc.config.json', 'w') as config_file:
            json.dump(DEFAULTS, config_file, indent=2)
            config_file.close()

        print('[+] Configuration file automatically generated.')
        print('[+] Open \'mfc.config.json\' to change default settings.')

    finally:
        return required
