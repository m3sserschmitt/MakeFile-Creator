#!/usr/bin/env python3


import makefile_creator.config as config
import makefile_creator.utils as utils

config.NAME = 'MakeFile-Creator'
config.PACKAGE_NAME = 'makefile_creator'
config.VERSION = 'v0.0.7-beta'

utils.PROJECT_ROOT = config.DEFAULTS['PROJECT_ROOT']
utils.CC = config.DEFAULTS['CC']
utils.EXTENSIONS = config.DEFAULTS['EXTENSIONS']
utils.C_FLAGS.update(config.DEFAULTS['C_FLAGS'])
utils.RM = config.DEFAULTS['RM']
utils.TARGET = config.DEFAULTS['TARGET']
utils.CLEAN = config.DEFAULTS['CLEAN']
utils.VERBOSE = config.DEFAULTS['VERBOSE']
