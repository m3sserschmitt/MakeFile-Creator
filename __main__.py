#!/usr/bin/env python3


import mfc.config

if __name__ == '__main__':
    config = mfc.config.import_config()

    mfc.utils.PROJECT_ROOT = config['PROJECT_ROOT']
    mfc.utils.CC = config['CC']
    mfc.utils.EXTENSIONS = config['EXTENSIONS']
    mfc.utils.IGNORE_PATHS.update(config['IGNORE_PATHS'])
    mfc.utils.C_FLAGS.update(config['C_FLAGS'])
    mfc.utils.RM = config['RM']
    mfc.utils.TARGET = config['TARGET']
    mfc.utils.CLEAN = config['CLEAN']

    mfc.utils.create_makefile()

    print(mfc.config.NAME, end=' ')
    print(mfc.config.VERSION)
