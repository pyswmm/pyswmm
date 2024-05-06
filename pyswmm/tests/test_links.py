# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

# Local imports
from pyswmm import Links, Nodes, Simulation
# from pyswmm.swmm5 import PySWMM
from pyswmm.tests.data import (MODEL_PUMP_SETTINGS_PATH, MODEL_STORAGE_PUMP,
                               MODEL_WEIR_SETTING_PATH)


def test_links_1():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        print("\n\n\nLINKS\n")
        c1c2 = Links(sim)["C1:C2"]
        assert (c1c2.linkid == "C1:C2")
        assert (c1c2.is_conduit() == True)
        assert (c1c2.is_pump() == False)
        assert (c1c2.is_orifice() == False)
        assert (c1c2.is_weir() == False)
        assert (c1c2.is_outlet() == False)
        assert (c1c2.connections == ("J1", "J2"))
        assert (c1c2.inlet_node == "J1")
        assert (c1c2.outlet_node == "J2")


def test_links_2():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        link_names = ["C1", "C1:C2", "C2", "C3"]
        assert "DUMMY_LINK" not in Links(sim)
        for link in Links(sim):
            assert (link.linkid in link_names)
            link.flow_limit = 10
            assert (link.flow_limit == 10)


def test_links_3():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        print("\n\n\nLINKS\n")
        c1c2 = Links(sim)["C1:C2"]
        sim.step_advance(300)
        for ind, step in enumerate(sim):
            if ind > 15:
                c1c2.flow_limit = 1
            if ind > 30:
                c1c2.flow_limit = 0

            if ind > 16 and ind <= 30:
                assert (c1c2.flow == 1)


def test_links_4():
    with Simulation(MODEL_PUMP_SETTINGS_PATH) as sim:
        peak_pump_rate = 20  # cfs
        print("\n\n\nLINKS\n")
        c3 = Links(sim)["C3"]

        sim.step_advance(300)
        for ind, step in enumerate(sim):
            # setting adjustment
            if ind == 15:
                c3.target_setting = 0.9
            if ind == 20:
                c3.target_setting = 0.8
            if ind == 25:
                c3.target_setting = 0.7
            if ind == 30:
                c3.target_setting = 0.6
            if ind == 35:
                c3.target_setting = 2.0
            if ind == 40:
                c3.target_setting = 0.4
            if ind == 45:
                c3.target_setting = 0.3
            if ind == 50:
                c3.target_setting = 0.2
            if ind == 55:
                c3.target_setting = 0.1
            if ind == 60:
                c3.target_setting = 0.0
            if ind == 65:
                c3.target_setting = 1.0

            # Check Results
            if ind == 16:
                assert (c3.target_setting == 0.9)
                assert (c3.flow == 0.9 * peak_pump_rate)
            if ind == 21:
                assert (c3.target_setting == 0.8)
                assert (c3.flow == 0.8 * peak_pump_rate)
            if ind == 26:
                assert (c3.target_setting == 0.7)
                assert (c3.flow == 0.7 * peak_pump_rate)
            if ind == 31:
                assert (c3.target_setting == 0.6)
                assert (c3.flow == 0.6 * peak_pump_rate)
            if ind == 36:
                assert (c3.target_setting == 2.0)
                assert (c3.flow >= peak_pump_rate)
            if ind == 41:
                assert (c3.target_setting == 0.4)
                assert (c3.flow == 0.4 * peak_pump_rate)
            if ind == 46:
                assert (c3.target_setting == 0.3)
                assert (c3.flow == 0.3 * peak_pump_rate)
            if ind == 51:
                assert (c3.target_setting == 0.2)
                assert (c3.flow == 0.2 * peak_pump_rate)
            if ind == 56:
                assert (c3.target_setting == 0.1)
                assert (c3.flow == 0.1 * peak_pump_rate)
            if ind == 61:
                assert (c3.target_setting == 0.0)
                assert (c3.flow == 0.0 * peak_pump_rate)
            if ind == 66:
                assert (c3.target_setting == 1.0)
                assert (c3.flow == 1.0 * peak_pump_rate)


def test_links_5():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        weir_pump_rate = 5  # cfs
        print("\n\n\nWEIR\n")
        c3 = Links(sim)["C3"]

        sim.step_advance(300)
        for ind, step in enumerate(sim):

            # setting adjustment
            if ind == 15:
                c3.target_setting = 0.9
            if ind == 20:
                c3.target_setting = 0.8
            if ind == 25:
                c3.target_setting = 0.7
            if ind == 30:
                c3.target_setting = 0.6
            if ind == 35:
                c3.target_setting = 0.5
            if ind == 40:
                c3.target_setting = 0.4
            if ind == 45:
                c3.target_setting = 0.3
            if ind == 50:
                c3.target_setting = 0.2
            if ind == 55:
                c3.target_setting = 0.1
            if ind == 60:
                c3.target_setting = 0.0
            if ind == 65:
                c3.target_setting = 1.0

            # Check Results
            if ind == 16:
                assert (c3.target_setting == 0.9)
                assert (c3.flow >= 0.9 * weir_pump_rate)
            if ind == 21:
                assert (c3.target_setting == 0.8)
                assert (c3.flow >= 0.8 * weir_pump_rate)
            if ind == 26:
                assert (c3.target_setting == 0.7)
                assert (c3.flow >= 0.7 * weir_pump_rate)
            if ind == 31:
                assert (c3.target_setting == 0.6)
                assert (c3.flow >= 0.6 * weir_pump_rate)
            if ind == 36:
                assert (c3.target_setting == 0.5)
                assert (c3.flow >= 0.5 * weir_pump_rate)
            if ind == 41:
                assert (c3.target_setting == 0.4)
                assert (c3.flow >= 0.4 * weir_pump_rate)
            if ind == 46:
                assert (c3.target_setting == 0.3)
                assert (c3.flow >= 0.3 * weir_pump_rate)
            if ind == 51:
                assert (c3.target_setting == 0.2)
                assert (c3.flow >= 0.15 * weir_pump_rate)
            if ind == 56:
                assert (c3.target_setting == 0.1)
                assert (c3.flow >= 0.05 * weir_pump_rate)
            if ind == 61:
                assert (c3.target_setting == 0.0)
                assert (c3.flow == 0.0 * weir_pump_rate)
            if ind == 66:
                assert (c3.target_setting == 1.0)
                assert (c3.flow >= 1.0 * weir_pump_rate)


def test_links_6():
    with Simulation(MODEL_STORAGE_PUMP) as sim:
        print("\n\n\nConduits\n")
        link = Links(sim)["C2"]

        sim.step_advance(300)
        for ind, step in enumerate(sim):
            if ind % 1000 == 0:
                print(link.conduit_statistics)


def test_links_7():
    with Simulation(MODEL_STORAGE_PUMP) as sim:
        print("\n\n\nPUMPS\n")
        link = Links(sim)["P1"]

        sim.step_advance(300)
        for ind, step in enumerate(sim):
            if ind % 1000 == 0:
                print(link.pump_statistics)
