# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""SWMM5 compiled libraries. This module provides the user with some options
for selecting the SWMM5 engine. """

# Standard library imports
import os
import sys

# Machine Architechture
MACHINE_BITS = 8 * tuple.__itemsize__

# Local Path
HERE = os.path.abspath(os.path.dirname(__file__))

# Library path
LIB_SWMM = ''
if os.name == 'nt':
    if MACHINE_BITS == 64:
        LIB_SWMM = os.path.join(HERE, 'windows', 'swmm5.dll')
    elif MACHINE_BITS == 32:
        LIB_SWMM = os.path.join(HERE, 'windows', 'swmm5.dll')
elif sys.platform == 'darwin':
    LIB_SWMM = os.path.join(HERE, 'macos', 'swmm5.so')
elif sys.platform.startswith('linux'):
    LIB_SWMM = os.path.join(HERE, 'linux', 'swmm5.so')
