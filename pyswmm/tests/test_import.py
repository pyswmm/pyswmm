# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""Test imports."""

# Local imports
from pyswmm import Simulation
from pyswmm.lib import LIB_SWMM
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH


def test_library_by_path():
    Simulation(MODEL_WEIR_SETTING_PATH, library=LIB_SWMM)


def test_library_not_found():
    try:
        Simulation(MODEL_WEIR_SETTING_PATH, library='fakelib')
    except:
        pass
