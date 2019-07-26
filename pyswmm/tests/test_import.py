# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

# Standard library imports
import os
import sys

# Local imports
from pyswmm import Simulation
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH, WIN_SWMM_LIB_PATH
import pyswmm
import pytest

def test_use_1():
    if sys.platform == 'darwin':
        pyswmm.lib.use('swmm5.dylib')
    elif sys.platform.startswith('linux'):
        pyswmm.lib.use('swmm5.so')
    else:
        pyswmm.lib.use('swmm5.dll')
        pyswmm.lib.use(WIN_SWMM_LIB_PATH)


def test_use_2():
    pyswmm.lib.use('swmm5')
    if sys.platform == 'nt':
        pyswmm.lib.use(WIN_SWMM_LIB_PATH)


def test_use_3():
    with pytest.raises(Exception) as e:
        assert pyswmm.lib.use('fakedll.dll')
    assert str(e.value) == 'Library Not Found'


def test_use_4():
    with pytest.raises(Exception) as e:
        pyswmm.lib.use('fakedll')
    assert str(e.value) == 'Library Not Found'
    

def test_lib_5():
    """Testing SWMM Path as argument to Simulation Object. 

    On Windows for now."""
    if os.name == 'nt':
        print(WIN_SWMM_LIB_PATH)
        sim = Simulation(MODEL_WEIR_SETTING_PATH, swmm_lib_path=WIN_SWMM_LIB_PATH) 
        sim.execute()
        pyswmm.lib.use(WIN_SWMM_LIB_PATH)
