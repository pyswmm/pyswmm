# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

# Local imports
from pyswmm import Simulation, SystemStats
from pyswmm.swmm5 import PySWMM
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH


def test_system_flow_routing():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        stats = SystemStats(sim)

        print("\n\n\System\n")
        print(stats.routing_stats)

        sim.step_advance(1200)
        for ind, step in enumerate(sim):
            print(stats.routing_stats)


def test_system_runoff_routing():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        stats = SystemStats(sim)

        print("\n\nRunoff Routing\n\n")
        print(stats.runoff_stats)

        sim.step_advance(1200)
        for ind, step in enumerate(sim):
            print(stats.runoff_stats)
