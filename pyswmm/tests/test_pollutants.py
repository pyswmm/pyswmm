# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2017 Katherine M. Ratliff
# Modified 2022 Brooke E. Mason
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

# Local imports
from pyswmm import Simulation, Subcatchments, Links, Nodes

# from pyswmm.swmm5 import PySWMM
from pyswmm.tests.data import (
    MODEL_POLLUTANTS_PATH,
    MODEL_POLLUTANTS_PATH_2,
    MODEL_POLLUTANTS_PATH_3,
    MODEL_POLLUTANTS_SETTERS_PATH,
)
import pyswmm.toolkitapi as tka
import pytest


def test_pollutants_allobjects_quality():
    with Simulation(MODEL_POLLUTANTS_PATH) as sim:
        S1 = Subcatchments(sim)["S1"]
        S2 = Subcatchments(sim)["S2"]
        S3 = Subcatchments(sim)["S3"]

        C1 = Links(sim)["C1"]
        C2 = Links(sim)["C2"]
        C3 = Links(sim)["C3"]
        C4 = Links(sim)["C4"]

        J1 = Nodes(sim)["J1"]
        J2 = Nodes(sim)["J2"]
        J3 = Nodes(sim)["J3"]
        J4 = Nodes(sim)["J4"]

        for step in sim:
            pass

        assert S1.buildup["test-pollutant"] == 25.000
        assert S2.buildup["test-pollutant"] == 25.000
        assert S3.buildup["test-pollutant"] == 25.000

        assert S1.conc_ponded["test-pollutant"] == pytest.approx(10, abs=1e-5)
        assert S2.conc_ponded["test-pollutant"] == pytest.approx(10, abs=1e-5)
        assert S3.conc_ponded["test-pollutant"] == pytest.approx(10, abs=1e-5)

        assert S1.pollut_quality["test-pollutant"] == 0.0
        assert S2.pollut_quality["test-pollutant"] == 0.0
        assert S3.pollut_quality["test-pollutant"] == 0.0

        assert S1.runoff_total_loading["test-pollutant"] == pytest.approx(
            0.0016770, abs=1e-5
        )
        assert S2.runoff_total_loading["test-pollutant"] == pytest.approx(
            0.0012342, abs=1e-5
        )
        assert S3.runoff_total_loading["test-pollutant"] == pytest.approx(
            0.00077988, abs=1e-5
        )

        assert C1.pollut_quality["test-pollutant"] == 0.0
        assert C2.pollut_quality["test-pollutant"] == 0.0
        assert C3.pollut_quality["test-pollutant"] == 0.0
        assert C4.pollut_quality["test-pollutant"] == 0.0

        assert C1.total_loading["test-pollutant"] == pytest.approx(26.87112, abs=1e-2)
        assert C2.total_loading["test-pollutant"] == pytest.approx(46.64880, abs=1e-2)
        assert C3.total_loading["test-pollutant"] == pytest.approx(12.49796, abs=1e-2)
        assert C4.total_loading["test-pollutant"] == pytest.approx(59.13658, abs=1e-2)

        assert J1.pollut_quality["test-pollutant"] == 0.0
        assert J2.pollut_quality["test-pollutant"] == 0.0
        assert J3.pollut_quality["test-pollutant"] == 0.0
        assert J4.pollut_quality["test-pollutant"] == 0.0


def test_pollutants_link_reactor():
    """
    Test pollutant getter: concentration in the link
    """
    with Simulation(MODEL_POLLUTANTS_PATH_2) as sim:
        C1 = Links(sim)["C1"]

        for step in sim:
            pass

        assert abs(10.000000000000002 - C1.reactor_quality["test-pollutant"]) <= 10e-6


def test_pollutants_node_reactor():
    """
    Test pollutant getter: concentration in the node
    """
    with Simulation(MODEL_POLLUTANTS_PATH_3) as sim:
        Tank = Nodes(sim)["Tank"]

        for step in sim:
            pass

        assert abs(2.302266769180957 - Tank.reactor_quality["P1"]) <= 10e-6


def test_pollutants_node_inflow():
    """
    Test pollutant getter: inflow concentration into a node
    """
    with Simulation(MODEL_POLLUTANTS_PATH_3) as sim:
        Tank = Nodes(sim)["Tank"]

        for step in sim:
            pass

        assert abs(10.000000000000002 - Tank.inflow_quality["P1"]) <= 10e-6


def test_pollutants_node_setter():
    """
    Test pollutant setter in node
    """
    with Simulation(MODEL_POLLUTANTS_PATH_3) as sim:
        Tank = Nodes(sim)["Tank"]

        for step in sim:
            Tank.pollut_quality = ("P1", 100)

        assert Tank.pollut_quality["P1"] == 100.0


def test_pollutants_link_setter():
    """
    Test pollutant setter in link
    """
    with Simulation(MODEL_POLLUTANTS_SETTERS_PATH) as sim:
        C1 = Links(sim)["C1"]

        for step in sim:
            C1.pollut_quality = ("test-pollutant", 100)

        assert C1.pollut_quality["test-pollutant"] == 100.0


def test_pollutants_node_hrt():
    # Test node hrt
    with Simulation(MODEL_POLLUTANTS_PATH_3) as sim:
        Tank = Nodes(sim)["Tank"]
        for _ in sim:
            assert Tank.hydraulic_retention_time is not None
