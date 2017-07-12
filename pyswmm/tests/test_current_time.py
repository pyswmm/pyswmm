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
from pyswmm import Simulation
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH


def test_current_time():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:

        start = sim.start_time
        print(start)
        endtime = sim.end_time
        print(endtime)

        print(start + timedelta(hours=30))
        sim.start_time = start + timedelta(hours=30)
        sim.end_time = endtime + timedelta(hours=30)
        print("\n\n\nDates\n")
        for step in sim:
            assert (sim.current_time >= sim.start_time)
            assert (sim.current_time <= sim.end_time)
