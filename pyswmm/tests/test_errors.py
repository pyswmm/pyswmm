# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

# Third party imports
import pytest

# Local imports
from pyswmm import Simulation
from pyswmm.swmm5 import PySWMM, PYSWMMException, SWMMException
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH, MODEL_BAD_INPUT_PATH_1
from pyswmm.utils.fixtures import get_model_files


def test_error_rpt_out():
    swmmobject = PySWMM(MODEL_WEIR_SETTING_PATH)
    swmmobject.swmm_open()


#    swmmobject.swmmExec()
#    swmmobject.swmm_close()


def test_pyswmm_exception():
    swmmobject = PySWMM(*get_model_files(MODEL_WEIR_SETTING_PATH))
    with pytest.raises(PYSWMMException):
        swmmobject.swmm_open()
        print(swmmobject.fileLoaded)
        swmmobject.swmm_open()
        swmmobject.swmm_close()

        
def test_swmm_input_error_1():
    with pytest.raises(SWMMException) as e:
        with Simulation(MODEL_BAD_INPUT_PATH_1) as sim:
            for step in sim:
                pass
    assert(str(e.value).strip() == 'ERROR 200: one or more errors in input file.') 
