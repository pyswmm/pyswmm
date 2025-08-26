# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

# Standard library imports
from random import randint
import warnings

# Local imports
import pyswmm.toolkitapi as tka
from pyswmm import Links, Nodes, Simulation, SimulationPreConfig
from pyswmm.errors import MultiSimulationError
from pyswmm.warnings import SimulationContextWarning
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH
import pytest
import os


def test_simulation_1():
    sim = Simulation(MODEL_WEIR_SETTING_PATH)
    print(f"system units: {sim.system_units}")
    print(f"swmm version: {sim._model.swmm_getVersion()}")
    allow_ponding = sim._model.getSimOptionSetting(tka.SimAnalysisSettings.AllowPonding)
    routing_step = sim._model.getSimAnalysisSetting(tka.SimulationParameters.RouteStep)
    print(f"analysis setting: {allow_ponding}")
    print(f"analysis param: {routing_step}")
    assert sim.system_units == "US"
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
    '''Modified test to use "before_start"'''
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        J1 = Nodes(sim)["J1"]

        def init_function():
            J1.initial_depth = 15

        sim.add_before_start(init_function)
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

        def after_start1():
            LIST.append("after_start1")

        sim.add_after_start(after_start1)

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
        "OPENED",
        "before_start1",
        "after_start1",
        "before_step1",
        "after_step1",
        "SIM_STEP",
        "before_end1",
        "after_end1",
        "after_close1",
    ]
    print(LIST)


def test_simulation_terminate():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        i = 0
        for ind, step in enumerate(sim):
            i += 1
            if ind == 10:
                sim.terminate_simulation()
        assert i == 11


def test_hotstart():
    HSF_PATH = MODEL_WEIR_SETTING_PATH.replace(".inp", ".hsf")
    if os.path.exists(HSF_PATH):
        os.remove(HSF_PATH)

    # test saving hotstart works
    assert not os.path.exists(HSF_PATH)

    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        J1 = Nodes(sim)["J1"]
        for ind, step in enumerate(sim):
            if ind == 10:
                sim.save_hotstart(HSF_PATH)
                J1_dep = J1.depth
                break

    assert os.path.exists(HSF_PATH)

    # test loading hotstart works and that data matches
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:

        def store_J1_depth_before_step():
            sim.J1_depth = Nodes(sim)["J1"].depth

        sim.add_before_step(store_J1_depth_before_step)
        sim.use_hotstart(HSF_PATH)

        for ind, step in enumerate(sim):
            break
    assert sim.J1_depth == pytest.approx(J1_dep, 0.00001)


def test_pre_simulation_config():
    sim_preconfig = SimulationPreConfig()
    sim_preconfig.filename_suffix = "_a"
    path_to_modified_inp = MODEL_WEIR_SETTING_PATH.replace(".inp", "_a.inp")

    sim_preconfig.add_update_by_token("SUBCATCHMENTS", "S1", 2, "J2")
    sim_preconfig.add_update_by_token("TIMESERIES", "SCS_24h_Type_I_1in", 2, 2.0, 5)

    with Simulation(MODEL_WEIR_SETTING_PATH, sim_preconfig=sim_preconfig) as sim:
        pass

    with open(path_to_modified_inp, "r") as fl:
        for ind, ln in enumerate(fl):
            if ind == 55:
                compare = [
                    "S1",
                    "SCS_24h_Type_I_1in",
                    "J2",
                    "1",
                    "100",
                    "500",
                    "0.5",
                    "0",
                ]
                ln = ln.strip()
                ln = ln.split()
                assert ln == compare
            if ind == 137:
                compare = ["SCS_24h_Type_I_1in", "1:15", "2.0"]
                ln = ln.strip()
                ln = ln.split()
                assert ln == compare


    # test cleanup
    if os.path.exists(path_to_modified_inp):
        os.remove(path_to_modified_inp)

def test_multi_sim_exception():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        with pytest.raises(MultiSimulationError):
            with Simulation(MODEL_WEIR_SETTING_PATH) as sim2:
                pass
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim3:
        pass


def test_states():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        assert sim.sim_is_open == True
    assert sim.sim_is_open == False

    with Simulation(MODEL_WEIR_SETTING_PATH) as sim3:
        assert sim.sim_is_started == False
        for step in sim:
            assert sim.sim_is_started == True

    sim4 = Simulation(MODEL_WEIR_SETTING_PATH)
    assert sim4.sim_is_open == True
    sim4.close()
    assert sim4.sim_is_open == False

    sim5 = Simulation(MODEL_WEIR_SETTING_PATH)
    assert sim5.sim_is_open == True
    sim5.execute()
    assert sim5.sim_is_open == False


def test_sim_context_warning():
    # Cause all warnings to always be triggered.
    warnings.simplefilter("always")

    # Count number of SimulationContextWarning warnings caught
    def warning_count(warnings_caught):
        return sum(1 for w in warnings_caught if w.category == SimulationContextWarning)

    # Positive: init Simulation without context manager
    with warnings.catch_warnings(record=True) as w1:
        sim1 = Simulation(MODEL_WEIR_SETTING_PATH)
        sim1.execute()
        sim1.execute()
        sim1.close()
        assert warning_count(w1) == 1

    with warnings.catch_warnings(record=True) as w2:
        sim2 = Simulation(MODEL_WEIR_SETTING_PATH)
        sim2.start()
        sim2.start()
        sim2.close()
        assert warning_count(w2) == 1

    # Negative: init Simulation with context manager
    with warnings.catch_warnings(record=True) as w3:
        with Simulation(MODEL_WEIR_SETTING_PATH) as sim3:
            sim3.execute()
            sim3.execute()
            sim3.close()
        assert warning_count(w3) == 0
