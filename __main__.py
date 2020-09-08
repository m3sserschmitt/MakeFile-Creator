#!/usr/bin/env python3

import makefile_creator.utils as utils
import makefile_creator.config as config
from os.path import abspath

if __name__ == '__main__':
    configuration = config.import_config()

    utils.PROJECT_ROOT = configuration['PROJECT_ROOT']
    utils.CC = configuration['CC']
    utils.EXTENSIONS = configuration['EXTENSIONS']
    utils.IGNORE_PATHS.update([abspath(p) for p in configuration['IGNORE_PATHS']])
    utils.C_FLAGS.update(configuration['C_FLAGS'])
    utils.LD_FLAGS.update(configuration['LD_FLAGS'])
    utils.RM = configuration['RM']
    utils.TARGET = configuration['TARGET']
    utils.CLEAN = configuration['CLEAN']
    utils.CUSTOM_TARGETS = configuration['CUSTOM_TARGETS']

    utils.create_makefile()

    print(config.NAME, end=' ')
    print(config.VERSION)
