# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""SWMM5 compiled libraries."""

# Standard library imports
import os

HERE = os.path.abspath(os.path.dirname(__file__))

# Library paths
LIB_SWMM_WIN_32 = os.path.join(HERE, 'windows', 'swmm5.dll').replace('\\', '/')
