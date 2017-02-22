# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

# Standard library imports
from random import randint
import sys

# Local imports
from pyswmm import Links, Simulation
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH


def test_simulation_1():
    sim = Simulation(MODEL_WEIR_SETTING_PATH)
    for ind, step in enumerate(sim):
        print(step.getCurrentSimualationTime())
        sim.step_advance(randint(300, 900))

    sim.report()
    sim.close()


def test_simulation_2():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for ind, step in enumerate(sim):
            current_time = step.getCurrentSimualationTime()
            sys.stdout.write("Status: {0}".format(current_time))
            sys.stdout.flush()
            sim.step_advance(randint(300, 900))
        sim.report()


def test_simulation_3():
    sim = Simulation(MODEL_WEIR_SETTING_PATH)
    sim.execute()


def test_simulation_iter():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        c1c2 = Links(sim)["C1:C2"]
        print(c1c2.flow)

        sim.step_advance(300)
        for ind, step in enumerate(sim):
            print(c1c2.flow, c1c2.target_setting)
            if c1c2.flow > 9.19:
                c1c2.target_setting = 0.9
        sim.report()
