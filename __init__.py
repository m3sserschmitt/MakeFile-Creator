#!/usr/bin/env python3


import makefile_creator.config as config
import makefile_creator.makefiles as makefiles

config.PACKAGE_NAME = 'makefile_creator'
config.VERSION = 'v0.0.8-beta'

makefiles.PROJECT_ROOT = config.DEFAULTS['PROJECT_ROOT']
makefiles.BUILD_DIRECTORY = config.DEFAULTS['BUILD_DIRECTORY']
makefiles.BIN_DIRECTORY = config.DEFAULTS['BIN_DIRECTORY']
makefiles.CC = config.DEFAULTS['CC']
makefiles.EXTENSIONS.extend(config.DEFAULTS['EXTENSIONS'])
makefiles.C_FLAGS.extend(config.DEFAULTS['C_FLAGS'])
makefiles.RM = config.DEFAULTS['RM']
makefiles.TARGET = config.DEFAULTS['TARGET']
makefiles.VERBOSE = config.DEFAULTS['VERBOSE']
