# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

# Standard library imports
from datetime import timedelta

# Local imports
from pyswmm.swmm5 import PySWMM
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH
from pyswmm.utils.fixtures import get_model_files


def test_current_time():
    swmmobject = PySWMM(*get_model_files(MODEL_WEIR_SETTING_PATH))
    swmmobject.swmm_open()
    date = swmmobject.getSimulationDateTime(0)
    print(date)
    swmmobject.swmm_start()

    i = 0
    while (True):
        time = swmmobject.swmm_stride(600)
        print(time)
        i += 1
        current_time = swmmobject.getCurrentSimulationTime()
        print(current_time)
        print(type(swmmobject.getCurrentSimulationTime()))

        if (time <= 0.0):
            break
        if i % 144 == 0:
            print(i)

    swmmobject.swmm_end()
    swmmobject.swmm_report()
    swmmobject.swmm_close()


def test_set_current_time():
    swmmobject = PySWMM(*get_model_files(MODEL_WEIR_SETTING_PATH))
    swmmobject.swmm_open()

    print(swmmobject.getSimulationDateTime(0))
    print(swmmobject.getSimulationDateTime(0) - timedelta(days=10))
    swmmobject.setSimulationDateTime(
        0,
        swmmobject.getSimulationDateTime(0) - timedelta(days=10), )
    print(swmmobject.getSimulationDateTime(0))

    print(swmmobject.getSimulationDateTime(1))
    print(swmmobject.getSimulationDateTime(1) - timedelta(days=10))
    swmmobject.setSimulationDateTime(
        1,
        swmmobject.getSimulationDateTime(1) - timedelta(days=10), )
    print(swmmobject.getSimulationDateTime(1))

    print(swmmobject.getSimulationDateTime(2))
    print(swmmobject.getSimulationDateTime(2) - timedelta(days=10))
    swmmobject.setSimulationDateTime(
        2,
        swmmobject.getSimulationDateTime(2) - timedelta(days=10), )
    print(swmmobject.getSimulationDateTime(2))

    swmmobject.swmm_start()

    i = 0
    while (True):
        time = swmmobject.swmm_stride(600)
        i += 1
        print(swmmobject.getCurrentSimulationTime())
        print(type(swmmobject.getCurrentSimulationTime()))

        if (time <= 0.0):
            break

        if i % 144 == 0:
            print(i)

    swmmobject.swmm_end()
    swmmobject.swmm_close()
