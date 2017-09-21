# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

# Standard library imports
import sys

# Local imports
# from pyswmm import Simulation
# from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH
import pyswmm


def test_use_1():
    if sys.platform == 'darwin':
        pyswmm.lib.use("libswmm5.dylib")
    elif sys.platform.startswith('linux'):
        pyswmm.lib.use("libswmm5.so")
    else:
        pyswmm.lib.use("swmm5.dll")


#    sim = Simulation(MODEL_WEIR_SETTING_PATH)


def test_use_2():
    if sys.platform == 'darwin':
        pyswmm.lib.use("libswmm5")
    elif sys.platform.startswith('linux'):
        pyswmm.lib.use("libswmm5")
    else:
        pyswmm.lib.use("swmm5")


#    sim = Simulation(MODEL_WEIR_SETTING_PATH)


def test_use_3():
    try:
        pyswmm.lib.use("fakedll.dll")
    except:
        pass


def test_use_4():
    try:
        pyswmm.lib.use("fakedll")
    except:
        pass
