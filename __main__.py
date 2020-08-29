#!/usr/bin/env python3

import makefile_creator

if __name__ == '__main__':
    config = makefile_creator.config.import_config()

    makefile_creator.utils.PROJECT_ROOT = config['PROJECT_ROOT']
    makefile_creator.utils.CC = config['CC']
    makefile_creator.utils.EXTENSIONS = config['EXTENSIONS']
    makefile_creator.utils.IGNORE_PATHS.update(config['IGNORE_PATHS'])
    makefile_creator.utils.C_FLAGS.update(config['C_FLAGS'])
    makefile_creator.utils.RM = config['RM']
    makefile_creator.utils.TARGET = config['TARGET']
    makefile_creator.utils.CLEAN = config['CLEAN']

    makefile_creator.utils.create_makefile()

    print(makefile_creator.config.NAME, end=' ')
    print(makefile_creator.config.VERSION)
