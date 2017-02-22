# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

# Local imports
from pyswmm.swmm5 import PySWMM
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH
from pyswmm.utils.fixtures import get_model_files


def test_error_rpt_out():
    swmmobject = PySWMM(MODEL_WEIR_SETTING_PATH)
    swmmobject.swmm_open()
    swmmobject.swmmExec()
    swmmobject.swmm_close()


def test_warning():
    swmmobject = PySWMM(*get_model_files(MODEL_WEIR_SETTING_PATH))
    swmmobject.swmm_open()
    swmmobject.getLinkResult('C2', 0)
    swmmobject.swmm_close()


def test_pyswmm_exception():
    swmmobject = PySWMM(*get_model_files(MODEL_WEIR_SETTING_PATH))
    swmmobject.swmm_open()
    print(swmmobject.fileLoaded)
    swmmobject.swmm_open()
    swmmobject.swmm_close()


def test_swmm_exception():
    swmmobject = PySWMM(MODEL_WEIR_SETTING_PATH)
    swmmobject.swmm_open()
    print(swmmobject.fileLoaded)
    swmmobject.swmm_open()
    swmmobject.swmm_close()
