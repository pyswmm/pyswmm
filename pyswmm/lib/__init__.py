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

MACHINE_BITS = str(8 * tuple.__itemsize__)
PYVER = '{0}.{1}'.format(sys.version_info[0], sys.version_info[1])
HERE = os.path.abspath(os.path.dirname(__file__))
VC_MAP = {
    '2.7': 'vc9',
    '3.4': 'vc10',
    '3.5': 'vc14',
    '3.6': 'vc14',
}

# Library path
LIB_SWMM = ''
if os.name == 'nt':
    VC = VC_MAP[PYVER]
    LIB_SWMM = os.path.join(HERE, 'windows', MACHINE_BITS, VC, 'swmm5.dll')
elif sys.platform == 'darwin':
    LIB_SWMM = os.path.join(HERE, 'osx', MACHINE_BITS, 'libswmm5.dylib')
elif sys.platform.startswith('linux'):
    LIB_SWMM = os.path.join(HERE, 'linux', MACHINE_BITS, 'libswmm5.so')
