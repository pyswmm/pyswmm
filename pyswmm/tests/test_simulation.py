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
from pyswmm import Nodes, Links, Simulation
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH


def test_simulation_1():
    sim = Simulation(MODEL_WEIR_SETTING_PATH)
    for ind, step in enumerate(sim):
        print(step.getCurrentSimulationTime())
        sim.step_advance(randint(300, 900))

    sim.report()
    sim.close()


def test_simulation_2():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for ind, step in enumerate(sim):
            current_time = step.getCurrentSimulationTime()
            sys.stdout.write("Status: {0}".format(current_time))
            sys.stdout.flush()
            sim.step_advance(randint(300, 900))
        sim.report()


def test_simulation_3():
    sim = Simulation(MODEL_WEIR_SETTING_PATH)
    sim.execute()


def test_simulation_4():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for ind, step in enumerate(sim):
            percent_complete = sim.percent_complete
            sys.stdout.write("Status: {0}".format(percent_complete))
            sys.stdout.flush()
            sim.step_advance(randint(300, 900))
        sim.report()


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


def test_nodes_9():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        J1 = Nodes(sim)["J1"]

        def init_function():
            J1.initial_depth = 15

        sim.initial_conditions(init_function)
        for ind, step in enumerate(sim):
            if ind == 0:
                assert J1.depth > 14

def test_nodes_callback_1():
    LIST = []
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        LIST.append("OPENED")
        def callback_test():
            LIST.append("CALLED")

        _test2 = callback_test
        sim.before_start = callback_test
        sim.before_start = _test2
        for ind, step in enumerate(sim):
            pass

        assert LIST == ["OPENED", "CALLED", "CALLED"]
        print(LIST)
