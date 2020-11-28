#!/usr/bin/env python3

from makefile_creator.args import parse_arguments

import makefile_creator.makefiles as makefiles
import makefile_creator.config as config


if __name__ == '__main__':
    args, user_set_args = parse_arguments()

    if args['VERSION']:
        print(config.PACKAGE_NAME, config.VERSION)
        exit()

    if args['CONFIG']:
        config.remove_irrelevant(args)
        config.export_config(args)

        print('[+] Configuration file generated.')
        print('[+] Open \'mfc.config.json\' to change settings.')
        exit()

    if args['CONFIG_UPDATE']:
        config.remove_irrelevant(args)
        config.update_config(args)

        print('[+] Configuration file updated.')
        exit()

    configuration = {}
    if not args['IGNORE_CONFIG_FILE']:
        try:
            configuration = config.import_config(False)
        except FileNotFoundError:
            print('[-] Configuration file does not exist.')
            exit(1)

        for option in args:
            try:
                if option not in user_set_args:
                    args[option] = configuration[option]
            except KeyError:
                continue

    makefiles.set_variables(args)
    makefiles.create_makefiles()
