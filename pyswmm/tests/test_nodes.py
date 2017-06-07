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
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH
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
            print(node)
            print(node.nodeid)
            print(node.invert_elevation)
            node.invert_elevation = 10
            assert node.invert_elevation == 10


def test_nodes_3():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        print("\n\n\nNODES\n")
        j1 = Nodes(sim)["J1"]
        print(j1.is_divider())
        print(j1.is_junction())
        print(j1.is_outfall())
        print(j1.is_storage())
        print(j1.invert_elevation)


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
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        print("\n\n\nNODES\n")
        node = Nodes(sim)["J5"]
        for ind, step in enumerate(sim):
            if ind > 7:
                node.generated_inflow(5)
            if ind > 8:
                assert int(node.lateral_inflow) == int(5)
