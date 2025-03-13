# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
from datetime import datetime

# Third party imports
import pytest

# Local imports
from pyswmm import Simulation, Output
from pyswmm.swmm5 import PySWMM, PYSWMMException
from pyswmm.errors import OutputException
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
    with pytest.raises(Exception) as e:
        with Simulation(MODEL_BAD_INPUT_PATH_1) as sim:
            for step in sim:
                pass
    assert str(e.value).strip() == "ERROR 200: one or more errors in input file."


def test_error_output():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for step in sim:
            pass

    with Output(MODEL_WEIR_SETTING_PATH.replace("inp", "out")) as out:
        with pytest.raises(OutputException):
            out.node_series("potato", "total_inflow")

        with pytest.raises(OutputException):
            out.link_series("C3", "flow_rate", datetime(2021, 1, 1))

        with pytest.raises(OutputException):
            out.link_series(
                "C3", "flow_rate", datetime(2015, 11, 4), datetime(2021, 1, 1)
            )
