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
from pyswmm import Simulation
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH
import pyswmm


def test_engine_version():
    if sys.platform == 'darwin':
        pyswmm.lib.use("swmm5.dylib")
    elif sys.platform.startswith('linux'):
        pyswmm.lib.use("swmm5.so")
    else:
        if sys.maxsize > 2**32:
            pyswmm.lib.use("swmm5-x64.dll")
        else:
            pyswmm.lib.use("swmm5.dll")

    print(sys.platform)
    print(sys.maxsize)
    sim = Simulation(MODEL_WEIR_SETTING_PATH)
    print(sim.engine_version)


def test_runoff_error():
    sim = Simulation(MODEL_WEIR_SETTING_PATH)
    sim.execute()
    print(sim.runoff_error)
    assert sim.runoff_error >= 0.0


def test_flow_routing_error():
    sim = Simulation(MODEL_WEIR_SETTING_PATH)
    sim.execute()
    print(sim.flow_routing_error)
    assert sim.flow_routing_error >= 0.0


def test_quality_error():
    sim = Simulation(MODEL_WEIR_SETTING_PATH)
    sim.execute()
    print(sim.quality_error)
    assert sim.quality_error >= 0.0
