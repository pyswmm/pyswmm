# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

# Local imports
from pyswmm import Node, Nodes, Simulation
from pyswmm.swmm5 import PySWMM
from pyswmm.tests.data import (MODEL_FULL_FEATURES_PATH, MODEL_STORAGE_PUMP,
                               MODEL_WEIR_SETTING_PATH)
from pyswmm.utils.fixtures import get_model_files
import pyswmm.toolkitapi as tka


def test_nodes_1():
    swmmobject = PySWMM(MODEL_WEIR_SETTING_PATH)
    swmmobject.swmm_open()
    node = Node(swmmobject, "J1")
    print(node.invert_elevation)


def test_nodes_2():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        print("\n\n\nNODES\n")
        for node in Nodes(sim):
            assert ('J' in node.nodeid)
            node.invert_elevation = 10
            assert (node.invert_elevation == 10)


def test_nodes_3():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        print("\n\n\nNODES\n")
        j1 = Nodes(sim)["J1"]
        assert (j1.is_divider() == False)
        assert (j1.is_junction() == True)
        assert (j1.is_outfall() == False)
        assert (j1.is_storage() == False)


def test_nodes_4():
    swmmobject = PySWMM(*get_model_files(MODEL_WEIR_SETTING_PATH))
    swmmobject.swmm_open()

    print(swmmobject.getNodeParam('J2', tka.NodeParams.invertElev))
    swmmobject.setNodeParam('J2', tka.NodeParams.invertElev, 19)
    print(swmmobject.getNodeParam('J2', tka.NodeParams.invertElev))

    print(swmmobject.getLinkParam('C1:C2', tka.LinkParams.offset1))
    swmmobject.setLinkParam('C1:C2', tka.LinkParams.offset1, 19)
    print(swmmobject.getLinkParam('C1:C2', tka.LinkParams.offset1))

    print(swmmobject.getSubcatchParam('S2', tka.SubcParams.area))
    swmmobject.setSubcatchParam('S2', tka.SubcParams.area, 19)
    print(swmmobject.getSubcatchParam('S2', tka.SubcParams.area))

    swmmobject.swmm_start()
    i = 0
    while (True):
        time = swmmobject.swmm_stride(600)
        i += 1

        if (time <= 0.0):
            break

        if i % 144 == 0:
            print(i)

        swmmobject.setLinkParam('C1:C2', tka.LinkParams.qLimit, 0.25)

    swmmobject.swmm_end()
    swmmobject.swmm_close()
    print("swmm_step() Check Passed")


def test_nodes_5():
    sim = Simulation(MODEL_WEIR_SETTING_PATH)
    print("\n\n\nNODES\n")
    J5 = Nodes(sim)["J5"]

    for ind, step in enumerate(sim):
        if ind == 7:
            J5.generated_inflow(544.0)
        if ind > 8:
            assert (J5.lateral_inflow >= 543.9)
            if ind % 1000 == 0:
                print(J5.lateral_inflow)
    sim.close()


def test_nodes_6():
    sim = Simulation(MODEL_WEIR_SETTING_PATH)
    print("\n\n\nNODES\n")
    J5 = Nodes(sim)["J5"]

    for ind, step in enumerate(sim):
        if ind % 1000 == 0:
            print(J5.statistics)
    sim.close()


def test_outfalls_7():
    sim = Simulation(MODEL_STORAGE_PUMP)
    print("\n\n\nSTORAGE\n")
    STOR1 = Nodes(sim)["SU1"]

    for ind, step in enumerate(sim):
        if ind % 1000 == 0:
            print(STOR1.storage_statistics)
    sim.close()


def test_outfalls_8():
    sim = Simulation(MODEL_STORAGE_PUMP)
    print("\n\n\nOUTFALL\n")
    outfall = Nodes(sim)["J3"]

    for ind, step in enumerate(sim):
        if ind % 1000 == 0:
            print(outfall.outfall_statistics)
            print(outfall.cumulative_inflow)
    sim.close()


def test_nodes_9():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        J1 = Nodes(sim)["J1"]

        def init_function():
            J1.initial_depth = 15

        sim.initial_conditions(init_function)
        for step in sim:
            pass
