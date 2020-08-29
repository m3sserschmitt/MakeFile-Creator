#!/usr/bin/env python3


import makefile_creator.config
import makefile_creator.utils

makefile_creator.config.NAME = 'MakeFile-Creator'
makefile_creator.config.PACKAGE_NAME = 'makefile_creator'
makefile_creator.config.VERSION = 'v0.0.1-beta1'

makefile_creator.utils.PROJECT_ROOT = makefile_creator.config.DEFAULTS['PROJECT_ROOT']
makefile_creator.utils.CC = makefile_creator.config.DEFAULTS['CC']
makefile_creator.utils.EXTENSIONS = makefile_creator.config.DEFAULTS['EXTENSIONS']
makefile_creator.utils.IGNORE_PATHS.update(makefile_creator.config.DEFAULTS['IGNORE_PATHS'])
makefile_creator.utils.C_FLAGS.update(makefile_creator.config.DEFAULTS['C_FLAGS'])
makefile_creator.utils.RM = makefile_creator.config.DEFAULTS['RM']
makefile_creator.utils.TARGET = makefile_creator.config.DEFAULTS['TARGET']
makefile_creator.utils.CLEAN = makefile_creator.config.DEFAULTS['CLEAN']
