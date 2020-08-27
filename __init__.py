#!/usr/bin/env python3

import mfc.config
import mfc.utils

mfc.config.NAME = 'MakeFile Creator'
mfc.config.PACKAGE_NAME = 'mfc'
mfc.config.VERSION = 'v0.0.1-beta'

mfc.utils.PROJECT_ROOT = mfc.config.DEFAULTS['PROJECT_ROOT']
mfc.utils.CC = mfc.config.DEFAULTS['CC']
mfc.utils.EXTENSIONS = mfc.config.DEFAULTS['EXTENSIONS']
mfc.utils.IGNORE_PATHS.update(mfc.config.DEFAULTS['IGNORE_PATHS'])
mfc.utils.C_FLAGS.update(mfc.config.DEFAULTS['C_FLAGS'])
mfc.utils.RM = mfc.config.DEFAULTS['RM']
mfc.utils.TARGET = mfc.config.DEFAULTS['TARGET']
mfc.utils.CLEAN = mfc.config.DEFAULTS['CLEAN']
