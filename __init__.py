#!/usr/bin/env python3


import makefile_creator.config as config
import makefile_creator.utils as utils

config.NAME = 'MakeFile-Creator'
config.PACKAGE_NAME = 'makefile_creator'
config.VERSION = 'v0.0.2-beta1'

utils.PROJECT_ROOT = config.DEFAULTS['PROJECT_ROOT']
utils.CC = config.DEFAULTS['CC']
utils.EXTENSIONS = config.DEFAULTS['EXTENSIONS']
utils.C_FLAGS.update(config.DEFAULTS['C_FLAGS'])
utils.RM = config.DEFAULTS['RM']
utils.TARGET = config.DEFAULTS['TARGET']
utils.CLEAN = config.DEFAULTS['CLEAN']
# utils.CUSTOM_TARGETS = config.DEFAULTS['CUSTOM_TARGETS']
