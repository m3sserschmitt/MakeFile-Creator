from argparse import ArgumentParser, Action, Namespace
from makefile_creator.config import DEFAULTS, get_user_set_config
from makefile_creator.iset import Set
from copy import deepcopy


class ArgsListUpdater(Action):
    def __call__(self, parser: ArgumentParser, namespace: Namespace, values, option_string=None):
        namespace_opt = option_string.strip('-').upper()
        values = values.split(',')

        try:
            default_values = vars(namespace)[namespace_opt]
        except KeyError or Exception:
            default_values = Set()

        default_values.update(values)
        namespace.__setattr__(namespace_opt, default_values)


class ArgsListParser(Action):
    def __call__(self, parser: ArgumentParser, namespace: Namespace, values, option_string=None):
        namespace_opt = option_string.strip('-').upper()
        values = Set(values.split(','))
        namespace.__setattr__(namespace_opt, values)


def parse_arguments() -> tuple:
    arg_parser = ArgumentParser()

    defaults = deepcopy(DEFAULTS)

    arg_parser.add_argument('-config', dest='CONFIG', action='store_true', default=False,
                            help='Save configuration provided as command line arguments.')
    arg_parser.add_argument('-config_update', dest='CONFIG_UPDATE', action='store_true', default=False,
                            help='Update configuration with this command line arguments.')
    arg_parser.add_argument('-ignore_config_file', dest='IGNORE_CONFIG_FILE', action='store_true', default=False,
                            help='Ignore configuration file.')

    arg_parser.add_argument('-target', dest='TARGET', default=defaults['TARGET'], help='Project target.')
    arg_parser.add_argument('-cc', dest='CC', default=defaults['CC'], help='Compiler to be used.')
    arg_parser.add_argument('-ld', dest='LD', default=defaults['LD'], help='Linker command.')
    arg_parser.add_argument('-c_flags', dest='C_FLAGS', action=ArgsListUpdater, default=defaults['C_FLAGS'],
                            help='Comma separated list of compiler flags (e.g. -c_flags=flag1,flag2,...).')
    arg_parser.add_argument('-ld_flags', dest='LD_FLAGS', action=ArgsListParser, default=defaults['LD_FLAGS'],
                            help='Comma separated list on linker flags (e.g. -ld_flags=flag1,flag2,...).')
    arg_parser.add_argument('-extensions', dest='EXTENSIONS', action=ArgsListParser, default=defaults['EXTENSIONS'],
                            help='Comma separated list of source files extensions (e.g. -extensions=ext1,ext2,...).')
    arg_parser.add_argument('-ignore_paths', dest='IGNORE_PATHS', default=defaults['IGNORE_PATHS'],
                            action=ArgsListParser,
                            help='Comma separated list of paths to be ignored when traversing source tree.')
    arg_parser.add_argument('-build_directory', dest='BUILD_DIRECTORY', default=defaults['BUILD_DIRECTORY'],
                            help='Project build directory.')
    arg_parser.add_argument('-bin_directory', dest='BIN_DIRECTORY', default=defaults['BIN_DIRECTORY'],
                            help='Binary output directory.')
    arg_parser.add_argument('-verbose', dest='VERBOSE', action='store_true',
                            help='Print details while traversing source tree.')
    arg_parser.add_argument('-version', dest='VERSION', action='store_true', default=False,
                            help='Print version ant exit.')

    parsed_args = vars(arg_parser.parse_args())
    defaults.update(parsed_args)

    return defaults, get_user_set_config()
