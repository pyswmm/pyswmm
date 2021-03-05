# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

# Standard library imports
from random import randint

# Local imports
import pyswmm.toolkitapi as tka
from pyswmm import Links, Nodes, Simulation
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH


def test_simulation_1():
    sim = Simulation(MODEL_WEIR_SETTING_PATH)
    print(f'system units: {sim.system_units}')
    print(f'swmm version: {sim._model.swmm_getVersion()}')
    allow_ponding = sim._model.getSimOptionSetting(tka.SimAnalysisSettings.AllowPonding)
    routing_step = sim._model.getSimAnalysisSetting(tka.SimulationParameters.RouteStep)
    print(f'analysis setting: {allow_ponding}')
    print(f'analysis param: {routing_step}')
    assert sim.system_units == 'US'
    assert not allow_ponding
    assert routing_step == 1
    for ind, step in enumerate(sim):
        print(sim.current_time)
        sim.step_advance(randint(300, 900))

    sim.close()


def test_simulation_2():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for ind, step in enumerate(sim):
            print(sim.current_time)
            sim.step_advance(randint(300, 900))


def test_simulation_3():
    sim = Simulation(MODEL_WEIR_SETTING_PATH)
    sim.execute()


def test_simulation_4():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for ind, step in enumerate(sim):
            print(sim.percent_complete)
            sim.step_advance(randint(300, 900))


def test_simulation_iter():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        c1c2 = Links(sim)["C1:C2"]

        sim.step_advance(300)
        for ind, step in enumerate(sim):
            print(c1c2.flow, c1c2.target_setting)
            if c1c2.flow > 9.19:
                c1c2.target_setting = 0.9


def test_simulation_9():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        J1 = Nodes(sim)["J1"]

        def init_function():
            J1.initial_depth = 15

        sim.initial_conditions(init_function)
        for ind, step in enumerate(sim):
            if ind == 0:
                assert J1.depth > 14


def test_simulation_callback_1():
    LIST = []
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        LIST.append("OPENED")

        def before_start1():
            LIST.append("before_start1")

        sim.add_before_start(before_start1)

        def before_step1():
            if "before_step1" not in LIST:
                LIST.append("before_step1")

        sim.add_before_step(before_step1)

        def after_step1():
            if "after_step1" not in LIST:
                LIST.append("after_step1")

        sim.add_after_step(after_step1)

        def before_end1():
            if "before_end1" not in LIST:
                LIST.append("before_end1")

        sim.add_before_end(before_end1)

        def after_end1():
            if "after_end1" not in LIST:
                LIST.append("after_end1")

        sim.add_after_end(after_end1)

        def after_close1():
            if "after_close1" not in LIST:
                LIST.append("after_close1")

        sim.add_after_close(after_close1)

        for ind, step in enumerate(sim):
            if ind == 0:
                LIST.append("SIM_STEP")

    assert LIST == [
        "OPENED", "before_start1", "before_step1", "after_step1", "SIM_STEP",
        "before_end1", "after_end1", "after_close1"
    ]
    print(LIST)


def test_simulation_terminate():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        i = 0
        for ind, step in enumerate(sim):
            i += 1
            if ind == 10:
                sim.terminate_simulation()
        assert(i == 11)

