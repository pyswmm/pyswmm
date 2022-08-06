# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

import pytest

# Local imports
from pyswmm import Simulation, SystemStats
from pyswmm.swmm5 import PySWMM, SWMMException
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH


def test_system_flow_routing():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        stats = SystemStats(sim)

        print(r"\n\n\System\n")
        with pytest.raises(Exception):
            print(stats.routing_stats)

        sim.step_advance(1200)
        for ind, step in enumerate(sim):
            print(stats.routing_stats)


def test_system_runoff_routing():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        stats = SystemStats(sim)

        print("\n\nRunoff Routing\n\n")
        with pytest.raises(Exception):
            print(stats.runoff_stats)

        sim.step_advance(1200)
        for ind, step in enumerate(sim):
            print(stats.runoff_stats)
